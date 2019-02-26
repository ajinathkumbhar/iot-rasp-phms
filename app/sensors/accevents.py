"""
Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
http://www.electronicwings.com
"""
import event
import datetime

class AccEvents:
	def __init__(self):
		self.name = "AccEvents"
		self.__last_event = [None,event.GES_EVENT_NONE]

	def get_event_str(self,evt):
		if evt == event.GES_EVENT_FINGER_UP:
			return 'GES_EVENT_FINGER_UP'
		if evt == event.GES_EVENT_FLIP:
			return 'GES_EVENT_FLIP'

	def get_last_event(self):
		return self.__last_event

	def __get_current_time(self):
		currentDT = datetime.datetime.now()
		return currentDT.strftime("%Y-%m-%d %H:%M:%S")

	def detect_gesture_event(self,sens_val,event_queue):
		event_detected = False
		current_time = self.__get_current_time()
		local_event = [current_time,event.GES_EVENT_NONE]
		acc_x = sens_val['Ax']
		acc_y = sens_val['Ay']
		acc_z = sens_val['Az']

		#print ("Ax=%.2f" % acc_x, "Ay=%.2f" % acc_y, "Az=%.2f" % acc_z)

		# Finger up event detection
		if event.FINGER_UP_X_LOW < acc_x < event.FINGER_UP_X_HIGH :
			if event.FINGER_UP_Y_LOW < acc_y < event.FINGER_UP_Y_HIGH \
					and event.FINGER_UP_Z_LOW < acc_z < event.FINGER_UP_Z_HIGH:
					local_event[1] = event.GES_EVENT_FINGER_UP
					event_detected = True

		# Hand flip event detection
		if event.FLIP_X_LOW < acc_x < event.FLIP_X_HIGH:
			if event.FLIP_Y_LOW < acc_y < event.FLIP_Y_HIGH \
					and event.FLIP_Z_LOW < acc_z < event.FLIP_Z_HIGH:
					local_event[1] = event.GES_EVENT_FLIP
					event_detected = True

		if event_detected and not event_queue.full():
			self.__last_event = local_event
			event_queue.put(local_event)


