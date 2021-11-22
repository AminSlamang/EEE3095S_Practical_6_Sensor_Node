# EEE3095S Practical 6 - IoT Application
# Pi 1 - Sensor
# KTNRIO001 - Rio Katundulu
# SLMAMI010 - Amin Slamang

import socket
import time
import threading
from datetime import datetime
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# TCP socket setup.
def main():
    global HOST, PORT, s, chan1, chan2,sample, lastSample
    HOST = '192.168.137.162'
    PORT = 10000
    sample = False
    lastSample  = 'XX:XX:XX'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # ADC setup.
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO,MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D5)
    mcp = MCP.MCP3008(spi, cs)
    chan2 = AnalogIn(mcp, MCP.P2)
    chan1 = AnalogIn(mcp, MCP.P1)
    sampling()

    # Reading Server commands and acting on them.
    while(True):
        server_command = s.recv(1024)
        server_command = server_command.decode("utf-8")
        code = server_command[0]
        if(server_command != ""):
            if(code  == "0"):
                cmmd = server_command[2:]
                if (cmmd == "on"):
                    sample = True
                elif(cmmd == "off"):
                    sample = False
            elif(code  == "1"):
                mssg = "S,<pre><br> Status      : " + ("Sampling" if sample else "Not sampling") + "<br> Last sample : "+ lastSample + "</pre>"
                s.sendall(mssg.encode())
            elif(code =="X"):
                sample = False        
        time.sleep(5)

# If sampling, samples and sends data to server, else does nothing.
def sampling():
    global lastSample, s,sample
    thread = threading.Timer(10, sampling)
    thread.daemon = True
    thread.start()
    if(sample):
        data = ("D{};{}".format(str(chan1.value),str(chan2.value)))
        s.sendall(data.encode())   
        lastSample = str(datetime.now().time())[0:8]



if __name__ == "__main__":
    main()