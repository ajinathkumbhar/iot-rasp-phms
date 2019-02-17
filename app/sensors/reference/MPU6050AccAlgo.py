"""
Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
http://www.electronicwings.com
"""
import smbus  # import SMBus module of I2C
from time import sleep  # import
import threading
from enum import Enum
import  Queue
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
qGesture_event = Queue.Queue(maxsize=3)

GES_EVENT_FINGER_UP = 0x01
GES_EVENT_FINGER_UP_DOWN = 0x02
GES_EVENT_LEFT_TURN = 0x03
GES_EVENT_LEFT_FLIP = 0x04
GES_EVENT_RIGHT_TURN = 0x05
GES_EVENT_RIGHT_FLIP = 0x06

FINGER_UP_X_LOW  = -1.0
FINGER_UP_X_HIGH = -0.30
FINGER_UP_Y_LOW = -0.20
FINGER_UP_Y_HIGH = 0.20
FINGER_UP_Z_LOW = 0.95
FINGER_UP_Z_HIGH = 1.0

FLIP_X_LOW  = -0.30
FLIP_X_HIGH = 0
FLIP_Y_LOW = -0.10
FLIP_Y_HIGH = 0.30
FLIP_Z_LOW = -1.0
FLIP_Z_HIGH = 0.95

def detect_gesture_event(sens_val):
	# print (
	# 	"is_finger_up_down test 1.0 Ax=%.2f" % sens_val['Ax'], "Ay=%.2f" % sens_val['Ay'],
	# 	"Az=%.2f" % sens_val['Az'])
	acc_x = sens_val['Ax']
	acc_y = sens_val['Ay']
	acc_z = sens_val['Az']
	if FINGER_UP_X_LOW < acc_x < FINGER_UP_X_HIGH :
		if FINGER_UP_Y_LOW < acc_y < FINGER_UP_Y_HIGH \
				and FINGER_UP_Z_LOW < acc_z < FINGER_UP_Z_HIGH:
			print 'GES_EVENT_FINGER_UP'

	if FLIP_X_LOW < acc_x < FLIP_X_HIGH:
		if FLIP_Y_LOW < acc_y < FLIP_Y_HIGH \
				and FLIP_Z_LOW < acc_z < FLIP_Z_HIGH:
			print 'GES_EVENT_FLIP'
			#qGesture_event.put(GES_EVENT_FINGER_UP)

# def is_finger_up_down():


def detect_gesture():
	# Run algo to detect gesture
	while True:
		if qRaw_value.empty():
			# print ("waiting for raw data... ")
			continue

		detect_gesture_event(qRaw_value.get())
		# while True:
		# sens_val = qRaw_value.get()
		# print (
		# 	"is_finger_up_down Ax=%.2f" % sens_val['Ax'], "Ay=%.2f" % sens_val['Ay'],
		# 	"Az=%.2f" % sens_val['Az'])
		# acc_x = sens_val['Ax']
		# acc_y = sens_val['Ay']
		# acc_z = sens_val['Az']
		# print acc_x
		#
		# if acc_x < -0.40:
		# 	print 'GES_EVENT_FINGER_UP'
		# 	qGesture_event.put(GES_EVENT_FINGER_UP)



def setup_algo():
	# Create consumer thread
	detect_gesture_thread = threading.Thread(target=detect_gesture, name='detect_gesture')
	detect_gesture_thread.start()


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
	sleep(0.1)
