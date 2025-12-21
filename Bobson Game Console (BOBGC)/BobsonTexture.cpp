#include "BobsonTexture.h"

Texture BobsonTexture::loadTexture(const char* path) {
    Texture tex = {0, 0, nullptr};

    File f = LittleFS.open(path, "r");
    if (!f) {
        Serial.printf("Failed to open texture %s\n", path);
        return tex;
    }

    // read width,height from first line
    String line = f.readStringUntil('\n');
    int commaIndex = line.indexOf(',');
    if (commaIndex == -1) return tex;

    tex.width = line.substring(0, commaIndex).toInt();
    tex.height = line.substring(commaIndex + 1).toInt();

    tex.pixels = new uint16_t[tex.width * tex.height];

    for (int i = 0; i < tex.width * tex.height; ++i) {
        if (!f.available()) break;
        tex.pixels[i] = (uint16_t)f.readStringUntil('\n').toInt();
    }

    f.close();
    return tex;
}

void BobsonTexture::drawTexture(int x0, int y0, const Texture& tex, BobsonGFX &tft) {
    if (!tex.pixels) return;

    for (int y = 0; y < tex.height; ++y) {
        for (int x = 0; x < tex.width; ++x) {
            uint16_t color = tex.pixels[y * tex.width + x];
            tft.fillRect(x0 + x, y0 + y, 1, 1, color); // draw pixel as 1x1 rect
        }
    }
}

void BobsonTexture::freeTexture(Texture& tex) {
    if (tex.pixels) {
        delete[] tex.pixels;
        tex.pixels = nullptr;
    }
}
