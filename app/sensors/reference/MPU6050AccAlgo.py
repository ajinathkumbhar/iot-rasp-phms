"""
Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
http://www.electronicwings.com
"""
import smbus  # import SMBus module of I2C
from time import sleep  # import
import threading
import Queue

# some MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

qRaw_value = Queue.Queue(maxsize=3)
qProcessed_value = Queue.Queue(maxsize=3)


def is_finger_up_down(sens_val):
	print (
		"is_finger_up_down Ax=%.2f" % sens_val['Ax'], "Ay=%.2f" % sens_val['Ay'],
		"Az=%.2f" % sens_val['Az'])
	acc_x = sens_val['Ax']
	acc_y = sens_val['Ay']
	acc_z = sens_val['Az']
        print acc_x
        if acc_x < -0.25:
        # if -0.10 < acc_y < 0.10 and 0.90 < acc_z < 0.99:
		take_decision()


def detect_gesture():
	# Run algo to detect gesture
	while True:
		if qRaw_value.empty():
			# print ("waiting for raw data... ")
			continue
		sens_val = qRaw_value.get()
		is_finger_up_down(sens_val)
		sleep(0.1)

def take_decision():
	# show result on gesture
	print 'Result : finger UP'


def setup_algo():
	# Create consumer thread
	process_thread = threading.Thread(target=detect_gesture, name='detect_gesture')
	decision_thread = threading.Thread(target=take_decision, name='take_decision')

	process_thread.start()
	decision_thread.start()


def MPU_Init():
	# write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

	# Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

	# Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)

	# Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

	# Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)


def read_raw_data(addr):
	# Accelero and Gyro value are 16-bit
	high = bus.read_byte_data(Device_Address, addr)
	low = bus.read_byte_data(Device_Address, addr + 1)

	# concatenate higher and lower value
	value = ((high << 8) | low)

	# to get signed value from mpu6050
	if (value > 32768):
		value = value - 65536
	return value


bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68  # MPU6050 device address

MPU_Init()
setup_algo()
print (" Reading Data of Gyroscope and Accelerometer")

while True:
	sens_values = {}
	# Read Accelerometer raw value
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)

	# Read Gyroscope raw value
	gyro_x = read_raw_data(GYRO_XOUT_H)
	gyro_y = read_raw_data(GYRO_YOUT_H)
	gyro_z = read_raw_data(GYRO_ZOUT_H)

	# Full scale range +/- 250 degree/C as per sensitivity scale factor
	Ax = acc_x / 16384.0
	Ay = acc_y / 16384.0
	Az = acc_z / 16384.0

	Gx = gyro_x / 131.0
	Gy = gyro_y / 131.0
	Gz = gyro_z / 131.0

	sens_values['Ax'] = acc_x / 16384.0
	sens_values['Ay'] = acc_y / 16384.0
	sens_values['Az'] = acc_z / 16384.0

	sens_values['Gx'] = gyro_x / 131.0
	sens_values['Gy'] = gyro_y / 131.0
	sens_values['Gz'] = gyro_z / 131.0
	# print ("Ax=%.2f" % sens_values['Ax'], "Ay=%.2f" % sens_values['Ay'], "Az=%.2f" % sens_values['Az'])
	# print("Gx=%.2f" % Gx, "Gy=%.2f" % Gy, "Gz=%.2f" % Gz, "Ax=%.2f g" % Ax, "Ay=%.2f g" % Ay, "Az=%.2f g" % Az)
	# print 'Gyro : x={0:2f} y={1:2f} z={2:2f}  --- Acc : x={3:2f} y={4:2f} z={5:2f}'.format(Gx, Gy, Gz, Gx, Gy, Gz)
	qRaw_value.put(sens_values)
