import pygame
import serial
import sys

# --- Settings ---
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
TERM_WIDTH, TERM_HEIGHT = 640, 480
SERIAL_PORT = "COM6"   # Change to your ESP32 serial port
BAUDRATE = 115200

# --- Init pygame ---
pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH + TERM_WIDTH, max(SCREEN_HEIGHT, TERM_HEIGHT)))
pygame.display.set_caption("Bobson Emulator + Serial Terminal")

screen_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
term_surface = pygame.Surface((TERM_WIDTH, TERM_HEIGHT))

# --- State ---
font = pygame.font.SysFont("monospace", 14)
cursor = (0, 0)
text_color = (255, 255, 255)
bg_color = (0, 0, 0)
wrap = False
serial_lines = []
MAX_LINES = TERM_HEIGHT // 16
buffer = ""

# --- Serial ---
ser = None
connected = False

def open_serial():
    global ser, connected
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.01)
        connected = True
        print(f"Connected to {SERIAL_PORT}")
    except Exception as e:
        connected = False
        print(f"Could not open serial: {e}")

def close_serial():
    global ser, connected
    try:
        if ser:
            ser.close()
    except:
        pass
    ser = None
    connected = False
    print("Disconnected")

# --- Utilities ---
def rgb565_to_rgb888(color):
    r = ((color >> 11) & 0x1F) << 3
    g = ((color >> 5) & 0x3F) << 2
    b = (color & 0x1F) << 3
    return (r, g, b)

def handle_command(cmd):
    global cursor, text_color, bg_color, wrap, font
    serial_lines.append(cmd)
    if len(serial_lines) > MAX_LINES:
        serial_lines.pop(0)

    parts = cmd.strip().split()
    if not parts:
        return

    op = parts[0]
    try:
        if op == "FILL":
            color = rgb565_to_rgb888(int(parts[1]))
            screen_surface.fill(color)
        elif op == "LINE":
            x0, y0, x1, y1, c = map(int, parts[1:])
            pygame.draw.line(screen_surface, rgb565_to_rgb888(c), (x0, y0), (x1, y1))
        elif op == "RECT":
            x, y, w, h, c = map(int, parts[1:])
            pygame.draw.rect(screen_surface, rgb565_to_rgb888(c), (x, y, w, h), 1)
        elif op == "FRECT":
            x, y, w, h, c = map(int, parts[1:])
            pygame.draw.rect(screen_surface, rgb565_to_rgb888(c), (x, y, w, h))
        elif op == "CIRC":
            x, y, r, c = map(int, parts[1:])
            pygame.draw.circle(screen_surface, rgb565_to_rgb888(c), (x, y), r, 1)
        elif op == "FCIRC":
            x, y, r, c = map(int, parts[1:])
            pygame.draw.circle(screen_surface, rgb565_to_rgb888(c), (x, y), r)
        elif op == "TRI":
            x0, y0, x1, y1, x2, y2, c = map(int, parts[1:])
            pygame.draw.polygon(screen_surface, rgb565_to_rgb888(c), [(x0,y0),(x1,y1),(x2,y2)], 1)
        elif op == "FTRI":
            x0, y0, x1, y1, x2, y2, c = map(int, parts[1:])
            pygame.draw.polygon(screen_surface, rgb565_to_rgb888(c), [(x0,y0),(x1,y1),(x2,y2)])
        elif op == "CUR":
            cursor = (int(parts[1]), int(parts[2]))
        elif op == "TXTCLR":
            if len(parts) == 2:
                text_color = rgb565_to_rgb888(int(parts[1]))
            elif len(parts) == 3:
                text_color = rgb565_to_rgb888(int(parts[1]))
                bg_color = rgb565_to_rgb888(int(parts[2]))
        elif op == "TXTSZ":
            size = int(parts[1])
            font = pygame.font.SysFont("monospace", 8*size)
        elif op == "WRAP":
            wrap = (parts[1] == "1")
        elif op == "STR":
            x, y = int(parts[1]), int(parts[2])
            text = " ".join(parts[3:])
            text_surface = font.render(text, True, text_color, bg_color)
            screen_surface.blit(text_surface, (x, y))
    except Exception as e:
        print(f"Command error: {cmd} -> {e}")

def main_loop():
    global buffer, connected, ser
    clock = pygame.time.Clock()
    open_serial()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_serial()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Press 'C' to try reconnect
                    if not connected:
                        open_serial()
                    else:
                        close_serial()

        # --- Read serial safely ---
        if connected and ser:
            try:
                while ser.in_waiting:
                    char = ser.read().decode(errors="ignore")
                    if char == "\n":
                        handle_command(buffer.strip())
                        buffer = ""
                    else:
                        buffer += char
            except Exception as e:
                print(f"Serial disconnected: {e}")
                close_serial()

        # --- Render window ---
        window.fill((0, 0, 0))
        window.blit(screen_surface, (0, 0))

        # Draw terminal
        term_surface.fill((0, 0, 0))
        for i, line in enumerate(serial_lines):
            surf = font.render(line, True, (0, 255, 0))
            term_surface.blit(surf, (2, i*16))
        window.blit(term_surface, (SCREEN_WIDTH, 0))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_loop()
