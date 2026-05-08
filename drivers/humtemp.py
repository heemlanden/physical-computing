

'''
AHT20, AHT21 (humidity and temperature sensors)
MicroPython driver for micro:bit AANGEPAST NAAR MACHINE MODULE

CREDIT for CRC calculation:
    SOURCE: AHT30 Datasheet, 3.CRCcheck, page 11.
    Function: unsigned char Calc_CRC8()
    Translated from C++
    to MicroPython for the micro:bit.

AUTHOR: fredscave.com
DATE  : 2024/11
VERSION : 1.00
'''


from micropython import const

from machine import I2C, Pin
import time

# You must choose the correct pins for your board:


ADDR = const(0x38)
CMD_INIT = [0xBE, 0x08, 0x00]
CMD_MEASURE = [0xAC, 0x33, 0x00]
CMD_RESET = const(0xBA)
CRC_INIT = const(0xFF)
CRC_POLY = const(0x31)

class AHT20():
    def __init__(self, scl, sda, addr=ADDR):
        self.i2c = I2C(0, scl=scl, sda=sda, freq=100000)  # Example for ESP32
        self.sleep = time.sleep_ms
        self.sleep(100)
        self.addr = addr
        self.IsChecksum = False
        self.Initialise()
        self.sleep(10)
        self.IsCalibrated = self.Read_Status() & 0b00001000

    def Initialise(self):
        self.i2c.writeto(self.addr, bytearray(CMD_INIT))

    def Read_Status(self):
        buf = self.i2c.readfrom(self.addr, 1)
        return buf[0]

    def Is_Calibrated(self):
        return bool(self.IsCalibrated)

    def Is_Checksum(self):
        return self.IsChecksum

    def Read(self):
        self.i2c.writeto(self.addr, bytearray(CMD_MEASURE))
        self.sleep(80)
        busy = True
        while busy:
            #buf = self.i2c.readfrom(self.addr, 1)
            self.sleep(10)
            busy = self.Read_Status() & 0b10000000
        buf = self.i2c.readfrom(self.addr, 7)
        measurements = self._Convert(buf)
        return measurements

    def T(self):
        measurements = self.Read()
        return round(measurements[1], 1)

    def RH(self):
        measurements = self.Read()
        return int(measurements[0] + 0.5)

    def Reset(self):
        self.i2c.writeto(self.addr, bytes([CMD_RESET]))
        self.sleep(20)

    def _Convert(self, buf):
        RawRH = ((buf[1] << 16) |( buf[2] << 8) | buf[3]) >> 4
        RH = RawRH * 100 / 0x100000
        RawT = ((buf[3] & 0x0F) << 16) | (buf[4] << 8) | buf[5]
        T = ((RawT * 200) / 0x100000) - 50
        self.IsChecksum = self._Compare_Checksum(buf)
        return (RH, T, self.IsChecksum)

    def _Compare_Checksum(self, buf):
        check = bytearray(1)
        check[0] = CRC_INIT
        for byte in buf[:6]:
            check[0] ^= byte
            for x in range(8):
                if check[0] & 0b10000000:
                    check[0] = (check[0] << 1) ^ CRC_POLY
                else:
                    check[0] = check[0]<< 1
        return check[0] == buf[6]
    
def test():
    aht = AHT20()
    aht.Initialise()
    print(aht.Read())
    print(aht.T())
    
def cont_test():
    aht = AHT20()
    aht.Initialise()
    while True:
        print(aht.Read())
        print(aht.T())
        time.sleep_ms(100)

