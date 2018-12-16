

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
        return self.Gx, Self.Gy, Self.Gz
    def getAccCoordinate(self):
        return self.Ax, Self.Ay, Self.Az
    def dump(self):
        print 'temperature : ' + str(temp)
        print 'humidity    : ' + str(humi)
        print 'Gx          : ' + str(Gx)
        print 'Gy          : ' + str(Gy)
        print 'Gz          : ' + str(Gz)
        print 'Ax          : ' + str(Ax)
        print 'Ay          : ' + str(Ay)
        print 'Az          : ' + str(Az)
        print 'Pulses      : ' + str(hbeat)
