#include "Pump.h"
#include <initializer_list>
#include <unity.h>
void setUp() {}
void tearDown() {}
void off_at_boot_and_pauses() {
  Pump p;
  for (auto phase : {Phase::Idle, Phase::Wake, Phase::Center, Phase::Settle, Phase::Spin,
                     Phase::Rest, Phase::Stopping}) {
    p.tick(0, phase, 0);
    TEST_ASSERT_FALSE(p.on());
  }
}
void timing_across_reversals() {
  Pump p;
  p.tick(0, Phase::Positive, 0);
  TEST_ASSERT_TRUE(p.on());
  p.tick(499, Phase::Negative, 0);
  TEST_ASSERT_TRUE(p.on());
  p.tick(500, Phase::Positive, 0);
  TEST_ASSERT_FALSE(p.on());
  p.tick(4999, Phase::Negative, 0);
  TEST_ASSERT_FALSE(p.on());
  p.tick(5000, Phase::Positive, 0);
  TEST_ASSERT_TRUE(p.on());
  p.tick(5100, Phase::Settle, 0);
  TEST_ASSERT_FALSE(p.on());
}
void mode_and_stop() {
  Pump p;
  p.tick(0, Phase::Positive, 2);
  p.tick(999, Phase::Negative, 2);
  TEST_ASSERT_TRUE(p.on());
  p.tick(1000, Phase::Negative, 2);
  TEST_ASSERT_FALSE(p.on());
  p.tick(1100, Phase::Positive, 1);
  TEST_ASSERT_TRUE(p.on());
  p.tick(1150, Phase::Stopping, 1);
  TEST_ASSERT_FALSE(p.on());
  p.tick(1160, Phase::Idle, 1);
  TEST_ASSERT_FALSE(p.on());
}
void manual_timeout_and_no_extension() {
  Pump p;
  TEST_ASSERT_TRUE(p.dispense(10, 3000, true));
  TEST_ASSERT_FALSE(p.dispense(100, 30000, true));
  p.tick(3009, Phase::Idle, 0);
  TEST_ASSERT_TRUE(p.on());
  p.tick(3010, Phase::Idle, 0);
  TEST_ASSERT_FALSE(p.on());
  TEST_ASSERT_FALSE(p.manual());
  TEST_ASSERT_FALSE(p.dispense(4000, 3000, false));
  TEST_ASSERT_FALSE(p.dispense(4000, 30001, true));
}
void calibration_cancel_and_start() {
  Pump p;
  TEST_ASSERT_TRUE(p.dispense(0, 30000, true));
  p.tick(29999, Phase::Idle, 0);
  TEST_ASSERT_TRUE(p.on());
  p.tick(30000, Phase::Idle, 0);
  TEST_ASSERT_FALSE(p.on());
  p.dispense(31000, 3000, true);
  p.cancel();
  TEST_ASSERT_FALSE(p.on());
  p.dispense(32000, 3000, true);
  p.tick(32001, Phase::Wake, 0);
  TEST_ASSERT_FALSE(p.on());
  TEST_ASSERT_FALSE(p.manual());
}
void auto_toggle_and_rollover() {
  Pump p;
  p.setAutomatic(false);
  p.tick(0, Phase::Positive, 0);
  TEST_ASSERT_FALSE(p.on());
  TEST_ASSERT_TRUE(p.dispense(0xffffff00u, 3000, true));
  p.tick(uint32_t(0xffffff00u + 3000), Phase::Idle, 0);
  TEST_ASSERT_FALSE(p.on());
  p.setAutomatic(true);
  p.tick(0xffffff00u, Phase::Positive, 0);
  p.tick(uint32_t(0xffffff00u + 500), Phase::Negative, 0);
  TEST_ASSERT_FALSE(p.on());
  p.tick(uint32_t(0xffffff00u + 5000), Phase::Positive, 0);
  TEST_ASSERT_TRUE(p.on());
}
void no_delayed_catchup() {
  Pump p;
  p.tick(0, Phase::Positive, 0);
  p.tick(60000, Phase::Negative, 0);
  TEST_ASSERT_FALSE(p.on());
  p.tick(60001, Phase::Positive, 0);
  TEST_ASSERT_FALSE(p.on());
  p.tick(64500, Phase::Negative, 0);
  TEST_ASSERT_TRUE(p.on());
}
int main() {
  UNITY_BEGIN();
  RUN_TEST(off_at_boot_and_pauses);
  RUN_TEST(timing_across_reversals);
  RUN_TEST(mode_and_stop);
  RUN_TEST(manual_timeout_and_no_extension);
  RUN_TEST(calibration_cancel_and_start);
  RUN_TEST(auto_toggle_and_rollover);
  RUN_TEST(no_delayed_catchup);
  return UNITY_END();
}
