#pragma once
#include <stdint.h>
namespace cfg {
// Photo: ESP8266 ESP-12E NodeMCU, NOT ESP32. Use GPIO numbers here.
constexpr uint8_t STEP_PIN = 14, DIR_PIN = 12, ENABLE_PIN = 13, BUTTON_PIN = 4;
constexpr bool INVERT_DIRECTION = false;
constexpr unsigned FULL_STEPS = 200; // Assumed 1.8 degree motor; verify your motor.
constexpr unsigned MICROSTEPS = 16;  // A4988 MS1/MS2/MS3 all HIGH physically.
constexpr float STEPS_PER_DEGREE = FULL_STEPS * MICROSTEPS / 360.0f;
struct Preset {
  const char *name;
  float amplitudeDeg, speedDegS, accelDegS2;
  uint8_t cycles;
  uint32_t settleMs;
  float spinRpm, spinAccelDegS2, spinHoldSeconds;
  uint32_t restMs;
};
// Exploratory settings, NOT calibrated gold-recovery recipes or rated limits.
constexpr Preset PRESETS[] = {{"LOW", 5, 60, 120, 6, 3000, 10, 120, 1.0f, 2000},
                              {"MEDIUM", 10, 90, 240, 8, 2500, 20, 180, 1.0f, 2000},
                              {"HIGH", 15, 120, 360, 10, 2000, 30, 240, 1.0f, 2000}};
constexpr unsigned PRESET_COUNT = sizeof(PRESETS) / sizeof(PRESETS[0]);
static_assert(FULL_STEPS > 0 && MICROSTEPS > 0, "Invalid step scaling");
constexpr bool valid(Preset p) {
  return p.amplitudeDeg > 0 && p.speedDegS > 0 && p.accelDegS2 > 0 && p.cycles > 0 &&
         p.spinRpm > 0 && p.spinAccelDegS2 > 0 && p.spinHoldSeconds >= 0;
}
static_assert(valid(PRESETS[0]) && valid(PRESETS[1]) && valid(PRESETS[2]),
              "Presets require positive speeds, acceleration, amplitude and cycles");
} // namespace cfg
