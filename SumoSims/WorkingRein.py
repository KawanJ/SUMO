#East North South West
import os, sys
import numpy as np


if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")
    
import traci
import traci.constants
import traci._trafficlight
import traci._lanearea
import traci._lane

TrafficClass = traci._trafficlight.TrafficLightDomain()
LaneDetClass = traci._lanearea.LaneAreaDomain()
LaneClass = traci._lane.LaneDomain()

#%%
depart_time = 2

def phasetime(): #algo 2
    TrafficClass.setPhaseDuration('J2',8)
    return 8
#%%
episodes = 5
Action_Value = [[0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]] #The Action_Value table that the agent creates during learning

Current_Reward = 0
    
for i in range(episodes):
    sumoCmd = ["sumo-gui", "-c", "sumoconfig.sumocfg", "--start", "--quit-on-end"]
    traci.start(sumoCmd)
    print("Starting SUMO")
    traci.gui.setSchema("View #0", "real world")
    
    count = 0
    CompareTime = 0
    IndAtTime = 0
    StateAtTime = 0

    
    state_count = [0,0,0,0] #vehicles in each road

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        state_count[0] = LaneDetClass.getJamLengthVehicle("e2det_-E1_0") + LaneDetClass.getJamLengthVehicle("e2det_-E1_1")
        state_count[1] = LaneDetClass.getJamLengthVehicle("e2det_-E2_0") + LaneDetClass.getJamLengthVehicle("e2det_-E2_1")
        state_count[2] = LaneDetClass.getJamLengthVehicle("e2det_-E3_0") + LaneDetClass.getJamLengthVehicle("e2det_-E3_1")
        state_count[3] = LaneDetClass.getJamLengthVehicle("e2det_E0_0") + LaneDetClass.getJamLengthVehicle("e2det_E0_1")
        ind = Action_Value[state_count.index(max(state_count))].index(max(Action_Value[state_count.index(max(state_count))]))
        
        if ind==0:
            act = 0
        elif ind==1:
            act = 2
        elif ind==2:
            act = 4
        elif ind==3:
            act = 6
        
        if count==0 and TrafficClass.getPhase('J2') in [0,2,4,6]:
            
            TrafficClass.setPhase('J2',act)
            if act==0:
                newtime = (max(LaneDetClass.getLastStepVehicleNumber("e2det_-E2_0"),LaneDetClass.getLastStepVehicleNumber("e2det_-E2_1")))*depart_time
                TrafficClass.setPhaseDuration('J2',newtime)
                count = newtime*10
            elif act==2:
                newtime = (max(LaneDetClass.getLastStepVehicleNumber("e2det_-E1_0"),LaneDetClass.getLastStepVehicleNumber("e2det_-E1_1")))*depart_time
                TrafficClass.setPhaseDuration('J2',newtime)
                count = newtime*10
            elif act==4:
                newtime = (max(LaneDetClass.getLastStepVehicleNumber("e2det_-E3_0"),LaneDetClass.getLastStepVehicleNumber("e2det_-E3_1")))*depart_time
                TrafficClass.setPhaseDuration('J2',newtime)
                count = newtime*10
            elif act==6:
                newtime = (max(LaneDetClass.getLastStepVehicleNumber("e2det_E0_0"),LaneDetClass.getLastStepVehicleNumber("e2det_E0_1")))*depart_time
                TrafficClass.setPhaseDuration('J2',newtime)
                count = newtime*10
            
            if state_count.index(max(state_count))==0:
                print("East")
                if ind==0:
                    print("North")
                elif ind==1:
                    print("East")
                elif ind==2:
                    print("South")
                elif ind==3 :
                    print("West")
            elif state_count.index(max(state_count))==1:
                print("North")
                if ind==0:
                    print("North")
                elif ind==1:
                    print("East")
                elif ind==2:
                    print("South")
                elif ind==3 :
                    print("West")
            elif state_count.index(max(state_count))==2:
                print("South")
                if ind==0:
                    print("North")
                elif ind==1:
                    print("East")
                elif ind==2:
                    print("South")
                elif ind==3 :
                    print("West")
            elif state_count.index(max(state_count))==3:
                print("West")
                if ind==0:
                    print("North")
                elif ind==1:
                    print("East")
                elif ind==2:
                    print("South")
                elif ind==3 :
                    print("West")
                    
            print(-1 * state_count[StateAtTime])
            Action_Value[StateAtTime][IndAtTime] += -1 * state_count[StateAtTime]
            print(Action_Value)
            IndAtTime = ind
            StateAtTime = state_count.index(max(state_count))
            
        else:
            count-=1
            if count<0:     #as count can be 0 and state can be in a yellow phase
                count = 0
            
    
    traci.close()

#%%
traci.close()