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
import keyboard
import time
from datetime import datetime

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

from dynamixel_sdk import *                    # Uses Dynamixel SDK library
from dynamixel_sdk.port_handler import PortHandler
from dynamixel_sdk.packet_handler import PacketHandler
from dynamixel_sdk.robotis_def import *


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

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID_T                      = 1                 # Dynamixel ID : 1
DXL_ID_P                      = 2
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME_P                  = '/dev/ttyUSB1'  #SensorB       # Check which port is being used on your controller
DEVICENAME_T                  = '/dev/ttyUSB0'  #SensorA                                              # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque


measure_pos=[]
measure_cur=[]
measure_cur_f=[]
measure_vel=[]
measure_vel_P=[]
current=[0,0,0,0,0,0,0,0,0,0]
new_current=0

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler_T = PortHandler(DEVICENAME_T)
portHandler_P = PortHandler(DEVICENAME_P)

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

if portHandler_P.openPort():
    print("Succeeded to open the P port")
else:
    print("Failed to open the P port")
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


if portHandler_P.setBaudRate(BAUDRATE):
    print("Succeeded to change the P baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel Torque





while 1:

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("T Dynamixel has been successfully connected")

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("P Dynamixel has been successfully connected")



    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_OPERATING_MODE, 3)# 3 is position mode
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_OPERATING_MODE, 0)# 0 is current control mode
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("P Dynamixel has been successfully connected")

    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_P, DXL_ID_P, ADDR_PROFILE_VELOCITY, 20)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))



    position_T, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_P, DXL_ID_P, ADDR_GOAL_POSITION, position_T)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    time.sleep(4.0)

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_OPERATING_MODE, 1)# 1 is velocity mode
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("T Dynamixel has been successfully connected")

    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_P, DXL_ID_P, ADDR_PROFILE_ACCELERATION, 0)# should be 10 otherwise trajectory is not followed
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    time.sleep(2.0)


    print("all set: patient velocity mode therapist current mode")

    if getch() == chr(0x1b):
        break

    time_old = datetime.now()

    while 1:

        #measuring time of the loop
        time_new = datetime.now()
        delta=time_new.microsecond-time_old.microsecond
        time_old = time_new
        print(delta)

        velocity_T, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_VELOCITY)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        velocity_P, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_P, DXL_ID_P, ADDR_PRESENT_VELOCITY)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        position_T, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_P, DXL_ID_P, ADDR_GOAL_VELOCITY, velocity_T)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        current_P, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler_P, DXL_ID_P, ADDR_PRESENT_CURRENT)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))


        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler_T, DXL_ID_T, ADDR_GOAL_CURRENT, new_current)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))


        print("[ID:%03d] PresPos:%03d" % (DXL_ID_T, position_T))

        measure_pos.append(position_T)
        measure_cur.append(current_P)
        measure_cur_f.append(new_current)
        measure_vel.append(velocity_T)
        measure_vel_P.append(velocity_P)


        #Limiting and filtering the values
        print(np.int16(1/4*np.int32(np.uint32(velocity_P))-1*(np.int16(current_P))))



        new_current=-1*(np.int16(current_P))
        #new_current=np.int16(1/10*np.int32(np.uint32(velocity_P))-1*(np.int16(current_P)))  #so far did not work well either more advanced model or not
        if new_current>100:
            new_current=0
        elif new_current<-100:
            new_current=0
        """
        current[0]=current[1]
        current[1]=current[2]
        current[2]=current[3]
        current[3]=current[4]
        current[4]=current[5]
        current[5]=current[6]
        current[6]=current[7]
        current[7]=current[8]
        current[8]=current[9]
        current[9]=new_current

        new_current=np.int16((current[0]+current[1]+current[2]+current[3]+current[4]+current[5]+current[6]+current[7]+current[8]+current[9])/10)

        """

        current[0]=current[1]
        current[1]=current[2]
        current[2]=current[3]
        current[3]=new_current

        new_current=np.int16((current[0]+current[1]+current[2]+current[3])/4)


        print(new_current)





        if keyboard.is_pressed('b'):
            break

    if getch() == chr(0x1b):
        break




# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))


# Close port
portHandler_T.closePort()
portHandler_P.closePort()


x=np.arange(0,len(measure_pos),1)
plt.plot(x,measure_pos)
plt.show()

xx=np.arange(0,len(measure_cur),1)
measure_cur=np.int16(measure_cur)
measure_cur_f=np.int16(measure_cur_f)
measure_vel=np.int32(np.uint32(measure_vel))
measure_vel_P=np.int32(np.uint32(measure_vel_P))

np.savetxt('data/sensorless_demo/current_P-x',measure_cur,delimiter=",")
np.savetxt('data/sensorless_demo/velocity_T-x',measure_vel,delimiter=",")
np.savetxt('data/sensorless_demo/velocity_P-x',measure_vel_P,delimiter=",")





plt.plot(xx,measure_cur)#unit 2.69 mA
plt.plot(xx,measure_vel)
plt.plot(xx,measure_vel_P)
plt.plot(xx,measure_cur_f)
plt.show()
getch()
