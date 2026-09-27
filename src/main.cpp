#include "Control.h"
#include "Pump.h"
#include <AccelStepper.h>
#include <Arduino.h>
#include <ESP8266WiFi.h>
// Do not initialize outputs from a global constructor before setup can drive EN high.
AccelStepper motor(AccelStepper::DRIVER, cfg::STEP_PIN, cfg::DIR_PIN, 0, 0, false);
Controller<AccelStepper> controller(motor);
Button button;
Pump pump;
void syncPump(uint32_t now) {
  pump.tick(now, controller.state(), controller.active());
  digitalWrite(cfg::PUMP_PIN, pump.on() ? HIGH : LOW);
}
void cancelPump() {
  pump.cancel();
  digitalWrite(cfg::PUMP_PIN, LOW);
}
bool reportPending = true;
void setup() {
  digitalWrite(cfg::PUMP_PIN, LOW);
  pinMode(cfg::PUMP_PIN, OUTPUT); // External 100k base pulldown + 10k gate-source pull-up hold OFF before setup.
  digitalWrite(cfg::ENABLE_PIN, HIGH);
  pinMode(cfg::ENABLE_PIN, OUTPUT);
  digitalWrite(cfg::STEP_PIN, LOW);
  pinMode(cfg::STEP_PIN, OUTPUT);
  digitalWrite(cfg::DIR_PIN, LOW);
  pinMode(cfg::DIR_PIN, OUTPUT);
  pinMode(cfg::BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  // setEnablePin writes HIGH with the default polarity, keeping A4988 off.
  motor.setEnablePin(cfg::ENABLE_PIN);
  motor.setPinsInverted(cfg::INVERT_DIRECTION, false, true); // Active-low A4988 EN.
  motor.setMinPulseWidth(3);
  motor.disableOutputs();
  WiFi.persistent(false);
  WiFi.mode(WIFI_OFF);
  WiFi.forceSleepBegin();
  Serial.begin(115200);
  Serial.println("\nGold separator: IDLE. Tap=mode; hold 0.8s=start/stop.");
  Serial.println("Serial: 1/2/3=mode s=start x=stop !=disable ?=status");
  Serial.println("Water: p=prime 3s c=calibrate 30s (idle only), w=auto toggle; x/! cancel");
}
void loop() {
  const uint32_t now = millis();
  const Phase before = controller.state();
  controller.tick(now);
  auto event = button.update(digitalRead(cfg::BUTTON_PIN) == LOW, now);
  if (event == ButtonEvent::Short) {
    controller.next();
    reportPending = true;
  }
  if (event == ButtonEvent::Long) {
    cancelPump();
    if (controller.running())
      controller.stop(now);
    else
      controller.start(now);
    reportPending = true;
  }
  // Bound serial work per iteration so input flooding cannot starve step generation.
  if (Serial.available()) {
    char ch = Serial.read();
    if (ch >= '1' && ch <= '3')
      controller.select(ch - '1');
    else if (ch == 's') {
      if (!controller.running()) {
        cancelPump();
        controller.start(now);
      }
    } else if (ch == 'x') {
      cancelPump();
      controller.stop(now);
    } else if (ch == '!') {
      cancelPump();
      controller.emergency(now);
    } else if (ch == 'p') {
      pump.dispense(now, cfg::PUMP_PRIME_MS, !controller.running());
    } else if (ch == 'c') {
      pump.dispense(now, cfg::PUMP_CALIBRATE_MS, !controller.running());
    } else if (ch == 'w') {
      pump.setAutomatic(!pump.automatic());
    }
    if (ch != '\r' && ch != '\n')
      reportPending = true;
  }
  const bool previousPump = pump.on();
  syncPump(millis());
  if (pump.on() != previousPump)
    reportPending = true;
  if (controller.state() != before)
    reportPending = true;
  // Defer formatting/transmission until rest; faster strokes need a tight run() cadence.
  if (reportPending && !motor.isRunning() && Serial.availableForWrite() >= 96) {
    char line[96];
    int n = snprintf(line, sizeof(line), "%s selected=%s active=%s water=%s auto=%u manual=%u\n",
                     phaseName(controller.state()), cfg::PRESETS[controller.selected()].name,
                     cfg::PRESETS[controller.active()].name, pump.on() ? "ON" : "OFF",
                     pump.automatic(), pump.manual());
    Serial.write(reinterpret_cast<const uint8_t *>(line), n);
    reportPending = false;
  }
  // 1/2/3 flashes per two seconds show selected mode; active mode is in Serial.
  const uint32_t t = now % 2000;
  const bool flash = t < (controller.selected() + 1) * 300 && t % 300 < 120;
  digitalWrite(LED_BUILTIN, flash ? LOW : HIGH);
  controller.tick(millis());
  syncPump(millis());
  yield(); // ESP8266 watchdog; Wi-Fi disabled to reduce background timing jitter.
}
