// Compile against the pinned real AccelStepper 1.64 source, with fake clock/GPIO.
// Tests commanded timing only; no torque, CPU cost, interrupt or fluid model.
#include <AccelStepper.h>
#include "Control.h"
#include <cassert>
#include <cstdio>
unsigned long simulatedMicros=0;
int main() {
  for (unsigned mode=0; mode<cfg::PRESET_COUNT; ++mode) {
    simulatedMicros=0;
    AccelStepper motor(AccelStepper::DRIVER, 14, 12);
    motor.setMinPulseWidth(3);
    Controller<AccelStepper> controller(motor);
    controller.select(mode);
    controller.start(0);
    Phase before=controller.state();
    unsigned long positiveAt=0, spinAt=0, agitationAt=0, agitationEnd=0;
    double periodSum=0;
    unsigned periods=0, positiveEntries=0;
    float peakSpin=0;
    while (controller.state()!=Phase::Rest && simulatedMicros<30000000) {
      simulatedMicros+=5;
      controller.tick(simulatedMicros/1000);
      auto phase=controller.state();
      if (phase==Phase::Positive && before!=phase) {
        if (!agitationAt) agitationAt=simulatedMicros;
        if (++positiveEntries > 2) { periodSum+=(simulatedMicros-positiveAt)/1e6; ++periods; }
        positiveAt=simulatedMicros;
      }
      if (phase==Phase::Settle && before!=phase) agitationEnd=simulatedMicros;
      if (phase==Phase::Spin) {
        if (before!=phase) spinAt=simulatedMicros;
        peakSpin=std::max(peakSpin, motor.speed());
      }
      before=phase;
    }
    assert(controller.state()==Phase::Rest && periods>5);
    // Compare recurring positive-target transitions against full-cycle timing.
    const auto &p=cfg::PRESETS[mode];
    const double travel=2*p.amplitudeDeg;
    const double expectedPeriod=travel <= p.speedDegS*p.speedDegS/p.accelDegS2
        ? 4*sqrt(travel/p.accelDegS2)
        : 2*(travel/p.speedDegS+p.speedDegS/p.accelDegS2);
    const double measuredPeriod=periodSum/periods;
    assert(fabs(measuredPeriod-expectedPeriod)<0.05);
    const double expectedSpin=2*p.spinRpm*6/p.spinAccelDegS2+p.spinHoldSeconds;
    const double measuredSpin=(simulatedMicros-spinAt)/1e6;
    assert(fabs(measuredSpin-expectedSpin)<0.05);
    assert(fabs(peakSpin/(6*cfg::STEPS_PER_DEGREE)-p.spinRpm)<0.2);
    const double agitation=(agitationEnd-agitationAt)/1e6;
    assert(agitation>7.5 && agitation<11.0);
    assert(positiveEntries==p.cycles);
    printf("%s: %.3f Hz, agitation %.3f s, spin %.3f s, peak %.2f RPM\n",p.name,1/measuredPeriod,agitation,measuredSpin,peakSpin/(6*cfg::STEPS_PER_DEGREE));
  }
}
