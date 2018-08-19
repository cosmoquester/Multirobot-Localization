import vrep
import matplotlib.pyplot as plt
from sys import exit as sysexit
from time import sleep

vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

# Connect
if clientID == -1:
    print ("Connection Error!")
    sysexit()

print ("Connected to remote API server")

# Car Control
errorCode, car_handle = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx", vrep.simx_opmode_blocking)
vrep.simxGetObjectVelocity(clientID, car_handle, vrep.simx_opmode_streaming)

ok = False
time_pre = 0
time = 0
t = 0
Predict_position=[]
Previous_position=[]
pos_X = []
pos_Y = []

while True:
       
    # Gyro Get
    #gyroX = vrep.simxGetFloatSignal(clientID, 'gyroX', vrep.simx_opmode_oneshot)[1]
    #gyroY = vrep.simxGetFloatSignal(clientID, 'gyroY', vrep.simx_opmode_oneshot)[1]
    #gyroZ = vrep.simxGetFloatSignal(clientID, 'gyroZ', vrep.simx_opmode_oneshot)[1]
    #print("Gyro : {:.5f} {:.5f} {:.5f}".format(gyroX, gyroY, gyroZ))
        
    # Accelerometer Get
    #accelX = vrep.simxGetFloatSignal(clientID, 'accelerometerX', vrep.simx_opmode_oneshot)[1]
    #accelY = vrep.simxGetFloatSignal(clientID, 'accelerometerY', vrep.simx_opmode_oneshot)[1]
    #accelZ = vrep.simxGetFloatSignal(clientID, 'accelerometerZ', vrep.simx_opmode_oneshot)[1]
    #print("Accelerometer : {:.5f} {:.5f} {:.5f}".format(accelX, accelY, accelZ))
        
    # GPS Get
    #gpsX = vrep.simxGetFloatSignal(clientID, 'gpsX', vrep.simx_opmode_oneshot)[1]
    #gpsY = vrep.simxGetFloatSignal(clientID, 'gpsY', vrep.simx_opmode_oneshot)[1]
    #gpsZ = vrep.simxGetFloatSignal(clientID, 'gpsZ', vrep.simx_opmode_oneshot)[1]
    #print("GPS : {:.5f} {:.5f} {:.5f}".format(gpsX, gpsY, gpsZ))
        
    # Absolute Position Get
    errorCode, pos = vrep.simxGetObjectPosition(clientID, car_handle, -1, vrep.simx_opmode_streaming)
    #print("Position : {:.5f} {:.5f} {:.5f}\n".format(pos[0], pos[1], pos[2]))
        
    # Orientation Get
    #errorCode, ori = vrep.simxGetObjectOrientation(clientID, car_handle, -1, vrep.simx_opmode_streaming)
        
    # Velocity
    errorCode, LinearV, AngularV = vrep.simxGetObjectVelocity(clientID, car_handle, vrep.simx_opmode_buffer)
    
    # Not Started
    if not sum(pos) and not sum(LinearV):
        continue

    # Simulation Time
    if time != vrep.simxGetLastCmdTime(clientID):
        time_pre = time
        time = vrep.simxGetLastCmdTime(clientID)
    else:
        continue

    # First Step
    if not ok:
        ok=True
        Previous_position=[pos[0], pos[1], pos[2]]
        Predict_position=Previous_position[:]
        time_pre = time
        continue

    t = (time - time_pre) / 1000
    Predict_position = [Predict_position[0] + LinearV[0]*t, Predict_position[1] + LinearV[1]*t, Predict_position[2] + LinearV[2]*t]
    
    pos_X.append(Predict_position[0])
    pos_Y.append(Predict_position[1])

    plt.plot(pos_X, pos_Y)
    plt.draw();plt.pause(0.000001)
    
    print('Time:', time, 'Predict Position: x:{:.4f} y:{:.4f} z:{:.4f}'.format(Predict_position[0], Predict_position[1], Predict_position[2]))

    sleep(0.01)
