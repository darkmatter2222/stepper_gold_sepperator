#pragma once
#include <stdint.h>
namespace cfg {
// Photo: ESP8266 ESP-12E NodeMCU, NOT ESP32. Use GPIO numbers here.
constexpr uint8_t STEP_PIN = 14, DIR_PIN = 12, ENABLE_PIN = 13, BUTTON_PIN = 4;
constexpr uint8_t PUMP_PIN = 5; // D1, active HIGH to the low-side MOSFET gate resistor.
constexpr bool PUMP_AUTO_DEFAULT = true;
constexpr bool PUMP_DURING_SPIN = false; // Quiet settling and no added spin spray by default.
constexpr uint32_t PUMP_PRIME_MS = 3000, PUMP_CALIBRATE_MS = 30000;
struct PumpSchedule {
  uint32_t onMs, offMs;
};
constexpr PumpSchedule PUMP_SCHEDULE[] = {{500, 4500}, {750, 4250}, {1000, 4000}};
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
static_assert(sizeof(PUMP_SCHEDULE) / sizeof(PUMP_SCHEDULE[0]) == PRESET_COUNT,
              "Pump preset mismatch");
constexpr bool validPump(PumpSchedule p) {
  return p.onMs > 0 && p.onMs <= 5000 && p.offMs > 0 && p.offMs <= 60000;
}
static_assert(validPump(PUMP_SCHEDULE[0]) && validPump(PUMP_SCHEDULE[1]) &&
                  validPump(PUMP_SCHEDULE[2]),
              "Invalid pump timing");
static_assert(PUMP_PIN != STEP_PIN && PUMP_PIN != DIR_PIN && PUMP_PIN != ENABLE_PIN &&
                  PUMP_PIN != BUTTON_PIN,
              "Pump GPIO collision");
static_assert(FULL_STEPS > 0 && MICROSTEPS > 0, "Invalid step scaling");
constexpr bool valid(Preset p) {
  return p.amplitudeDeg > 0 && p.speedDegS > 0 && p.accelDegS2 > 0 && p.cycles > 0 &&
         p.spinRpm > 0 && p.spinAccelDegS2 > 0 && p.spinHoldSeconds >= 0;
}
static_assert(valid(PRESETS[0]) && valid(PRESETS[1]) && valid(PRESETS[2]),
              "Presets require positive speeds, acceleration, amplitude and cycles");
} // namespace cfg
