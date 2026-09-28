#pragma once
#include <stdint.h>
namespace cfg {
// Photo: ESP8266 ESP-12E NodeMCU, NOT ESP32. Use GPIO numbers here.
constexpr uint8_t STEP_PIN = 14, DIR_PIN = 12, ENABLE_PIN = 13, BUTTON_PIN = 4;
constexpr uint8_t PUMP_PIN = 5; // D1, active HIGH through 4.7k to 2N3904 driving IRF9540N high-side switch.
constexpr bool PUMP_AUTO_DEFAULT = true;
constexpr bool PUMP_DURING_SPIN = false; // Quiet settling and no added spin spray by default.
constexpr uint32_t PUMP_PRIME_MS = 3000, PUMP_CALIBRATE_MS = 30000;
struct PumpSchedule {
  uint32_t onMs, offMs;
};
constexpr PumpSchedule PUMP_SCHEDULE[] = {{500, 4500}, {750, 4250}, {1000, 4000},
                                            {1000, 4000}, {1000, 4000}, {1000, 4000}};
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
// Experimental loaded-bed trials; see docs/MOTION.md. Not motor ratings.
// Keep 1/16 wiring. Bound requested pulse rate for the cooperative step loop.
constexpr float MAX_STEP_RATE = 12000;
// Modes 1-3 keep the user's tested speeds and double the rocking cycle count.
// Modes 4-6 are modest experimental increments; same angle and ~10s agitation.
constexpr Preset PRESETS[] = {{"LOW", 12, 540, 7200, 36, 3000, 90, 1800, 0.5f, 2000},
                              {"MEDIUM", 16, 810, 14400, 48, 3000, 135, 2700, 0.5f, 2000},
                              {"HIGH", 20, 1080, 21600, 60, 3000, 180, 3600, 0.5f, 2000},
                              {"TRIAL4", 20, 1170, 25350, 65, 3000, 195, 3900, 0.5f, 2000},
                              {"TRIAL5", 20, 1260, 29400, 70, 3000, 210, 4200, 0.5f, 2000},
                              {"TRIAL6", 20, 1350, 33750, 75, 3000, 225, 4500, 0.5f, 2000}};
constexpr unsigned PRESET_COUNT = sizeof(PRESETS) / sizeof(PRESETS[0]);
static_assert(sizeof(PUMP_SCHEDULE) / sizeof(PUMP_SCHEDULE[0]) == PRESET_COUNT,
              "Pump preset mismatch");
constexpr bool validPump(PumpSchedule p) {
  return p.onMs > 0 && p.onMs <= 5000 && p.offMs > 0 && p.offMs <= 60000;
}
static_assert(validPump(PUMP_SCHEDULE[0]) && validPump(PUMP_SCHEDULE[1]) &&
                  validPump(PUMP_SCHEDULE[2]) && validPump(PUMP_SCHEDULE[3]) &&
                  validPump(PUMP_SCHEDULE[4]) && validPump(PUMP_SCHEDULE[5]),
              "Invalid pump timing");
static_assert(PUMP_PIN != STEP_PIN && PUMP_PIN != DIR_PIN && PUMP_PIN != ENABLE_PIN &&
                  PUMP_PIN != BUTTON_PIN,
              "Pump GPIO collision");
static_assert(FULL_STEPS > 0 && MICROSTEPS > 0, "Invalid step scaling");
constexpr double rockStepRate(Preset p) {
  return double(p.speedDegS) * FULL_STEPS * MICROSTEPS / 360.0;
}
constexpr double spinStepRate(Preset p) {
  return double(p.spinRpm) * FULL_STEPS * MICROSTEPS / 60.0;
}
constexpr bool valid(Preset p) {
  return p.amplitudeDeg > 0 && p.speedDegS > 0 && p.accelDegS2 > 0 && p.cycles > 0 &&
         p.spinRpm > 0 && p.spinAccelDegS2 > 0 && p.spinHoldSeconds >= 0 &&
         rockStepRate(p) <= MAX_STEP_RATE &&
         spinStepRate(p) <= MAX_STEP_RATE;
}
static_assert(valid(PRESETS[0]) && valid(PRESETS[1]) && valid(PRESETS[2]) &&
                  valid(PRESETS[3]) && valid(PRESETS[4]) && valid(PRESETS[5]),
              "Invalid preset or requested pulse rate exceeds MAX_STEP_RATE");
} // namespace cfg

static_assert(cfg::PRESET_COUNT == 6, "Update serial/LED controls for preset count changes");
