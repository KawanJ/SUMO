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

temp1 = traci._trafficlight.TrafficLightDomain()
temp2 = traci._lanearea.LaneAreaDomain()

sumoCmd = ["sumo-gui", "-c", "sumoconfig.sumocfg", "--start"]
traci.start(sumoCmd)

print("Starting SUMO")
traci.gui.setSchema("View #0", "real world")



def whynot():
    if temp2.getLastStepVehicleNumber("e2det_-E1_0") == 0 and temp2.getLastStepVehicleNumber("e2det_-E1_1") == 0 and temp2.getLastStepVehicleNumber("e2det_-E1_2") == 0 and temp1.getPhase('J2')==2:
        temp1.setPhase('J2',4)
        
    if temp2.getLastStepVehicleNumber("e2det_-E2_0") == 0 and temp2.getLastStepVehicleNumber("e2det_-E2_1") == 0 and temp2.getLastStepVehicleNumber("e2det_-E2_2") == 0 and temp1.getPhase('J2')==0:
        temp1.setPhase('J2',2)
        
    if temp2.getLastStepVehicleNumber("e2det_-E3_0") == 0 and temp2.getLastStepVehicleNumber("e2det_-E3_1") == 0 and temp2.getLastStepVehicleNumber("e2det_-E3_2") == 0 and temp1.getPhase('J2')==4:
        temp1.setPhase('J2',6)
        
    if temp2.getLastStepVehicleNumber("e2det_E0_0") == 0 and temp2.getLastStepVehicleNumber("e2det_E0_1") == 0 and temp2.getLastStepVehicleNumber("e2det_E0_2") == 0 and temp1.getPhase('J2')==6:
        temp1.setPhase('J2',0)
        
        

step = 0
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    whynot()
#%%
traci.close()
