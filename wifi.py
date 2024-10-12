import network
import time

time.sleep(1)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('ShArVa', 'end dirt people main zero')

time.sleep(1) # better would be a callback somewhere
print('wifi connected')
