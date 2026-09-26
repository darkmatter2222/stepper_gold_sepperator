#pragma once
#include "Config.h"
#include <math.h>
enum class ButtonEvent { None, Short, Long };
class Button {
  bool raw_ = false, stable_ = false, fired_ = false, armed_ = false;
  uint32_t changed_ = 0, pressed_ = 0;

public:
  ButtonEvent update(bool down, uint32_t now) {
    if (down != raw_) {
      raw_ = down;
      changed_ = now;
    }
    // A held button at boot cannot start the machine: require an initial release.
    if (!down && !stable_)
      armed_ = true;
    if (raw_ != stable_ && uint32_t(now - changed_) >= 30) {
      stable_ = raw_;
      if (stable_) {
        pressed_ = now;
        fired_ = false;
      } else {
        if (armed_ && !fired_)
          return ButtonEvent::Short;
        armed_ = true;
      }
    }
    if (armed_ && stable_ && raw_ && !fired_ && uint32_t(now - pressed_) >= 800) {
      fired_ = true;
      return ButtonEvent::Long;
    }
    return ButtonEvent::None;
  }
};
enum class Phase { Idle, Wake, Positive, Negative, Center, Settle, Spin, Rest, Stopping };
inline const char *phaseName(Phase p) {
  switch (p) {
  case Phase::Idle:
    return "IDLE";
  case Phase::Wake:
    return "WAKE";
  case Phase::Positive:
    return "+ANGLE";
  case Phase::Negative:
    return "-ANGLE";
  case Phase::Center:
    return "CENTER";
  case Phase::Settle:
    return "SETTLE";
  case Phase::Spin:
    return "SPIN";
  case Phase::Rest:
    return "REST";
  case Phase::Stopping:
    return "STOPPING";
  }
  return "UNKNOWN";
}
// Motor supplies the AccelStepper interface; fake motor allows host-side tests.
// All changes to speed/acceleration are made at rest, except stop()'s decel target.
template <class Motor> class Controller {
  Motor &m_;
  uint32_t since_ = 0;
  uint8_t cycles_ = 0;
  unsigned selected_ = 0, active_ = 0;
  Phase phase_ = Phase::Idle;
  void phase(Phase p, uint32_t now) {
    phase_ = p;
    since_ = now;
  }
  const cfg::Preset &preset() const { return cfg::PRESETS[active_]; }
  long angle() const { return lroundf(preset().amplitudeDeg * cfg::STEPS_PER_DEGREE); }
  void beginCycle(uint32_t now) {
    active_ = selected_;
    cycles_ = 0;
    m_.setCurrentPosition(0); // New local origin only at rest; prevents long-run overflow.
    m_.setMaxSpeed(preset().speedDegS * cfg::STEPS_PER_DEGREE);
    m_.setAcceleration(preset().accelDegS2 * cfg::STEPS_PER_DEGREE);
    m_.moveTo(angle());
    phase(Phase::Positive, now);
  }
  void idle(uint32_t now) {
    m_.setCurrentPosition(0);
    m_.disableOutputs();
    phase(Phase::Idle, now);
  }

public:
  explicit Controller(Motor &m) : m_(m) {}
  Phase state() const { return phase_; }
  unsigned selected() const { return selected_; }
  unsigned active() const { return active_; }
  bool running() const { return phase_ != Phase::Idle; }
  void select(unsigned n) {
    if (n < cfg::PRESET_COUNT)
      selected_ = n;
  }
  void next() { selected_ = (selected_ + 1) % cfg::PRESET_COUNT; }
  void start(uint32_t now) {
    if (running())
      return;
    m_.setCurrentPosition(0);
    m_.enableOutputs();
    phase(Phase::Wake, now);
  }
  void stop(uint32_t now) {
    if (!running() || phase_ == Phase::Stopping)
      return;
    if (!m_.isRunning()) {
      idle(now);
      return;
    }
    m_.stop();
    phase(Phase::Stopping, now);
  }
  void emergency(uint32_t now) { idle(now); } // Immediate release; rotor may coast.
  void tick(uint32_t now) {
    if (phase_ == Phase::Idle)
      return;
    m_.run();
    if (m_.isRunning())
      return;
    switch (phase_) {
    case Phase::Wake:
      if (uint32_t(now - since_) >= 10)
        beginCycle(now);
      break;
    case Phase::Positive:
      m_.moveTo(-angle());
      phase(Phase::Negative, now);
      break;
    case Phase::Negative:
      if (++cycles_ >= preset().cycles) {
        m_.moveTo(0);
        phase(Phase::Center, now);
      } else {
        m_.moveTo(angle());
        phase(Phase::Positive, now);
      }
      break;
    case Phase::Center:
      phase(Phase::Settle, now);
      break;
    case Phase::Settle:
      if (uint32_t(now - since_) >= preset().settleMs) {
        const float v = preset().spinRpm * 6 * cfg::STEPS_PER_DEGREE;
        const float a = preset().spinAccelDegS2 * cfg::STEPS_PER_DEGREE;
        m_.setMaxSpeed(v);
        m_.setAcceleration(a);
        // Acceleration + requested plateau + deceleration. Hold is NOT total burst time.
        m_.moveTo(lroundf(v * v / a + v * preset().spinHoldSeconds));
        phase(Phase::Spin, now);
      }
      break;
    case Phase::Spin:
      m_.setCurrentPosition(0);
      phase(Phase::Rest, now);
      break;
    case Phase::Rest:
      if (uint32_t(now - since_) >= preset().restMs)
        beginCycle(now);
      break;
    case Phase::Stopping:
      idle(now);
      break;
    default:
      break;
    }
  }
};
