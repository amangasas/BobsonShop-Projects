#pragma once
#include <Arduino.h>

class BobsonGFX {
  public:
    void begin() { Serial.println("BEGIN"); }
    void init() { Serial.println("INIT"); }
    void setRotation(uint8_t r) { Serial.printf("ROT %d\n", r); }
    void fillScreen(uint16_t color) { Serial.printf("FILL %u\n", color); }

    void drawLine(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1, uint16_t color) {
      Serial.printf("LINE %d %d %d %d %u\n", x0,y0,x1,y1,color);
    }
    void drawRect(uint16_t x0,uint16_t y0,uint16_t w,uint16_t h,uint16_t color) {
      Serial.printf("RECT %d %d %d %d %u\n",x0,y0,w,h,color);
    }
    void fillRect(uint16_t x0,uint16_t y0,uint16_t w,uint16_t h,uint16_t color) {
      Serial.printf("FRECT %d %d %d %d %u\n",x0,y0,w,h,color);
    }
    void drawCircle(uint16_t x0,uint16_t y0,uint16_t r,uint16_t color) {
      Serial.printf("CIRC %d %d %d %u\n",x0,y0,r,color);
    }
    void fillCircle(uint16_t x0,uint16_t y0,uint16_t r,uint16_t color) {
      Serial.printf("FCIRC %d %d %d %u\n",x0,y0,r,color);
    }
    void drawTriangle(uint16_t x0,uint16_t y0,uint16_t x1,uint16_t y1,uint16_t x2,uint16_t y2,uint16_t color) {
      Serial.printf("TRI %d %d %d %d %d %d %u\n",x0,y0,x1,y1,x2,y2,color);
    }
    void fillTriangle(uint16_t x0,uint16_t y0,uint16_t x1,uint16_t y1,uint16_t x2,uint16_t y2,uint16_t color) {
      Serial.printf("FTRI %d %d %d %d %d %d %u\n",x0,y0,x1,y1,x2,y2,color);
    }

    void setCursor(int16_t x,int16_t y) { Serial.printf("CUR %d %d\n",x,y); }
    void setTextColor(uint16_t c) { Serial.printf("TXTCLR %u\n",c); }
    void setTextColor(uint16_t c,uint16_t bg) { Serial.printf("TXTCLR %u %u\n",c,bg); }
    void setTextSize(uint8_t s) { Serial.printf("TXTSZ %d\n",s); }
    void setTextWrap(bool w) { Serial.printf("WRAP %d\n",w?1:0); }
    void drawString(const char *str,int16_t x,int16_t y) { Serial.printf("STR %d %d %s\n",x,y,str); }
};

extern BobsonGFX tft;
