# ESPHome DHT11 Temperature & Humidity Sensor

Simple ESPHome configuration for reading temperature and humidity using a DHT11 sensor.

This project reports temperature and humidity values to Home Assistant and updates every 15 seconds.

---

## Important Note About Accuracy

The DHT11 is not a high-precision sensor.

* Temperature and humidity readings may have noticeable deviation
* Slow response time compared to modern sensors
* Suitable for basic monitoring, not precision environments

If higher accuracy is required, consider using DHT22, BME280, SHT3x, or similar sensors.

This setup is intended for low-precision monitoring use cases.

---

## Example Use Case

Used for remote monitoring of filament storage conditions.

For critical measurements, a more accurate sensor should be used. This setup is primarily for quick remote checks.

---

## Hardware Required

* ESP32 (any ESPHome-supported board)
* DHT11 sensor (3-pin or 4-pin module)
* Jumper wires

---

## Wiring

Default configuration:

| DHT11 Pin | ESP32 Pin |
| --------- | --------- |
| VCC       | 3.3V      |
| GND       | GND       |
| DATA      | GPIO 33   |

GPIO 33 can be changed in YAML if needed.

This configuration does NOT require an external pull-up resistor.

ESPHome enables the internal software pull-up.

---

## Installation

### 1. Add Sensor Configuration

```yaml
sensor:
  - platform: dht
    pin:
      number: GPIO33
      mode: INPUT_PULLUP
    model: DHT11
    temperature:
      name: "Room Temperature"
      id: room_temperature
      accuracy_decimals: 1
    humidity:
      name: "Room Humidity"
      id: room_humidity
      accuracy_decimals: 1
    update_interval: 15s

```

---

## Configuration Details

* `pin` → GPIO connected to DATA
* `update_interval` → sensor refresh rate (default here: 15 seconds)
* IDs can be used elsewhere in YAML (display, automations, etc.)

---

## Notes

* Works with ESP32 and ESP8266
* Avoid long wires to reduce signal instability
* Keep away from direct airflow or heat sources
* Allow sensor to stabilize for accurate readings

---

## When To Upgrade

Upgrade if you need:

* Better humidity accuracy
* Faster response time
* Stable long-term readings
* Wider temperature range

Recommended alternatives:

* DHT22
* BME280
* SHT31 / SHT30

---

## Summary

This project provides a simple, low-cost temperature and humidity monitoring solution using DHT11.

Best suited for:

* Filament storage monitoring
* Basic room monitoring
* Non-critical environmental tracking

Not recommended for precision-dependent applications.
