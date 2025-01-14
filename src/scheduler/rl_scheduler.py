import torch
import torch.nn as nn
import numpy as np
from collections import deque
import random

class MaintenanceEnvironment:
    def __init__(self, machines_data, config):
        self.machines = machines_data
        self.config = config
        self.current_step = 0
        self.maintenance_history = []
    
    def reset(self):
        self.current_step = 0
        return self._get_state()
    
    def step(self, action):
        machine_id = action['machine_id']
        maintenance_type = action['maintenance_type']
        
        maintenance_cost = self._calculate_maintenance_cost(maintenance_type)
        downtime_cost = self._calculate_downtime_cost(machine_id, maintenance_type)
        
        self._apply_maintenance(machine_id, maintenance_type)
        reward = self._calculate_reward(maintenance_cost, downtime_cost)
        
        self.current_step += 1
        new_state = self._get_state()
        done = self.current_step >= self.config['episode_length']
        
        return new_state, reward, done