#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Jul 26 15:47:13 2018
@author: EvanTroop
Sources : 
    https://stackoverflow.com/questions/22963263/creating-a-zero-filled-pandas-data-frame
    https://stackoverflow.com/questions/18692261/whats-a-simple-way-to-hard-code-a-6x6-numpy-matrix
    https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
    https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
    https://stackoverflow.com/questions/10202570/pandas-dataframe-find-row-where-values-for-column-is-maximal
    https://stackoverflow.com/questions/13717554/weird-behaviour-initializing-a-numpy-array-of-string-data
    
    
"""

import pandas as pd
import random as rd
#import tensorflow as tf
#import numpy as np

def generate_csv(name, type_list='BASIC'): 
    if type_list == 'BASIC':
        state_list = []
        for p1 in range(1,6):
            for p2 in range(1,6):
                for p3 in range(1,6):
                    for p4 in range(1,6):
                        for p5 in range(1,6):
                            n = 10000*p1  +1000*p2 + 100*p3 + 10*p4 + p5
                            state_list.append(n)
                        
        action_list = [1,2,3,4,5]
    
        frame = pd.DataFrame(0,index=state_list, columns=action_list)
        frame.to_csv(name)
        frame.describe()
        return True
    return False
   
    
scales = [[1,2,4,8,16], #Zealot
          [2,4,8,16,32], #Stalker
          [0,1,2,4,8], #Immortal
          [0,1,2,4,8], #Sentury
          [2700,5400,8100,13500,27000]] #Time


""" Returns an array of scaled values in the format[zealot, stalker, immortal, sentury, time] """
def get_scaled_value(typ, n_zealot=0, n_stalker=0, n_immortal=0, n_sentury= 0, time=0):
    if typ == 'SIMPLE':
        numbers = [n_zealot, n_stalker, n_immortal, n_sentury, time]
        outs = [0,0,0,0,0]
        for i in range(len(numbers)):
            for j in range(len(scales[i])):

                if scales[i][j] >= numbers[i]:

                    outs[i] = j + 1
                    break
            if(outs[i] == 0):
                outs[i] = 5
        state = 10000*outs[0] + 1000*outs[1] + 100*outs[2] + 10*outs[3] + outs[4]
        return state
  
"""This returns a list with format [n_zealots, n_stalker, n_immortal, n_sentury]"""
def get_unit_nums(data):
    out = list([0,0,0,0])
    for l1 in data:
        if l1[0] == 73:
            out[0] = l1[1]
        elif l1[0] == 74:
            out[1] = l1[1]
        elif l1[0] == 83:
            out[2] = l1[1]
        elif l1[0] == 77:
            out[3] = l1[1]
    return out
    
""" Q_List Driver Class"""
class Q_list():
    states = [10]
    actions = [10]
    index = 0
    def __init__(self, path, mode='LEARNING'):
        #rows(index) = states
        #columns is actions
        self.path = path
        self.min_state = 11111
        self.max_state = 55555
        

        

        #a number if you want to limit how many future steps are counted, -1 if you want no endpoint
        self.recersive_units = 10
        #how much each step into the future retains value
        self.gamma = 0.8
       
        #likleyhood that we try new spots
        if mode == "LEARNING" :
            self.is_learning = True
            #MUST BE GREATER THAN 1
            self.record_last_index = 1
            self.epsilon = 0.95
        else : 
            
            self.is_learning = False
            self.record_last_index = 3
            self.epsilon = 0.0001
        
        _index_ = []
        
        for i in range(self.record_last_index + 1):
            _index_.append(i)
        
        # will store past actions
        self.past_actions = pd.DataFrame(0,index=_index_, columns=['state', 'action'])
        self.q_list = pd.read_csv(path, index_col=0)


        
      
    
    
    """This will return the desired action accounting for Epsilon"""
    def get_max_action(self, state):
        if state >= self.min_state and state <= self.max_state:
            if rd.randint(0,100) > 100 * self.epsilon:
                return self.q_list.loc[state].idxmax()
            else :
                rand = rd.randint(1, 5)
                return rand
        
    
    
    """This will set the reward for a given state. won't do any calculations"""
    def set_reward(self, state, action, last_reward):
        if self.is_learning:

            for i in range(len(self.past_actions.index)):
                st = self.past_actions.loc[i]['state']
                ac = self.past_actions.loc[i]['action']
            
                if st != 0:   
                    current_val = self.q_list.loc[st][str(ac)]
                    current_val = current_val + last_reward * self.gamma ** (self.record_last_index - i)
                    self.q_list.loc[st][str(ac)] = current_val
        if int(state) >= int(self.min_state) and int(state) <= int(self.max_state) and int(action) >= 1 and int(action) <= 5:
            

            for i in range(1, self.record_last_index + 1):

                last_s = self.past_actions.loc[i]['state']
                last_a = self.past_actions.loc[i]['action']
                
                self.past_actions.loc[i - 1]['state'] = last_s
                self.past_actions.loc[i - 1]['action'] = last_a
            
                
            self.past_actions.loc[self.record_last_index]['state'] = state
            self.past_actions.loc[self.record_last_index]['action'] = action
            return True
        return False
    
    
    def export_q_list(self):
        self.q_list.to_csv(self.path)
        print("Q-List was successfully exported to path : " + self.path)
        
        
    def end_of_game(self):
        self.export_q_list()
        print("End of Game Funcitons Complete")
        
ql = Q_list("Army_Q.csv")  

ql.set_reward(11111, 1, 100)  
ql.set_reward(11112, 1, 100) 
ql.set_reward(11113, 2, 100) 
ql.set_reward(11114, 2, 100) 
ql.set_reward(11115, 3, 100) 