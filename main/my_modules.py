import numpy as np
import csv
import matplotlib.pyplot as plt
from constants import *

def load_generated_sinario():
    all_data = []
    for name in ['oil_price','freight_outward','freight_homeward','exchange_rate','demand','supply','new_ship','secondhand_ship']:
        history_data_path = '../scenario/{}.csv'.format(name)
        # read data
        dt   = np.dtype({'names': ('date', 'price'),
                       'formats': ('S10' , np.float)})
        data = np.array([], dtype=dt)
        for j in range(DEFAULT_PREDICT_PATTERN_NUMBER):
            data = np.append(data,np.genfromtxt(history_data_path,
                             delimiter=',',
                             dtype=dt,
                             usecols=[2*j,2*j+1],
                             skip_header=0,
                             encoding='utf-8_sig'))
        data = data.reshape(DEFAULT_PREDICT_PATTERN_NUMBER,DEFAULT_PREDICT_YEARS*12)
        all_data.append(data)
    return all_data

def calc_statistics(list):
    n = len(list)
    e = 0
    sigma = 0
    for i in range(n):
        e += list[i]
    e /= n
    for i in range(n):
        sigma += (list[i] - e)**2
    sigma /= n
    
    return [e,sigma]


