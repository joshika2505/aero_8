#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

void setup() {

  Serial.begin(115200);

  if (!mpu.begin()) {
    Serial.println("MPU6050 NOT FOUND");
    while (1);
  }

  Serial.println("MPU6050 READY");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  delay(100);
}

void loop() {

  sensors_event_t a, g, temp;

  mpu.getEvent(&a, &g, &temp);

  Serial.print(a.acceleration.x);
  Serial.print(",");

  Serial.print(a.acceleration.y);
  Serial.print(",");

  Serial.print(a.acceleration.z);
  Serial.print(",");

  Serial.print(g.gyro.x);
  Serial.print(",");

  Serial.print(g.gyro.y);
  Serial.print(",");

  Serial.print(g.gyro.z);
  Serial.print(",");

  Serial.println(temp.temperature);

  delay(100);
}