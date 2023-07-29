import os, sys
import time
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

temp1 = traci._trafficlight.TrafficLightDomain()
temp2 = traci._lanearea.LaneAreaDomain()

depart_time = 2

def phasetime(phase): #algo 2
    newtime = 0
    if phase==2:
        newtime = (max(temp2.getLastStepVehicleNumber("e2det_-E1_0"),temp2.getLastStepVehicleNumber("e2det_-E1_1")))*depart_time
        print(newtime)
        temp1.setPhaseDuration('J2',newtime)
    elif phase==4:
        newtime = (max(temp2.getLastStepVehicleNumber("e2det_-E3_0"),temp2.getLastStepVehicleNumber("e2det_-E3_1")))*depart_time
        print(newtime)
        temp1.setPhaseDuration('J2',newtime)
    elif phase==6:
        newtime = (max(temp2.getLastStepVehicleNumber("e2det_E0_0"),temp2.getLastStepVehicleNumber("e2det_E0_1")))*depart_time
        print(newtime)
        temp1.setPhaseDuration('J2',newtime)
    elif phase==0:
        newtime = (max(temp2.getLastStepVehicleNumber("e2det_-E2_0"),temp2.getLastStepVehicleNumber("e2det_-E2_1")))*depart_time
        print(newtime)
        temp1.setPhaseDuration('J2',newtime)
    return newtime
        
        

def whynot(): #red when no vehicle
    if temp2.getLastStepVehicleNumber("e2det_-E1_0") == 0 and temp2.getLastStepVehicleNumber("e2det_-E1_1") == 0 and temp2.getLastStepVehicleNumber("e2det_-E1_2") == 0 and temp1.getPhase('J2')==2:
        temp1.setPhase('J2',4)
        phasetime(temp1.getPhase('J2'))
        
    if temp2.getLastStepVehicleNumber("e2det_-E2_0") == 0 and temp2.getLastStepVehicleNumber("e2det_-E2_1") == 0 and temp2.getLastStepVehicleNumber("e2det_-E2_2") == 0 and temp1.getPhase('J2')==0:
        temp1.setPhase('J2',2)
        phasetime(temp1.getPhase('J2'))
        
    if temp2.getLastStepVehicleNumber("e2det_-E3_0") == 0 and temp2.getLastStepVehicleNumber("e2det_-E3_1") == 0 and temp2.getLastStepVehicleNumber("e2det_-E3_2") == 0 and temp1.getPhase('J2')==4:
        temp1.setPhase('J2',6)
        phasetime(temp1.getPhase('J2'))
        
    if temp2.getLastStepVehicleNumber("e2det_E0_0") == 0 and temp2.getLastStepVehicleNumber("e2det_E0_1") == 0 and temp2.getLastStepVehicleNumber("e2det_E0_2") == 0 and temp1.getPhase('J2')==6:
        temp1.setPhase('J2',0)
        phasetime(temp1.getPhase('J2'))
        
 #------------------------------------------------------------------------------------------------------------------------

episodes = 5
Total_Reward = []
Action_Value = [[0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]] #The Action_Value table that the agent creates during learning
Reward_Value = np.zeros(4) #For tracking the reward of each action
Count_Value = [[0,0,0,0],
                [0,0,0,0],
                [0,0,0,0],
                [0,0,0,0]] #Number of times each action has been performed
Current_Reward = 0
        

def update(reward,state,ind):
    Count_Value[state][ind] += 1
    Action_Value[state][ind] += (reward - Action_Value[state][ind])/Count_Value[state][ind]
    
    
        
for i in range(episodes):
    
    sumoCmd = ["sumo-gui", "-c", "sumoconfig.sumocfg", "--start"]
    traci.start(sumoCmd)
    
    print("Starting SUMO")
    traci.gui.setSchema("View #0", "real world")

    step = 0
    count = 0
    x = 0
    state_count = [0,0,0,0] #vehicles in each road
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        if x==1:
            newy = temp2.getJamLengthMeters("e2det_-E1_0") + temp2.getJamLengthMeters("e2det_-E1_1") + temp2.getJamLengthMeters("e2det_-E2_0") + temp2.getJamLengthMeters("e2det_-E2_1") + temp2.getJamLengthMeters("e2det_-E3_0") + temp2.getJamLengthMeters("e2det_-E3_1") + temp2.getJamLengthMeters("e2det_E0_0") + temp2.getJamLengthMeters("e2det_E0_1")
            Current_Reward = newy-y
            update(Current_Reward,state,ind)
            Total_Reward.append(Current_Reward)
            x=0
        
        if count==0 and temp1.getPhase('J2') in [0,2,4,6]:
            
            
            state_count[0] = temp2.getLastStepVehicleNumber("e2det_-E1_0") + temp2.getLastStepVehicleNumber("e2det_-E1_1")
            state_count[1] = temp2.getLastStepVehicleNumber("e2det_-E2_0") + temp2.getLastStepVehicleNumber("e2det_-E2_1")
            state_count[2] = temp2.getLastStepVehicleNumber("e2det_-E3_0") + temp2.getLastStepVehicleNumber("e2det_-E3_1")
            state_count[3] = temp2.getLastStepVehicleNumber("e2det_E0_0") + temp2.getLastStepVehicleNumber("e2det_E0_1")
            
            state = state_count.index(max(state_count))
            
            ind = Action_Value[state].index(max(Action_Value[state]))
            
            if ind==0:
                act = 2
            elif ind==1:
                act = 0
            elif ind==2:
                act = 4
            elif ind==3:
                act = 6
                
            
            count = phasetime(act)*10 #multiplied by 10 cuz 0.1 time setps in xml settings
            y = temp2.getJamLengthMeters("e2det_-E1_0") + temp2.getJamLengthMeters("e2det_-E1_1") + temp2.getJamLengthMeters("e2det_-E2_0") + temp2.getJamLengthMeters("e2det_-E2_1") + temp2.getJamLengthMeters("e2det_-E3_0") + temp2.getJamLengthMeters("e2det_-E3_1") + temp2.getJamLengthMeters("e2det_E0_0") + temp2.getJamLengthMeters("e2det_E0_1")
            
            x = 1
        else:
            count-=1
            if count<0:
                count = 0
        print("Phase: ", temp1.getPhase('J2'))
        
        """
        if temp1.getPhase('J2')==1 or temp1.getPhase('J2')==3 or temp1.getPhase('J2')==5 or temp1.getPhase('J2')==7:
            phase = temp1.getPhase('J2')
            if phase==7:
                temp1.setPhase('J2',0)
                phasetime(temp1.getPhase('J2'))
            else:
                temp1.setPhase('J2',phase+1)
                phasetime(temp1.getPhase('J2'))
        """
        

    traci.close()