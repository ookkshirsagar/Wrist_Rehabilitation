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
from datetime import datetime
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()        
    print("Bye!")
    sys.exit()

def storeData():
    """
    np.savetxt('data/versuch7/torque',valuesf,delimiter=",")
    np.savetxt('data/versuch7/vel',vel,delimiter=",")
    np.savetxt('data/versuch7/pwm',pwm,delimiter=",")
    np.savetxt('data/versuch7/pos',pos,delimiter=",")
    np.savetxt('data/versuch7/current',current,delimiter=",")
    """
    np.savetxt('data/versuchi1/SensorT',valuesTf,delimiter=",")
    np.savetxt('data/versuchi1/SensorP',valuesPf,delimiter=",")
    np.savetxt('data/versuchi1/time3',timevec,delimiter=",")
    np.savetxt('data/versuchi1/Measured_posP',posP,delimiter=",")
    np.savetxt('data/versuchi1/Measured_posT',posT,delimiter=",")


def plotdata():
    ll=len(timevec)-1
    plt.plot(timevec[0:ll],valuesTf[0:ll])
    plt.plot(timevec[0:ll],valuesPf[0:ll])

    plt.plot(timevec[0:ll],posT[0:ll])
    plt.plot(timevec[0:ll],posP[0:ll])
    """
    plt.plot(timevec[0:ll],vel[0:ll])
    plt.plot(timevec[0:ll],pwm[0:ll])
    plt.plot(timevec[0:ll],current[0:ll])
    plt.plot(timevec[0:ll],pos[0:ll])
    """
    plt.show()

def filter(vals,newdata):
    if abs(newdata + hxP.get_offset_A()/467000)<0.00001:#for checking if they are equal
       f=vals.copy()
       vals[0]=vals[1]
       vals[1]=vals[2]
       vals[2]=vals[3]
       vals[3]=vals[4]
       vals[4]=np.median(f)
       return np.median(f),vals
    elif abs(newdata + hxT.get_offset_A()/431400)<0.00001:#for checking if they are equal
       f=vals.copy()
       vals[0]=vals[1]
       vals[1]=vals[2]
       vals[2]=vals[3]
       vals[3]=vals[4]
       vals[4]=np.median(f)
       return np.median(f),vals
    elif newdata > 2.0:
       f=vals.copy()
       vals[0]=vals[1]
       vals[1]=vals[2]
       vals[2]=vals[3]
       vals[3]=vals[4]
       vals[4]=np.median(f)
       return np.median(f),vals
    elif newdata < -2.0:
       f=vals.copy()
       vals[0]=vals[1]
       vals[1]=vals[2]
       vals[2]=vals[3]
       vals[3]=vals[4]
       vals[4]=np.median(f)
       return np.median(f),vals

    vals[0]=vals[1]
    vals[1]=vals[2]
    vals[2]=vals[3]
    vals[3]=vals[4]
    vals[4]=newdata
    f=vals.copy()
    return np.median(f),vals







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
DEVICENAME_P                  = '/dev/ttyUSB2'         # Check which port is being used on your controller
DEVICENAME_T                  = '/dev/ttyUSB1'                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque

posP=[]
posT=[]
timevec=[]
valuesPf=[]
valuesTf=[]
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

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler_T, DXL_ID_T, ADDR_OPERATING_MODE, 1)# 1 is velocity control mode
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

dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_P, DXL_ID_P, ADDR_PROFILE_VELOCITY, 500)
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

dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PROFILE_ACCELERATION, 0)# should be 10 otherwise trajectory is not followed
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
"""
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler_P, DXL_ID_P, ADDR_GOAL_PWM, 300)# should be 10 otherwise trajectory is not followed
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler_T, DXL_ID_T, ADDR_GOAL_PWM, 300)# should be 10 otherwise trajectory is not followed
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
"""
time.sleep(2.0)


print("all set: patient velocity mode therapist current mode")


print("THE DYNAMIXEL IS SET UP AND READY TO USE")
print("NOW TARE.....")
time.sleep(0.5)
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

valuesf=[]
hxT = HX711(8, 7)#Sensor B
hxP = HX711(5, 6)#SensorA
valsT=[0,0,0,0,0]
valsP=[0,0,0,0,0]
referenceUnit = 1
hxT.set_reading_format("MSB", "MSB")
hxP.set_reading_format("MSB", "MSB")
hxT.reset()
hxP.reset()
hxT.tare()
hxP.tare()
print("Tare done! ready...")

time_old = datetime.now()
abstime=0





while 1:
    try:

        #measuring time of the loop
        timevec.append(abstime/1000000)
        time_new = datetime.now()
        delta=(time_new.microsecond-time_old.microsecond)%1000000
        abstime+=delta
        time_old = time_new
        print(delta)

        valP = hxP.get_weight(1)/467000
        valP,valsP = filter(valsP,valP)
        valuesPf.append(valP)

        valT = hxT.get_weight(1)/431400
        valT,valsT = filter(valsT,valT)
        valuesTf.append(-valT)
        print(valP)
        print(valT)

        
        """
        if(valT+valP<=-0.008):
            velocity=-5
        elif(valT+valP>0.008):
            velocity=5
        else:
            velocity=0
        """


        if(valT+valP<=-0.25):
            velocity=-19
        elif(valT+valP>=0.25):
            velocity=19
        else:
            velocity=np.int32(75*(valT+valP))




        """
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
        """

        position_T, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        position_P, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler_P, DXL_ID_P, ADDR_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_P, DXL_ID_P, ADDR_GOAL_VELOCITY, velocity)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler_T, DXL_ID_T, ADDR_GOAL_VELOCITY, velocity)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        posP.append(position_P)
        posT.append(position_T)

        """
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
       






        new_current=-1*(np.int16(current_P))
        #new_current=np.int16(1/10*np.int32(np.uint32(velocity_P))-1*(np.int16(current_P)))  #so far did not work well either more advanced model or not
        if new_current>100:
            new_current=0
        elif new_current<-100:
            new_current=0


        current[0]=current[1]
        current[1]=current[2]
        current[2]=current[3]
        current[3]=new_current

        new_current=np.int16((current[0]+current[1]+current[2]+current[3])/4)


        print(new_current)

        """

    except (KeyboardInterrupt, SystemExit):

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

        storeData()
        plotdata()
        """
        x=np.arange(0,len(measure_pos),1)
        plt.plot(x,measure_pos)
        plt.show()

        xx=np.arange(0,len(measure_cur),1)
        measure_cur=np.int16(measure_cur)
        measure_cur_f=np.int16(measure_cur_f)
        measure_vel=np.int32(np.uint32(measure_vel))
        measure_vel_P=np.int32(np.uint32(measure_vel_P))

        plt.plot(xx,measure_cur)#unit 2.69 mA
        plt.plot(xx,measure_vel)
        plt.plot(xx,measure_vel_P)
        plt.plot(xx,measure_cur_f)
        plt.show()
        """
        getch()
        cleanAndExit()
