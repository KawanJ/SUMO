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

def phasetime(phase): #algo 2
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
#%%


def update(reward,state,ind):
    Count_Value[state][ind] += 1
    Reward_Value[state][ind] += reward
    Action_Value[state][ind] = Reward_Value[state][ind]

episodes = 3
Action_Value = [[0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]] #The Action_Value table that the agent creates during learning

Reward_Value = [[0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]] #For tracking the reward of each action

Count_Value = [[0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]] #Number of times each action has been performed
Current_Reward = 0
    
for i in range(episodes):
    sumoCmd = ["sumo-gui", "-c", "sumoconfig.sumocfg", "--start", "--quit-on-end"]
    traci.start(sumoCmd)
    print("Starting SUMO")
    traci.gui.setSchema("View #0", "real world")
    
    count = 0
    greedyind = 0
    CompareTime = 0
    temp = 0
    IndAtTime = 0
    StateAtTime = 0

    
    state_count = [0,0,0,0] #vehicles in each road

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        state_count[0] = LaneDetClass.getLastStepVehicleNumber("e2det_-E1_0") + LaneDetClass.getLastStepVehicleNumber("e2det_-E1_1")
        state_count[1] = LaneDetClass.getLastStepVehicleNumber("e2det_-E2_0") + LaneDetClass.getLastStepVehicleNumber("e2det_-E2_1")
        state_count[2] = LaneDetClass.getLastStepVehicleNumber("e2det_-E3_0") + LaneDetClass.getLastStepVehicleNumber("e2det_-E3_1")
        state_count[3] = LaneDetClass.getLastStepVehicleNumber("e2det_E0_0") + LaneDetClass.getLastStepVehicleNumber("e2det_E0_1")
        ind = Action_Value[state_count.index(max(state_count))].index(max(Action_Value[state_count.index(max(state_count))]))
        greedyind = state_count.index(max(state_count))
        
        if ind==0:
            act = 0
            print("North")
        elif ind==1:
            act = 2
        elif ind==2:
            act = 4
        elif ind==3:
            act = 6
        
        if count==0 and TrafficClass.getPhase('J2') in [0,2,4,6]:
            Current_Reward = -1 * state_count[temp]
            if Current_Reward!=0:
                update(Current_Reward,StateAtTime,IndAtTime)
            count = phasetime(act)*10
            temp = greedyind
            IndAtTime = ind
            StateAtTime = state_count.index(max(state_count))
        else:
            count-=1
            if count<0:     #as count can be 0 and state can be in a yellow phase
                count = 0
            
    
    traci.close()

#%%
traci.close()