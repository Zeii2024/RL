import pandas as pd
import numpy as np
import pickle

with open('Sarsa_find_room5.pkl', 'rb') as f:
    Q_table = pickle.load(f)

print(Q_table)