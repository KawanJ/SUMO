import os, sys
import time

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")
    
import traci
import traci.constants
import traci._trafficlight
import traci._lanearea

TrafficClass = traci._trafficlight.TrafficLightDomain()
LaneDetClass = traci._lanearea.LaneAreaDomain()

sumoCmd = ["sumo-gui", "-c", "sumoconfig.sumocfg", "--start"]
traci.start(sumoCmd)

print("Starting SUMO")
traci.gui.setSchema("View #0", "real world")



depart_time = 2

def phasetime(phase):
    newtime = 0
    if phase==2:
        newtime = (max(LaneDetClass.getLastStepVehicleNumber("e2det_-E1_0"),LaneDetClass.getLastStepVehicleNumber("e2det_-E1_1")))*depart_time
        TrafficClass.setPhaseDuration('J2',newtime)
    elif phase==4:
        newtime = (max(LaneDetClass.getLastStepVehicleNumber("e2det_-E3_0"),LaneDetClass.getLastStepVehicleNumber("e2det_-E3_1")))*depart_time
        TrafficClass.setPhaseDuration('J2',newtime)
    elif phase==6:
        newtime = (max(LaneDetClass.getLastStepVehicleNumber("e2det_E0_0"),LaneDetClass.getLastStepVehicleNumber("e2det_E0_1")))*depart_time
        TrafficClass.setPhaseDuration('J2',newtime)
    elif phase==0:
        newtime = (max(LaneDetClass.getLastStepVehicleNumber("e2det_-E2_0"),LaneDetClass.getLastStepVehicleNumber("e2det_-E2_1")))*depart_time
        TrafficClass.setPhaseDuration('J2',newtime)
    return newtime
        


step = 0
count = 0
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    if count==0:
        count = phasetime(TrafficClass.getPhase('J2'))*10
    else:
        count-=1
    print("Phase: ", TrafficClass.getPhase('J2'))
        
#%%
traci.close()