import vrep
import sys
from time import sleep
import matplotlib.pyplot as plt

vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
#clientID=vrep.simxStart('192.168.1.2',19997,True,True,5000,5) # Connect to V-REP

# Connect
if clientID == -1:
    print "Connection Error!"
    sys.exit()

print "Connected to remote API server"

# Car Control
zerrorCode, left_motor_handle = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_leftMotor", vrep.simx_opmode_blocking)
errorCode, right_motor_handle = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx_rightMotor", vrep.simx_opmode_blocking)
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

GPSerror=[]
while True:
#for i in range(100):    
    # Gyro Get
    gyroX = vrep.simxGetFloatSignal(clientID, 'gyroX', vrep.simx_opmode_oneshot)[1]
    gyroY = vrep.simxGetFloatSignal(clientID, 'gyroY', vrep.simx_opmode_oneshot)[1]
    gyroZ = vrep.simxGetFloatSignal(clientID, 'gyroZ', vrep.simx_opmode_oneshot)[1]
    print("Gyro : {:.5f} {:.5f} {:.5f}".format(gyroX, gyroY, gyroZ))
    
    # Accelerometer Get
    accelX = vrep.simxGetFloatSignal(clientID, 'accelerometerX', vrep.simx_opmode_oneshot)[1]
    accelY = vrep.simxGetFloatSignal(clientID, 'accelerometerY', vrep.simx_opmode_oneshot)[1]
    accelZ = vrep.simxGetFloatSignal(clientID, 'accelerometerZ', vrep.simx_opmode_oneshot)[1]
    print("Accelerometer : {:.5f} {:.5f} {:.5f}".format(accelX, accelY, accelZ))
    
    # GPS Get
    gpsX = vrep.simxGetFloatSignal(clientID, 'gpsX', vrep.simx_opmode_oneshot)[1]
    gpsY = vrep.simxGetFloatSignal(clientID, 'gpsY', vrep.simx_opmode_oneshot)[1]
    gpsZ = vrep.simxGetFloatSignal(clientID, 'gpsZ', vrep.simx_opmode_oneshot)[1]
    print("GPS : {:.5f} {:.5f} {:.5f}".format(gpsX, gpsY, gpsZ))
    
    # Absolute Position Get
    errorCode, pos = vrep.simxGetObjectPosition(clientID, left_motor_handle, -1, vrep.simx_opmode_streaming)
    print("Position : {:.5f} {:.5f} {:.5f}\n".format(pos[0], pos[1], pos[2]))
    
    sleep(0.3)

#    GPSerror.append(((gpsX-pos[0])**2)**1/2+((gpsY-pos[1])**2)**1/2+((gpsZ-pos[2])**2)**1/2)
#plt.plot(GPSerror)