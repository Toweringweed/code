#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-07-21 16:18:45
# Project: **

import numpy as np, pandas as pd
import matplotlib
import matplotlib.pylab as plt

X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C,S = np.cos(X), np.sin(X)

plt.plot(X, C)
plt.plot(X, S)
plt.plot([5,3,4,5,8,9],[2,3,4,5,8,9],'py')
plt.xlabel('first pic')

data = np.random.normal(5.0,10.0,1000)
bins = np.arange(-5.,16.,1.)
plt.hist(data, bins, histtype='stepfilled')
plt.show()




bentian = pd.io.parsers.read_csv('E:\\Python\\data2\\bentian.csv')
p1 = bentian[['v_biaoti', 'v_jiage', 'v_shangjiashijian']].head()
p2 = bentian[bentian['v_shangjiashijian']=='2016-12-13']['v_biaoti']

nn1 = list(range(10))
nn2 = list(np.arange(10))
arr1 = np.array((1,20,30))
arr2 = np.ones([3, 4])
arr3 = np.array(np.arange(16)).reshape(4, 4)
arr4 = np.random.randint(1,100,size=24).reshape(6,4)

np.random.seed(1234)
N = 1000
randnorm = np.random.normal(size=N)
counts, bins, path = matplotlib.pylab.hist(randnorm, bins=np.sqrt(N), normed=True, color='blue')



n1 = np.random.seed(1234)

n2 = np.random.f(2, 4, size=100)
