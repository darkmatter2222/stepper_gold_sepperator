#pragma once
#include "Control.h"
// Full-voltage ON/OFF bursts, not high-frequency PWM or calibrated volumetric dosing.
class Pump {
  bool automatic_ = cfg::PUMP_AUTO_DEFAULT, manual_ = false, output_ = false;
  bool eligible_ = false;
  unsigned profile_ = 0;
  uint32_t changed_ = 0, manualStarted_ = 0, manualDuration_ = 0;

public:
  bool on() const { return output_; }
  bool manual() const { return manual_; }
  bool automatic() const { return automatic_; }
  void cancel() {
    manual_ = false;
    output_ = false;
    eligible_ = false;
  }
  void setAutomatic(bool enable) {
    automatic_ = enable;
    cancel();
  }
  bool dispense(uint32_t now, uint32_t durationMs, bool machineIdle) {
    // Repeated serial characters cannot extend a running manual dose.
    if (!machineIdle || manual_ || durationMs == 0 || durationMs > cfg::PUMP_CALIBRATE_MS)
      return false;
    manual_ = true;
    output_ = true;
    eligible_ = false;
    manualStarted_ = now;
    manualDuration_ = durationMs;
    return true;
  }
  void tick(uint32_t now, Phase phase, unsigned active) {
    if (manual_) {
      if (phase != Phase::Idle || uint32_t(now - manualStarted_) >= manualDuration_)
        cancel();
      else {
        output_ = true;
        return;
      }
    }
    const bool allowed = phase == Phase::Positive || phase == Phase::Negative ||
                         (cfg::PUMP_DURING_SPIN && phase == Phase::Spin);
    if (!automatic_ || !allowed || active >= cfg::PRESET_COUNT) {
      output_ = false;
      eligible_ = false;
      return;
    }
    if (!eligible_ || active != profile_) {
      eligible_ = true;
      profile_ = active;
      changed_ = now;
      output_ = true;
      return;
    }
    const auto &schedule = cfg::PUMP_SCHEDULE[profile_];
    const uint32_t interval = output_ ? schedule.onMs : schedule.offMs;
    if (uint32_t(now - changed_) >= interval) {
      output_ = !output_;
      changed_ = now; // Never catch up missed doses after a delayed loop.
    }
  }
};
