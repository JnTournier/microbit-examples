import time
from bluepy import btle
import bluetooth

"""

"""

#Connection to the server on the 6lbr
serverMACAddress = 'B8:27:EB:36:1B:9D'
port = 3
server6lbr = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server6lbr.connect((serverMACAddress, port))
server6lbr.send(b'test')


class MyDelegate(btle.DefaultDelegate):
    def __init__(self, microbit):
        self.serverMicroBit = microbit
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        # if (cHandle == temperature_handle):
        #     # temp = binascii.b2a_hex(data)
        #     temp = ord(data)
        #     # temp2 = int(data.encode('hex'), 8)
        #     print("A notification was received: %s ", temp)
        # else:
        # print("A notification was received: {} ".format(data))
        server6lbr.send(data)
        dataToMicrobit = server6lbr.recv(1024)

        if dataToMicrobit:
            self.serverMicroBit.write(dataToMicrobit)
        

class microbitCollector():
    def __init__(self, device_name, device_mac, sampling_interval_sec=1, retry_interval_sec=5):
        # Prepare the config to connect to the MicroBit device
        self.conn = None
        self.device_name = device_name
        self.device_mac = device_mac
        self._sampling_interval_sec = sampling_interval_sec
        self._retry_interval_sec = retry_interval_sec
        # Connects with re-try mechanism
        self._re_connect()

    def _connect(self):
        print("Connecting...")
        self.conn = btle.Peripheral(self.device_mac, btle.ADDR_TYPE_RANDOM)
        #self.conn.setSecurityLevel("medium")
        print("Connected...")
        self._enable()

    def _enable(self):
        self.svc = self.conn.getServiceByUUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
        self.ch = self.svc.getCharacteristics("6e400002-b5a3-f393-e0a9-e50e24dcca9e")[0]
        self.chwrite = self.svc.getCharacteristics("6e400003-b5a3-f393-e0a9-e50e24dcca9e")[0]

        # Write 0200 to CCCD UUID
        self.ch_cccd = self.ch.getDescriptors("00002902-0000-1000-8000-00805f9b34fb")[0]
        self.ch_cccd.write(b"\x02\x00", True)

        self.conn.setDelegate(MyDelegate(self.chwrite))
        time.sleep(1)
        print("UART notification enabled...")

    def run(self):
        counter = 0
        while True:
            try:
                if self.conn.waitForNotifications(3.0):
                    continue

                # if counter == 10:
                #     print("Counter reaches the max, go send data")
                #     self.chwrite.write(b"17.")
                #     counter = 0

                # print(f'Counter : {counter}')
                # counter += 1
            except Exception as e:
                print(str(e))
                self.conn.disconnect()
                break

        time.sleep(self._retry_interval_sec)
        self._re_connect()

    def _re_connect(self):
        while True:
            try:
                self._connect()
                break
            except Exception as e:
                print(str(e))
                time.sleep(self._retry_interval_sec)

if __name__ == '__main__':
    
    mbc = microbitCollector(device_name="microbit", device_mac="E0:14:9E:14:11:72", sampling_interval_sec=1)
    mbc.run()
    
    while True:
        time.sleep(1000)
        pass
