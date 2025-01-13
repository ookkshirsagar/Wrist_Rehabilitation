#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# Author: Ryu Woon Jung (Leon)

#
# *********     Read and Write Example      *********
#
#
# Available Dynamixel model on this example : All models using Protocol 2.0
# This example is designed for using a Dynamixel PRO 54-200, and an USB2DYNAMIXEL.
# To use another Dynamixel model, such as X series, see their details in E-Manual(emanual.robotis.com) and edit below variables yourself.
# Be sure that Dynamixel PRO properties are already set as %% ID : 1 / Baudnum : 1 (Baudrate : 57600)
#

import os
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
from datetime import datetime

from dynamixel_sdk import *                    # Uses Dynamixel SDK library
from dynamixel_sdk.port_handler import PortHandler
from dynamixel_sdk.packet_handler import PacketHandler
from dynamixel_sdk.robotis_def import *

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()        
    print("Bye!")
    sys.exit()

def storeData():
    np.savetxt('data/versuch6/torque',valuesf,delimiter=",")
    np.savetxt('data/versuch6/vel',vel,delimiter=",")
    np.savetxt('data/versuch6/pwm',pwm,delimiter=",")
    np.savetxt('data/versuch6/pos',pos,delimiter=",")
    np.savetxt('data/versuch6/current',current,delimiter=",")

def plotdata():
    ll=len(timevec)-1
    plt.plot(timevec[0:ll],valuesf[0:ll])
    plt.plot(timevec[0:ll],vel[0:ll])
    plt.plot(timevec[0:ll],pwm[0:ll])
    plt.plot(timevec[0:ll],current[0:ll])
    plt.plot(timevec[0:ll],pos[0:ll])
    plt.show()

def filter(newdata):
    if abs(newdata + hx.get_offset_A()/467000)<0.00001:#for checking if they are equal
       f=vals.copy()
       vals[0]=vals[1]
       vals[1]=vals[2]
       vals[2]=vals[3]
       vals[3]=vals[4]
       vals[4]=np.median(f)
       return np.median(f)
    elif newdata > 4.0:
       f=vals.copy()
       vals[0]=vals[1]
       vals[1]=vals[2]
       vals[2]=vals[3]
       vals[3]=vals[4]
       vals[4]=np.median(f)
       return np.median(f)
    elif newdata < -4.0:
       f=vals.copy()
       vals[0]=vals[1]
       vals[1]=vals[2]
       vals[2]=vals[3]
       vals[3]=vals[4]
       vals[4]=np.median(f)
       return np.median(f)

    vals[0]=vals[1]
    vals[1]=vals[2]
    vals[2]=vals[3]
    vals[3]=vals[4]
    vals[4]=newdata
    f=vals.copy()
    return np.median(f)






if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch




# Control table address
ADDR_TORQUE_ENABLE        = 64               # Control table address is different in Dynamixel model
ADDR_GOAL_POSITION        = 116
ADDR_PRESENT_POSITION     = 132
ADDR_PRESENT_CURRENT      = 126
ADDR_GOAL_PWM             = 100
ADDR_GOAL_CURRENT         = 102
ADDR_PRESENT_VELOCITY     = 128
ADDR_GOAL_VELOCITY        = 104
ADDR_OPERATING_MODE       = 11
ADDR_PROFILE_VELOCITY     = 112
ADDR_PROFILE_ACCELERATION = 108
ADDR_PRESENT_PWM          = 124

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID_T                      = 1                 # Dynamixel ID : 1
DXL_ID_P                      = 2
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME_P                  = '/dev/ttyUSB1'         # Check which port is being used on your controller
DEVICENAME_T                  = '/dev/ttyUSB0'                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque

new_current= 0
cycle=0

timevec=[]
current=[]
vel=[]
pwm=[]
pos=[]

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows

portHandler_T = PortHandler(DEVICENAME_T)
#portHandler_P = PortHandler(DEVICENAME_P)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler_T.openPort():
    print("Succeeded to open the T port")
else:
    print("Failed to open the T port")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler_T.setBaudRate(BAUDRATE):
    print("Succeeded to change the T baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()


# Enable Dynamixel Torque







dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("T Dynamixel has been successfully connected")

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_OPERATING_MODE, 0)# 0 current mode
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
"""
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PROFILE_VELOCITY, 15)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
"""

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("torque on")

print("THE DYNAMIXEL IS SET UP AND READY TO USE")
print("NOW TARE.....")
time.sleep(0.5)
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

valuesf=[]
hx = HX711(5, 6)
vals=[0,0,0,0,0]
referenceUnit = 1
hx.set_reading_format("MSB", "MSB")
hx.reset()
hx.tare()
print("Tare done! ready...")

time_old = datetime.now()
abstime=0

while 1:

    try:

        cycle+=1
        if cycle>=100:
            cycle=0
            new_current-=1

        val = hx.get_weight(1)/467000
        val = filter(val)
        valuesf.append(val)
        print(val)

        """
        current_T, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_CURRENT)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))


        
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_GOAL_POSITION, new_pos)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        """

        pwm_T, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_PWM)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        current_T, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_CURRENT)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler_T, DXL_ID_T, ADDR_GOAL_CURRENT, new_current)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        """

        position_P, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_P, DXL_ID_P, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        """
        velocity_T, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_VELOCITY)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        position_T, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        current.append(np.int16(current_T))
        vel.append(np.int32(np.uint32(velocity_T))*0.229)
        pwm.append(np.int16(pwm_T))
        pos.append(position_T)
        
        timevec.append(abstime/1000000)
        time_new = datetime.now()
        delta=(time_new.microsecond-time_old.microsecond)%1000000
        abstime+=delta
        time_old = time_new

    except (KeyboardInterrupt, SystemExit):

        # Disable Dynamixel Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        # Close port
        portHandler_T.closePort()

        storeData()
        plotdata()
        print('mean:')
        print(np.mean(valuesf))
        print('standart deviation:')
        print(np.std(valuesf))
        print(-hx.get_offset_A()/467000.0)
        cleanAndExit()
        


        #x=np.arange(0,len(measure_pos_t),1)
        #plt.plot(x,measure_pos_t)
        #plt.plot(x,measure_torque)
        #plt.plot(x,measure_pos_p)
        #plt.show()

getch()
