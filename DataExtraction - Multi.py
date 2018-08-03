'''
This file is for data extraction.
It receive sensor data from vrep and write in excel.
Save file 'data.xlsx'
'''


import vrep
import sys
import xlsxwriter
from time import sleep


class Robot:
    def __init__(self, name):
        self.name = name[1:] if name else name
        _, self.handle = vrep.simxGetObjectHandle(clientID, "Pioneer_p3dx"+name, vrep.simx_opmode_blocking)
        self.file = xlsxwriter.Workbook('data-robot'+name+'.xlsx')
        self.sheet = self.file.add_worksheet()

        # Some data we want to write to the worksheet.
        defaults = ['X-posi', 'Y-posi', 'Z-posi', 'gyroX', 'gyroY', 'gyroZ', 'accelX', 'accelY', 'accelZ', 'alpha', 'beta', 'gamma', 'vx', 'vy', 'vz', 'Time']

        # Iterate over the data and write it out row by row.
        for i, default in enumerate(defaults):
            self.sheet.write(0, i, default)
            i += 1


vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP

# Connect
if clientID == -1:
    print ("Connection Error!")
    sys.exit()

print ("Connected to remote API server")
num_R = int(input("Please Input the number of robots: "))

robots = [''] + [ '#'+str(x) for x in range(num_R-1) ]
robots = [ Robot(x) for x in robots ]

    
i=1
t = 0
try:
    while i<10001:

        # Simulation Time
        if t != vrep.simxGetLastCmdTime(clientID):
            t = vrep.simxGetLastCmdTime(clientID)
            
            for robot in robots:
                
                # Gyro Get
                gyroX = vrep.simxGetFloatSignal(clientID, 'gyroX'+robot.name, vrep.simx_opmode_oneshot)[1]
                gyroY = vrep.simxGetFloatSignal(clientID, 'gyroY'+robot.name, vrep.simx_opmode_oneshot)[1]
                gyroZ = vrep.simxGetFloatSignal(clientID, 'gyroZ'+robot.name, vrep.simx_opmode_oneshot)[1]
                #print("Gyro : {:.5f} {:.5f} {:.5f}".format(gyroX, gyroY, gyroZ))
                
                # Accelerometer Get
                accelX = vrep.simxGetFloatSignal(clientID, 'accelerometerX'+robot.name, vrep.simx_opmode_oneshot)[1]
                accelY = vrep.simxGetFloatSignal(clientID, 'accelerometerY'+robot.name, vrep.simx_opmode_oneshot)[1]
                accelZ = vrep.simxGetFloatSignal(clientID, 'accelerometerZ'+robot.name, vrep.simx_opmode_oneshot)[1]
                #print("Accelerometer : {:.5f} {:.5f} {:.5f}".format(accelX, accelY, accelZ))
                
                # Absolute Position Get
                errorCode, pos = vrep.simxGetObjectPosition(clientID, robot.handle, -1, vrep.simx_opmode_streaming)
                #print("Position : {:.5f} {:.5f} {:.5f}\n".format(pos[0], pos[1], pos[2]))
                
                # Orientation Get
                errorCode, ori = vrep.simxGetObjectOrientation(clientID, robot.handle, -1, vrep.simx_opmode_streaming)
                
                # Velocity
                errorCode, LinearV, AngularV = vrep.simxGetObjectVelocity(clientID, robot.handle, vrep.simx_opmode_streaming if i is 1 else vrep.simx_opmode_buffer)

                for col, data in enumerate([pos[0], pos[1], pos[2], gyroX, gyroY, gyroZ, accelX, accelY, accelZ, ori[0], ori[1], ori[2], LinearV[0], LinearV[1], LinearV[2], t]):
                    robot.sheet.write(i, col, data)

            if i % 100 == 0:
                print(i)
        else:
            i -= 1
            vrep.simxGetObjectPosition(clientID, robots[0].handle, -1, vrep.simx_opmode_streaming)


        sleep(0.01)
        i += 1
finally:
    for robot in robots:
        robot.file.close()
    print("end")


