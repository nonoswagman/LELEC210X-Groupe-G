# -*- coding: utf-8 -*-
"""
uart-reader.py 
ELEC PROJECT - 210x
"""
import argparse
import serial
from   serial.tools import list_ports
import time
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

PRINT_PREFIX = "SND:HEX:"
FREQ_SAMPLING = 10200
VAL_MAX_ADC = 4096
VDD = 3.3

def parse_buffer(line):
    line = line.strip()
    if line.startswith(PRINT_PREFIX):
        return bytes.fromhex(line[len(PRINT_PREFIX):])
    else:
        print(line)
        return None
    
def reader(port=None):
    ser = serial.Serial(port=port,baudrate=115200)
    while True:
        line = ""
        while not line.endswith('\n'):
            line += ser.read_until(b'\n', size=1042).decode("ascii")
        line = line.strip()
        buffer = parse_buffer(line)
        if buffer is not None:
            dt = np.dtype(np.uint16)
            dt = dt.newbyteorder('<')
            buffer_array = np.frombuffer(buffer, dtype=dt)
            
            yield buffer_array
            
def generate_audio(buf, file_name):
    buf = np.asarray(buf, dtype=np.float64)
    buf = buf - np.mean(buf)
    buf /= max(abs(buf))
    sf.write("audio_files/" + file_name + '.ogg', buf, FREQ_SAMPLING)
    
        
if __name__ == '__main__':
    
    # argParser = argparse.ArgumentParser()
    # argParser.add_argument("-p", "--port", help="Port for serial communication")
    # args = argParser.parse_args()
    por="COM5"
    print('uart-reader launched...\n')

    if por is None:
        print("No port specified, here is a list of serial communication port available")
        print("================")
        port = list(list_ports.comports())
        for p in port:
            print(p.device)
        print("================")
        print("Launch this script with [-p PORT_REF] to access the communication port")
    
    else:
    
        plt.figure(figsize=(10,5))
        input_stream = reader(port=por)
        msg_counter = 0
        
        for msg in input_stream:
            print('Acquisition #{}'.format(msg_counter))
            
            buffer_size = len(msg)
            times = np.linspace(0, buffer_size-1, buffer_size)*1/FREQ_SAMPLING
            voltage_mV = msg*VDD/VAL_MAX_ADC*1e3
            
            fig,ax=plt.subplots(1,2)
            ax[0].plot(times, voltage_mV)
            ax[1].plot(np.fft.fftfreq(len(voltage_mV),1/FREQ_SAMPLING),np.fft.fft(voltage_mV))
            
            plt.title('Acquisition #{}'.format(msg_counter))
            #ax[0].xlabel('Time (s)')
            #ax[0].ylabel('Voltage (mV)')
            #ax[0].ylim([0,3300])
            ax[0].draw()
            ax[0].pause(0.001)
            ax[0].cla()
            
            
            
            generate_audio(msg, 'acq-{}'.format(msg_counter))
            
            msg_counter+=1
