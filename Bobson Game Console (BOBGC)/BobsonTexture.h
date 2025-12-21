#pragma once
#include <Arduino.h>
#include <LittleFS.h>
#include "BobsonGFX.h"

struct Texture {
    int width;
    int height;
    uint16_t* pixels; // row-major, width*height
};

class BobsonTexture {
public:
    BobsonTexture() {}

    bool begin() { return LittleFS.begin(); }   // initialize LittleFS

    Texture loadTexture(const char* path);          // load from LittleFS
    void drawTexture(int x, int y, const Texture& tex, BobsonGFX &tft); // draw at coordinates
    void freeTexture(Texture& tex);                 // free memory if dynamically allocated
};
