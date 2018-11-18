import time
from mpu6050 import mpu6050


sensor = mpu6050(0x68)
print sensor

while True:
    accelerometer_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    print 'Gyro X=' + str(gyro_data['x']),
    print 'Gyro Y=' + str(gyro_data['y']),
    print 'Gyro Z=' + str(gyro_data['x']),
    print 'Acc  X=' + str(accelerometer_data['y']),
    print 'Acc  Y=' + str(accelerometer_data['x']),
    print 'Acc  Z=' + str(accelerometer_data['y'])
    time.sleep(1)





