# ESPHome SSD1306 Numeric Sensor Display

Simple ESPHome configuration for displaying up to 4 numeric sensors on a 128x32 SSD1306 I2C OLED.

This project listens to sensor states (from Home Assistant or local sensors) and displays formatted numeric values in a clean 2x2 layout.

---

## What This Does

* Connects to Home Assistant
* Reads numeric sensor states
* Displays formatted values on OLED
* Supports any unit (W, °C, %, RPM, mL, etc.)
* Fully customizable layout

---

## Hardware Required

* ESP32 (any supported ESPHome board)
* SSD1306 128x32 I2C OLED
* 4 jumper wires

### Default Wiring

| OLED | ESP32   |
| ---- | ------- |
| VCC  | 3.3V    |
| GND  | GND     |
| SDA  | GPIO 18 |
| SCL  | GPIO 19 |

Pins can be changed inside YAML if needed.

---

## Installation

### 1. Add I2C

```yaml
i2c:
  sda: 18
  scl: 19
  scan: true
```

---

### 2. Add Font

```yaml
font:
  - file: "gfonts://Roboto"
    id: font_small
    size: 12
```

---

### 3. Add Sensors

Example using Home Assistant sensors:

```yaml
sensor:
  - platform: homeassistant
    id: id1
    entity_id: sensor.pc_power

  - platform: homeassistant
    id: id2
    entity_id: sensor.nas_power

  - platform: homeassistant
    id: id3
    entity_id: sensor.cnc_power

  - platform: homeassistant
    id: id4
    entity_id: sensor.printer_power
```

Replace entity_id values with your own sensors.

IDs (id1, id2, etc.) must match what is used in the display section.

---

### 4. Add Display

```yaml
display:
  - platform: ssd1306_i2c
    model: "SSD1306 128x32"
    address: 0x3C
    lambda: |-
      // Top row
      it.printf(0, 0, id(font_small), "PC %3.0fW", id(id1).state);
      it.printf(64, 0, id(font_small), "NAS %3.0fW", id(id2).state);

      // Bottom row
      it.printf(0, 16, id(font_small), "CNC %4.0fW", id(id3).state);
      it.printf(64, 16, id(font_small), "P1S %3.0fW", id(id4).state);
```

---

## How Formatting Works

Example:

```
"PC %3.0fW"
```

Explanation:

* %3.0f → float formatting

  * 3 = minimum width
  * .0 = number of decimals
  * f = float
* W = text label (unit)

---

## Changing Units

Only modify the text inside printf().

### Temperature

```cpp
"Room %3.1f°C"
```

### Humidity

```cpp
"Hum %3.0f%%"
```

Use %% to print a single percent sign.

### RPM

```cpp
"Fan %4.0fRPM"
```

### Milliliters

```cpp
"Tank %4.0fmL"
```

The sensor does not enforce units — it simply prints numeric state.

---

## Changing Layout

Format:

```
it.printf(X, Y, font, "text", sensor.state);
```

For 128x32 display:

* X range: 0–127
* Y range: 0–31
* Top row: Y = 0
* Bottom row: Y = 16

Adjust X values to move items left or right.

---

## Notes

* Sensors must return numeric values
* If a sensor is unavailable, NaN will be printed
* Compatible with ESP8266 and ESP32
* Additional pages can be implemented manually if desired

---

## Example Use Cases

* Server power monitoring
* 3D printer dashboard
* CNC live metrics
* Workshop monitor
* Smart home quick-view panel
