#include <Arduino.h>
#include "BobsonGFX.h"

// ================= CONFIG =================
#define SCREEN_W 640
#define SCREEN_H 480

#define GRID_COLS 80
#define GRID_ROWS 60
#define CELL_W 8
#define CELL_H 8

#define LAYERS 3
#define MAX_GRIDS 3

#define FRAME_MS 33   // ~30 FPS (safe)

// ================= TYPES =================
struct Cell {
  uint16_t color;
  bool transparent;
};

struct Grid {
  int layer;
  int x, y;
  int cols, rows;
  int cellW, cellH;
  Cell *cells;
  bool *dirty;
};

// ================= GLOBALS =================

Grid grids[MAX_GRIDS];
int gridCount = 0;

unsigned long lastFrame = 0;

// Demo state
int objX = 10;
int objY = 10;
int dirX = 1;
int counter = 0;

// ================= GRID ENGINE =================
Grid* createGrid(
  int layer,
  int x, int y,
  int cols, int rows,
  int cellW, int cellH
) {
  Grid &g = grids[gridCount++];
  g.layer = layer;
  g.x = x;
  g.y = y;
  g.cols = cols;
  g.rows = rows;
  g.cellW = cellW;
  g.cellH = cellH;

  int count = cols * rows;
  g.cells = (Cell*)malloc(sizeof(Cell) * count);
  g.dirty = (bool*)malloc(sizeof(bool) * count);

  for (int i = 0; i < count; i++) {
    g.cells[i].transparent = true;
    g.cells[i].color = 0;
    g.dirty[i] = true;
  }

  return &g;
}

inline int idx(Grid *g, int x, int y) {
  return y * g->cols + x;
}

void setCell(Grid *g, int x, int y, uint16_t color) {
  if (x < 0 || y < 0 || x >= g->cols || y >= g->rows) return;
  int i = idx(g, x, y);
  g->cells[i].color = color;
  g->cells[i].transparent = false;
  g->dirty[i] = true;
}

void clearCell(Grid *g, int x, int y) {
  if (x < 0 || y < 0 || x >= g->cols || y >= g->rows) return;
  int i = idx(g, x, y);
  g->cells[i].transparent = true;
  g->dirty[i] = true;
}

// Resolve visible color at grid cell position
bool resolveCellColor(int gx, int gy, uint16_t &outColor) {
  for (int l = LAYERS - 1; l >= 0; l--) {
    for (int g = 0; g < gridCount; g++) {
      Grid *gr = &grids[g];
      if (gr->layer != l) continue;
      if (gx < 0 || gy < 0 || gx >= gr->cols || gy >= gr->rows) continue;
      int i = idx(gr, gx, gy);
      if (!gr->cells[i].transparent) {
        outColor = gr->cells[i].color;
        return true;
      }
    }
  }
  return false;
}

// ================= RENDER =================
void render() {
  for (int y = 0; y < GRID_ROWS; y++) {
    for (int x = 0; x < GRID_COLS; x++) {

      bool needsDraw = false;
      for (int g = 0; g < gridCount; g++) {
        if (grids[g].dirty[idx(&grids[g], x, y)]) {
          needsDraw = true;
          break;
        }
      }
      if (!needsDraw) continue;

      uint16_t color = 0;
      bool visible = resolveCellColor(x, y, color);

      int px = x * CELL_W;
      int py = y * CELL_H;

      if (visible) {
        tft.fillRect(px, py, CELL_W, CELL_H, color);
      } else {
        tft.fillRect(px, py, CELL_W, CELL_H, 0);
      }

      for (int g = 0; g < gridCount; g++) {
        grids[g].dirty[idx(&grids[g], x, y)] = false;
      }
    }
  }
}

// ================= DEMO LOGIC =================
Grid *bg;
Grid *obj;
Grid *ui;

void updateDemo() {
  // Background once
  static bool bgInit = false;
  if (!bgInit) {
    for (int y = 0; y < GRID_ROWS; y++)
      for (int x = 0; x < GRID_COLS; x++)
        setCell(bg, x, y, 0x001F); // blue
    bgInit = true;
  }

  // Clear old object
  clearCell(obj, objX, objY);

  objX += dirX;
  if (objX <= 1 || objX >= GRID_COLS - 2) dirX = -dirX;

  // Draw new object
  setCell(obj, objX, objY, 0xFFFF); // white

  // UI counter
  int uiX = 2;
  int uiY = 2;
  clearCell(ui, uiX, uiY);
  setCell(ui, uiX + (counter % 10), uiY, 0xFFE0); // yellow

  counter++;
}

// ================= SETUP / LOOP =================
void setup() {
  Serial.begin(115200);
  tft.begin();
  tft.fillScreen(0);

  bg  = createGrid(0, 0, 0, GRID_COLS, GRID_ROWS, CELL_W, CELL_H);
  obj = createGrid(1, 0, 0, GRID_COLS, GRID_ROWS, CELL_W, CELL_H);
  ui  = createGrid(2, 0, 0, GRID_COLS, GRID_ROWS, CELL_W, CELL_H);

  Serial.println("Bobson layered grid demo started");
}

void loop() {
  unsigned long now = millis();
  if (now - lastFrame < FRAME_MS) return;
  lastFrame = now;

  updateDemo();
  render();
}
