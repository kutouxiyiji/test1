# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 15:01:50 2019

@author: yongw
"""
 
    
import gzip
import ujson as json

    
import random

#Fraction to subsample, needs to be between 0 and 1
subsample = 0.2
#subsample = 1
data = json.loads('C:/Users/yongw/Downloads/yelp_dataset/yelp_dataset')

#with gzip.open('C:/Users/yongw/Downloads/yelp_dataset.tar') as f:
#    data = [json.loads(line) for line in f if random.random() < subsample]
print(data[0])