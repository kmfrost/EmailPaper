# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 15:10:27 2016

@author: Kayla
"""
from __future__ import division
import pandas as pd
from scipy.stats import entropy

def calc_entropy(data_series):
    counts = pd.value_counts(data_series)
    freqs = counts/sum(counts)
    return entropy(freqs, base=2)

# get the various data frames imported and ready
csv = pd.read_csv("../../Thesis/DataFiles/trai_norm_email_features_100.csv")
pids = csv['pid'].tolist()
no_pids = csv.drop('pid', axis=1)
raw_data = no_pids.drop('Status', axis=1)
parent_entropy = calc_entropy(csv['Status'])
num_rows = csv.shape[0]

info_gains = pd.DataFrame(columns=['Feature', 'InfoGain'])

# loop through each feature and calculate the maximum mutual information
for feature in raw_data.columns.tolist():
    max_ig = 0
    feat_data = csv[[feature, 'Status']]
    feat_data.sort(columns=feature, inplace=True)
    feat_data.reset_index(inplace=True)
    for row_idx in xrange(num_rows-1):
        part1 = feat_data[:row_idx+1]
        part2 = feat_data[row_idx+1:]
        
        entropy1 = calc_entropy(part1['Status'])
        entropy2 = calc_entropy(part2['Status'])
        
        prop1 = part1.shape[0]/num_rows
        prop2 = part2.shape[0]/num_rows
        
        ig = parent_entropy - (prop1*entropy1 + prop2*entropy2)
        if ig > max_ig:
            max_ig = ig
    info_gains.loc[len(info_gains)+1] = [feature, max_ig]
info_gains.to_csv("../../Thesis/Relevant Documents/InfoGain.csv")
    