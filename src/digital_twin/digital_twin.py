import numpy as np
from scipy.integrate import odeint
import torch
import torch.nn as nn

class MachineDigitalTwin:
    def __init__(self, initial_state, parameters):
        self.state = initial_state
        self.parameters = parameters
        self.physics_model = PhysicalModel(parameters)
        self.ml_model = MLAdaptiveLayer()
        self.uncertainty = UncertaintyEstimator()
    
    def update_state(self, sensor_data):
        physics_pred = self.physics_model.predict(self.state)
        ml_correction = self.ml_model.predict(self.state, sensor_data)
        updated_state = self.combine_predictions(physics_pred, ml_correction, sensor_data)
        self.state = updated_state
        return updated_state

    def combine_predictions(self, physics_pred, ml_correction, sensor_data):
        uncertainty = self.uncertainty.estimate(physics_pred, ml_correction, sensor_data)
        weights = 1.0 / (uncertainty + 1e-6)
        weights = weights / np.sum(weights)
        combined = weights[0] * physics_pred + weights[1] * ml_correction + weights[2] * sensor_data
        return combined