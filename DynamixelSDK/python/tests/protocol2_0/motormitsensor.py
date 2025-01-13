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
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
from datetime import datetime

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
DXL_ID_T                      = 2                 # Dynamixel ID : 1
DXL_ID_P                      = 1
BAUDRATE                      = 1000000            # Dynamixel default baudrate : 57600
DEVICENAME_P                  = '/dev/ttyUSB1'         # Check which port is being used on your controller
DEVICENAME_T                  = '/dev/ttyUSB0'                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque

measure_pos_t=[]
measure_pos_p=[]

measure_torque=[]
timevec=[]

measure_cur_t=[]
measure_cur_p=[]
measure_pwm_target=[]


posf=[2000,2000,2000,2000,2000,2000,2000]
new_pos=2000

speed_cal=0
pos_o=2000
pos_n=2000

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler_T = PortHandler(DEVICENAME_T)
####################################    portHandler_P = PortHandler(DEVICENAME_P)

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

#if portHandler_P.openPort():
#    print("Succeeded to open the P port")
#else:
#    print("Failed to open the P port")
#    print("Press any key to terminate...")
#    getch()
#    quit()

# Set port baudrate
if portHandler_T.setBaudRate(BAUDRATE):
    print("Succeeded to change the T baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()


#if portHandler_P.setBaudRate(BAUDRATE):
#    print("Succeeded to change the P baudrate")
#else:
#    print("Failed to change the baudrate")
#    print("Press any key to terminate...")
#    getch()
#    quit()

# Enable Dynamixel Torque

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("T Dynamixel has been successfully connected")

#dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
#if dxl_comm_result != COMM_SUCCESS:
#    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
#elif dxl_error != 0:
#    print("%s" % packetHandler.getRxPacketError(dxl_error))
#else:
#    print("P Dynamixel has been successfully connected")


#dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_OPERATING_MODE, 3)# 3 is position mode
#if dxl_comm_result != COMM_SUCCESS:
#    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
#elif dxl_error != 0:
#    print("%s" % packetHandler.getRxPacketError(dxl_error))

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_OPERATING_MODE, 3)# 16 is pwm mode
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

#dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
#if dxl_comm_result != COMM_SUCCESS:
#    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
#elif dxl_error != 0:
#    print("%s" % packetHandler.getRxPacketError(dxl_error))
#else:
#    print("P Dynamixel has been successfully connected")

dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PROFILE_VELOCITY, 400)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PROFILE_ACCELERATION, 50)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

#position_T, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_POSITION)
#if dxl_comm_result != COMM_SUCCESS:
#    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
#elif dxl_error != 0:
#    print("%s" % packetHandler.getRxPacketError(dxl_error))

#dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_P, DXL_ID_P, ADDR_GOAL_POSITION, position_T)
#if dxl_comm_result != COMM_SUCCESS:
#    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
#elif dxl_error != 0:
#    print("%s" % packetHandler.getRxPacketError(dxl_error))

#time.sleep(4.0)

#dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
#if dxl_comm_result != COMM_SUCCESS:
#    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
#elif dxl_error != 0:
#    print("%s" % packetHandler.getRxPacketError(dxl_error))

#dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_OPERATING_MODE, 16)# 16 is pwm mode
#if dxl_comm_result != COMM_SUCCESS:
#    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
#elif dxl_error != 0:
#    print("%s" % packetHandler.getRxPacketError(dxl_error))

#dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
#if dxl_comm_result != COMM_SUCCESS:
#    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
#elif dxl_error != 0:
#    print("%s" % packetHandler.getRxPacketError(dxl_error))

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("T Dynamixel has been successfully connected")

time.sleep(0.5)
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
hx = HX711(8,7)#5,6
hx.set_reading_format("MSB", "MSB")
hx.reset()
hx.tare()
vals=[0,0,0,0,0]


print("Tare done! ready...")





time_old = datetime.now()
abstime=0
while 1:
    try:

        """
        current_T, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_CURRENT)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        current_P, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler_P, DXL_ID_P, ADDR_PRESENT_CURRENT)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        """
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_GOAL_POSITION, new_pos)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        """
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler_P, DXL_ID_P, ADDR_GOAL_PWM, new_pwm)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))



        position_P, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_P, DXL_ID_P, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        """
        position_T, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))


        pos_o=pos_n
        pos_n=position_T
        daspeed=(pos_n-pos_o)/0.01 #0.01 estimation for time delta
        print(daspeed)



        torqueA = filter((hx.get_weight(1))/467000)
        print(torqueA)
        if torqueA > 0.6:
            new_pos = 2300
        elif torqueA <= -0.6:
            new_pos = 1700
        else:
            new_pos = 2000+np.int16(torqueA*500)#-0.01*daspeed)    TODO: try using difference of target position and actual position to introduce some damping. when diff is groß reduce target

        """

        posf[0]=posf[1]
        posf[1]=posf[2]
        posf[2]=posf[3]
        posf[3]=posf[4]
        posf[4]=posf[5]
        posf[5]=posf[6]
        posf[6]=new_pos

        new_pos=np.int16((posf[0]+posf[1]+posf[2]+posf[3]+posf[4]+posf[5]+posf[6])/7)
        """


        #print("[ID:%03d] PresPos:%03d" % (DXL_ID_T, position_T))

        measure_pos_t.append(position_T)
        measure_torque.append(torqueA*1000+2000)
        #measure_pos_p.append(position_P)
        #measure_cur_t.append(current_T)
        #measure_cur_p.append(current_P)
        #measure_pwm_target.append(new_pwm)



        #Limiting and filtering the values
        #print(np.int16(1/4*np.int32(np.uint32(velocity_P))-1*(np.int16(current_P))))



        #new_pwm=0-3*(np.int16(current_P))-3*(np.int16(current_T))
        #new_current=np.int16(1/10*np.int32(np.uint32(velocity_P))-1*(np.int16(current_P)))  #so far did not work well either more advanced model or not
        #if new_current>100:
        #    new_current=0
        #elif new_current<-100:
        #    new_current=0
        """
        pwm[0]=pwm[1]
        pwm[1]=pwm[2]
        pwm[2]=pwm[3]
        pwm[3]=pwm[4]
        pwm[4]=pwm[5]
        pwm[5]=pwm[6]
        pwm[6]=pwm[7]
        pwm[7]=pwm[8]
        pwm[8]=pwm[9]
        pwm[9]=new_pwm

        new_pwm=np.int16((pwm[0]+pwm[1]+pwm[2]+pwm[3]+pwm[4]+pwm[5]+pwm[6]+pwm[7]+pwm[8]+pwm[9])/10)

        

        pwm[0]=pwm[1]
        pwm[1]=pwm[2]
        pwm[2]=pwm[3]
        pwm[3]=new_pwm

        new_pwm=np.int16((pwm[0]+pwm[1]+pwm[2]+pwm[3])/4)
        """

        print(new_pos)

        timevec.append(abstime/1000000)
        time_new = datetime.now()
        delta=(time_new.microsecond-time_old.microsecond)%1000000
        abstime+=delta
        time_old = time_new
        print(delta)
    except (KeyboardInterrupt, SystemExit):

        GPIO.cleanup()

        # Disable Dynamixel Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        """
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_P, DXL_ID_P, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        """

        # Close port
        portHandler_T.closePort()
        #portHandler_P.closePort()


        x=np.arange(0,len(measure_pos_t),1)
        plt.plot(x,measure_pos_t)
        plt.plot(x,measure_torque)
        #plt.plot(x,measure_pos_p)
        plt.show()
        """
        xx=np.arange(0,len(measure_cur_t),1)
        measure_cur_t=np.int16(measure_cur_t)
        measure_cur_p=np.int16(measure_cur_p)


        plt.plot(xx,measure_cur_t)#unit 2.69 mA
        plt.plot(xx,measure_pwm_target)
        plt.plot(xx,measure_cur_p)
        plt.show()
        """
        getch()
