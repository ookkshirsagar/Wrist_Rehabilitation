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

import time
from datetime import datetime





while 1:
   now = datetime.now()
   print(str(now.second) + str(now.microsecond))


"""

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

        
        
        if(valT+valP<=-0.008):
            velocity=-5
        elif(valT+valP>0.008):
            velocity=5
        else:
            velocity=0

        Pgain=60
        Igain=1
        
        if (velocity<20 and velocity>-20):                         #anti windup protection
            integrator=integrator+Igain*(valT+valP)

        velocity=np.int32(Pgain*(valT+valP))+np.int32(integrator)

        if (velocity>20):                                          #saturation for safety
            velocity=20
        elif (velocity<-20):
            velocity=-20





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

