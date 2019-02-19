

# SensData class to collect all sensors data in
# in single object
class SensData:
    def __init__(self):
        self.clear()
    def clear(self):
        self.temp = 0
        self.humi = 0
        self.Gx = 0
        self.Gy = 0
        self.Gz = 0
        self.Ax = 0
        self.Ay = 0
        self.Az = 0
        self.hbeat = 0
    def getTemp(self):
        return self.temp
    def getHumidity(self):
        return self.humi
    def getGyroCoordinate(self):
        return self.Gx, self.Gy, self.Gz
    def getAccCoordinate(self):
        return self.Ax, self.Ay, self.Az
    def dump(self):
        print 'temperature : ' + str(self.temp)
        print 'humidity    : ' + str(self.humi)
        print 'Gx          : ' + str(self.Gx)
        print 'Gy          : ' + str(self.Gy)
        print 'Gz          : ' + str(self.Gz)
        print 'Ax          : ' + str(self.Ax)
        print 'Ay          : ' + str(self.Ay)
        print 'Az          : ' + str(self.Az)
        print 'Pulses      : ' + str(self.hbeat)
