from mcp3208 import MCP3208
import time

adc = MCP3208()

while True:
        for i in range(8):
                print('ADC[{}]: {:.2f}'.format(i, adc.read(i)))
        time.sleep(0.5)
