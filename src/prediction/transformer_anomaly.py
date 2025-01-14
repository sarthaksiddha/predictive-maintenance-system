import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset, DataLoader

class TimeSeriesTransformer(nn.Module):
    def __init__(self, input_dim, seq_length, num_heads=4, num_layers=2):
        super().__init__()
        
        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model=input_dim,
            nhead=num_heads,
            dim_feedforward=128,
            dropout=0.1
        )
        
        self.transformer = nn.TransformerEncoder(
            self.encoder_layer,
            num_layers=num_layers
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, input_dim)
        )
    
    def forward(self, x):
        x = x.transpose(0, 1)
        transformer_out = self.transformer(x)
        decoded = torch.stack([
            self.decoder(transformer_out[i]) 
            for i in range(transformer_out.size(0))
        ])
        return decoded.transpose(0, 1)