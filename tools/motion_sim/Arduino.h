#pragma once
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <algorithm>
using std::min;
using std::max;
using boolean = bool;
constexpr int HIGH=1, LOW=0, OUTPUT=1;
extern unsigned long simulatedMicros;
inline unsigned long micros() { return simulatedMicros; }
inline void pinMode(int, int) {}
inline void digitalWrite(int, int) {}
inline void delayMicroseconds(unsigned int us) { simulatedMicros += us; }
inline void yield() {}
template <typename T> inline T constrain(T x, T low, T high) { return min(max(x,low),high); }
