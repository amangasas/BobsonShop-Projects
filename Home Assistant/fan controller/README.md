# ESPHome PWM Fan Controller

Simple remote PWM fan controller using ESPHome.

This project allows remote control of a 4-pin PWM fan and reads RPM using the tachometer signal.

---

## What This Does

* Controls fan speed using PWM
* Reads fan RPM via tach pin
* Allows remote control from Home Assistant
* Suitable for server racks, enclosures, cabinets, or workshop setups

---

## Hardware Required

* ESP32 (ESPHome-supported board)
* 4-pin PWM fan
* External power supply (if required by fan)
* Jumper wires

---

## Pin Configuration

Default configuration:

| Function | ESP32 Pin |
| -------- | --------- |
| PWM      | GPIO 5    |
| TACH     | GPIO 4    |

Pins can be changed inside the YAML configuration file.

---

## Power Notes

Some fans draw more current than the ESP32 can safely supply.

If required:

* Use an external PSU for the fan
* Connect grounds together (ESP32 GND and PSU GND)
* Do NOT power high-current fans directly from ESP32 5V pin

Always verify fan voltage requirements (5V / 12V).

---

## Example Configuration

```yaml
output:
  - platform: ledc
    pin: 5
    id: fan_pwm_out
    frequency: 25000 Hz

fan:
  - platform: speed
    output: fan_pwm_out
    name: "P1P Exhaust Fan"
    id: exhaust_fan

sensor:
  - platform: pulse_counter
    pin: 4
    name: "P1P Exhaust RPM"
    id: exhaust_rpm
    update_interval: 1s
    internal_filter: 10us
    filters:
      - multiply: 30   # (Hz * 60) / 2 pulses = RPM
```

---

## Configuration Notes

* PWM frequency commonly used for 4-pin fans: 25 kHz
* Tach output typically provides 2 pulses per revolution
* The multiply filter adjusts pulse count to RPM (may vary per fan)

---

## Customization

You can:

* Rename entities inside YAML
* Change pins
* Add temperature-based automation
* Add minimum speed limits
* Add fail-safe behavior

---

## Typical Use Cases

* Server cooling control
* Enclosure airflow management
* 3D printer enclosure cooling
* Workshop ventilation

---

## Important

* Always verify wiring before powering
* Ensure common ground between ESP32 and fan PSU
* Test at low speed first

---

This project provides a simple remote-controlled PWM fan solution using ESPHome.
