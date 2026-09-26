#include "Control.h"
#include <unity.h>
struct Motor {
  long pos = 0, target = 0;
  float speed = 0, accel = 0;
  bool enabled = false;
  void setCurrentPosition(long p) { pos = target = p; }
  void setMaxSpeed(float v) { speed = v; }
  void setAcceleration(float a) { accel = a; }
  void moveTo(long p) { target = p; }
  bool isRunning() { return pos != target; }
  void run() {
    if (pos < target)
      ++pos;
    else if (pos > target)
      --pos;
  }
  void enableOutputs() { enabled = true; }
  void disableOutputs() { enabled = false; }
  void stop() { target = pos + (target > pos ? 2 : -2); }
};
void setUp() {}
void tearDown() {}
void boot_idle() {
  Motor m;
  Controller<Motor> c(m);
  for (unsigned t = 0; t < 10000; t++)
    c.tick(t);
  TEST_ASSERT_FALSE(m.enabled);
  TEST_ASSERT_EQUAL(0, m.pos);
}
void sequence_and_queue() {
  Motor m;
  Controller<Motor> c(m);
  uint32_t t = 0;
  c.start(t);
  c.tick(9);
  TEST_ASSERT_EQUAL_INT((int)Phase::Wake, (int)c.state());
  c.tick(10);
  t = 10;
  TEST_ASSERT_EQUAL(44, m.target);
  c.select(2); // Must keep LOW through complete cycle.
  unsigned neg = 0;
  Phase old = c.state();
  while (c.state() != Phase::Spin && t < 30000) {
    c.tick(++t);
    if (c.state() == Phase::Negative && old != c.state())
      ++neg;
    old = c.state();
  }
  TEST_ASSERT_EQUAL(6, neg);
  TEST_ASSERT_EQUAL(0, c.active());
  const float v = 10 * 6 * cfg::STEPS_PER_DEGREE, a = 120 * cfg::STEPS_PER_DEGREE;
  TEST_ASSERT_EQUAL(lroundf(v * v / a + v), m.target);
  while (c.state() != Phase::Rest && t < 40000)
    c.tick(++t);
  TEST_ASSERT_EQUAL(0, m.pos);
  t += 2000;
  c.tick(t);
  TEST_ASSERT_EQUAL(2, c.active());
  TEST_ASSERT_EQUAL(133, m.target);
}
void stop_and_disable() {
  Motor m;
  Controller<Motor> c(m);
  c.start(0);
  c.tick(10);
  c.tick(11);
  c.stop(12);
  TEST_ASSERT_TRUE(m.enabled);
  c.tick(13);
  c.tick(14);
  TEST_ASSERT_FALSE(m.enabled);
  TEST_ASSERT_FALSE(c.running());
  c.start(20);
  c.tick(30);
  c.emergency(31);
  TEST_ASSERT_FALSE(m.enabled);
  TEST_ASSERT_EQUAL(m.pos, m.target);
}
void stop_every_phase() {
  for (int p = 1; p <= 7; p++) {
    Motor m;
    Controller<Motor> c(m);
    c.start(0);
    uint32_t t = 0;
    while ((int)c.state() != p && t < 30000)
      c.tick(++t);
    TEST_ASSERT_EQUAL(p, (int)c.state());
    c.stop(t);
    for (unsigned k = 0; k < 10; k++)
      c.tick(++t);
    TEST_ASSERT_FALSE(c.running());
    TEST_ASSERT_FALSE(m.enabled);
  }
}
void button_click_long() {
  Button b;
  b.update(false, 0);
  b.update(true, 10);
  TEST_ASSERT_EQUAL_INT(0, (int)b.update(true, 40));
  b.update(false, 100);
  TEST_ASSERT_EQUAL_INT((int)ButtonEvent::Short, (int)b.update(false, 130));
  b.update(true, 200);
  b.update(true, 230);
  TEST_ASSERT_EQUAL_INT((int)ButtonEvent::Long, (int)b.update(true, 1030));
  TEST_ASSERT_EQUAL_INT(0, (int)b.update(true, 2030));
  b.update(false, 2040);
  TEST_ASSERT_EQUAL_INT(0, (int)b.update(false, 2070));
}
void boot_held() {
  Button b;
  for (uint32_t t = 0; t < 2000; t += 10)
    TEST_ASSERT_EQUAL_INT(0, (int)b.update(true, t));
  b.update(false, 2000);
  TEST_ASSERT_EQUAL_INT(0, (int)b.update(false, 2030));
}
void bounce_and_wrap() {
  Button b;
  uint32_t t = 0xffffff00u;
  b.update(false, t);
  b.update(true, t + 1);
  b.update(false, t + 5);
  b.update(true, t + 10);
  TEST_ASSERT_EQUAL_INT(0, (int)b.update(true, t + 20));
  b.update(true, t + 40);
  TEST_ASSERT_EQUAL_INT((int)ButtonEvent::Long, (int)b.update(true, t + 840));
  Motor m;
  Controller<Motor> c(m);
  c.start(0xfffffffbu);
  c.tick(6);
  TEST_ASSERT_EQUAL_INT((int)Phase::Positive, (int)c.state());
}
void thousands_of_batches() {
  Motor m;
  Controller<Motor> c(m);
  c.start(0);
  uint32_t t = 0;
  unsigned rests = 0;
  Phase old = c.state();
  while (rests < 1000 && t < 20000000) {
    c.tick(++t);
    if (c.state() == Phase::Rest && old != c.state()) {
      ++rests;
      TEST_ASSERT_EQUAL(0, m.pos);
    }
    old = c.state();
  }
  TEST_ASSERT_EQUAL(1000, rests);
}
int main() {
  UNITY_BEGIN();
  RUN_TEST(boot_idle);
  RUN_TEST(sequence_and_queue);
  RUN_TEST(stop_and_disable);
  RUN_TEST(stop_every_phase);
  RUN_TEST(button_click_long);
  RUN_TEST(boot_held);
  RUN_TEST(bounce_and_wrap);
  RUN_TEST(thousands_of_batches);
  return UNITY_END();
}
