'''
This file is for data extraction.
It receive sensor data from vrep and write in excel.
Save file 'data.xlsx'
'''

import vrep
import sys
import xlsxwriter
from time import sleep

vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
#clientID=vrep.simxStart('192.168.1.2',19997,True,True,5000,5) # Connect to V-REP

# Connect
if clientID == -1:
    print ("Connection Error!")
    sys.exit()

print ("Connected to remote API server")

# Car Control
errorCode, car_handle = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx", vrep.simx_opmode_blocking)
#errorCode, right_motor_handle = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_rightMotor", vrep.simx_opmode_blocking)
#vrep.simxSetJointTargetVelocity(clientID, left_motor_handle, 0.2, vrep.simx_opmode_streaming)
#vrep.simxSetJointTargetVelocity(clientID, right_motor_handle, 0.2, vrep.simx_opmode_streaming)


# Ultrasonic Sensor
#errorCode, sensor1 = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_ultrasonicSensor16", vrep.simx_opmode_blocking)
#returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, sensor1, vrep.simx_opmode_streaming)

# Gyro sensor
errorCode, GyroSensor = vrep.simxGetObjectHandle(clientID, "GyroSensor_reference", vrep.simx_opmode_blocking)

# Accelerometer
errorCode, AccelSensor = vrep.simxGetObjectHandle(clientID, "Accelerometer_mass", vrep.simx_opmode_blocking)

# GPS
errorCode, GPS = vrep.simxGetObjectHandle(clientID, "GPS_reference", vrep.simx_opmode_blocking)

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
defaults = ['X-posi', 'Y-posi', 'Z-posi', 'gyroX', 'gyroY', 'gyroZ', 'accelX', 'accelY', 'accelZ', 'alpha', 'beta', 'gamma', 'vx', 'vy', 'vz', 'Time']
t = 0

# Iterate over the data and write it out row by row.
for i, default in enumerate(defaults):
    worksheet.write(0, i, default)
    i += 1
    
i=1
try:
    while i<10001:
        # Pause Simulation
        #vrep.simxPauseSimulation(clientID, vrep.simx_opmode_oneshot)
        
        # Gyro Get
        gyroX = vrep.simxGetFloatSignal(clientID, 'gyroX', vrep.simx_opmode_oneshot)[1]
        gyroY = vrep.simxGetFloatSignal(clientID, 'gyroY', vrep.simx_opmode_oneshot)[1]
        gyroZ = vrep.simxGetFloatSignal(clientID, 'gyroZ', vrep.simx_opmode_oneshot)[1]
        #print("Gyro : {:.5f} {:.5f} {:.5f}".format(gyroX, gyroY, gyroZ))
        
        # Accelerometer Get
        accelX = vrep.simxGetFloatSignal(clientID, 'accelerometerX', vrep.simx_opmode_oneshot)[1]
        accelY = vrep.simxGetFloatSignal(clientID, 'accelerometerY', vrep.simx_opmode_oneshot)[1]
        accelZ = vrep.simxGetFloatSignal(clientID, 'accelerometerZ', vrep.simx_opmode_oneshot)[1]
        #print("Accelerometer : {:.5f} {:.5f} {:.5f}".format(accelX, accelY, accelZ))
        
        # GPS Get
        gpsX = vrep.simxGetFloatSignal(clientID, 'gpsX', vrep.simx_opmode_oneshot)[1]
        gpsY = vrep.simxGetFloatSignal(clientID, 'gpsY', vrep.simx_opmode_oneshot)[1]
        gpsZ = vrep.simxGetFloatSignal(clientID, 'gpsZ', vrep.simx_opmode_oneshot)[1]
        #print("GPS : {:.5f} {:.5f} {:.5f}".format(gpsX, gpsY, gpsZ))
        
        # Absolute Position Get
        errorCode, pos = vrep.simxGetObjectPosition(clientID, car_handle, -1, vrep.simx_opmode_streaming)
        #print("Position : {:.5f} {:.5f} {:.5f}\n".format(pos[0], pos[1], pos[2]))
        
        # Orientation Get
        errorCode, ori = vrep.simxGetObjectOrientation(clientID, car_handle, -1, vrep.simx_opmode_streaming)
        
        # Velocity
        errorCode, LinearV, AngularV = vrep.simxGetObjectVelocity(clientID, car_handle, vrep.simx_opmode_streaming if i is 1 else vrep.simx_opmode_buffer)
        
        # Simulation Time
        if t != vrep.simxGetLastCmdTime(clientID):
            t = vrep.simxGetLastCmdTime(clientID)

            for col, data in enumerate([pos[0], pos[1], pos[2], gyroX, gyroY, gyroZ, accelX, accelY, accelZ, ori[0], ori[1], ori[2], LinearV[0], LinearV[1], LinearV[2], t]):
                worksheet.write(i, col, data)
        else:
            i -= 1
        #vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
        sleep(0.01)
        i += 1
finally:
    workbook.close()
    print("end")
