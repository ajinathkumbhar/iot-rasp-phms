"""
Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
http://www.electronicwings.com
"""
import event


class AccEvents:
	def __init__(self):
		self.name = "AccEvents"

	def get_event_str(self,evt):
		if evt == event.GES_EVENT_FINGER_UP:
			return 'GES_EVENT_FINGER_UP'
		if evt == event.GES_EVENT_FLIP:
			return 'GES_EVENT_FLIP'

	def detect_gesture_event(self,sens_val,event_queue):
		acc_x = sens_val['Ax']
		acc_y = sens_val['Ay']
		acc_z = sens_val['Az']

		#print ("Ax=%.2f" % acc_x, "Ay=%.2f" % acc_y, "Az=%.2f" % acc_z)

		# Finger up event detection
		if event.FINGER_UP_X_LOW < acc_x < event.FINGER_UP_X_HIGH :
			if event.FINGER_UP_Y_LOW < acc_y < event.FINGER_UP_Y_HIGH \
					and event.FINGER_UP_Z_LOW < acc_z < event.FINGER_UP_Z_HIGH:
				#print 'GES_EVENT_FINGER_UP'
				if not event_queue.full():
					event_queue.put(event.GES_EVENT_FINGER_UP)

		# Hand flip event detection
		if event.FLIP_X_LOW < acc_x < event.FLIP_X_HIGH:
			if event.FLIP_Y_LOW < acc_y < event.FLIP_Y_HIGH \
					and event.FLIP_Z_LOW < acc_z < event.FLIP_Z_HIGH:
				#print 'GES_EVENT_FLIP'
				if not event_queue.full():
					event_queue.put(event.GES_EVENT_FLIP)

