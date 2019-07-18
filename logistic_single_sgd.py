#! /usr/bin/env python3

import numpy as np
import pandas as pd
import time
import sys, os

import random
import pickle

from sklearn.linear_model import SGDClassifier

from utils import clean_airlinedata
# from linereader import dopen


tic0 = time.clock()
##----------------------------------------------------------------------------------------
## Logistic Regression with Single machine SGD
##----------------------------------------------------------------------------------------

file_path = ['~/running/data_raw/' + str(year) + '.csv' for year in range(1987, 2007 + 1)]
# file_path = ['~/running/data/' + str(year) + '.csv.bz2' for year in range(1987, 1987 + 1)]
# file_name = '~/running/data_raw/allfile.csv'

model_saved_file_name = '~/running/single_sgd_finalized_model.pkl'

nBatches = 1000
Y_name = 'ArrDelay'
fit_intercept = False
verbose = True
penalty = 'l2'

SGD_model = SGDClassifier(fit_intercept=fit_intercept, verbose=verbose, penalty=penalty)

for iFile in range(len(file_path)):

    sample_df = clean_airlinedata(os.path.expanduser(file_path[iFile]))

    sample_df_size = sample_df.shape[0]

    total_idx = list(range(sample_df_size))
    random.shuffle(total_idx)

    x_train = sample_df.drop([Y_name], axis=1)
    y_train = sample_df[Y_name]
    classes=np.unique(y_train)

    for iBatch in range(nBatches):

        idx_curr_batch = total_idx[round(sample_df_size / nBatches * iBatch):
                                   round(sample_df_size / nBatches * (iBatch + 1))]


        SGD_model.partial_fit(x_train.iloc[idx_curr_batch, ],
                              y_train.iloc[idx_curr_batch, ], classes=classes)

    print(print(file_path[iFile] + '\tprocessed'))


# tic = time.clock()
# parsedData = assembler.transform(data_sdf)
# time_parallelize = time.clock() - tic

# tic = time.clock()
# # Model configuration
# lr = LogisticRegression(maxIter=100, regParam=0.3, elasticNetParam=0.8)

# # Fit the model
# lrModel = lr.fit(parsedData)
# time_clusterrun = time.clock() - tic

# # Model fitted
# print(lrModel.intercept)
# print(lrModel.coefficients)

time_wallclock = time.clock() - tic0


pickle.dump(SGD_model, open(os.path.expanduser(model_saved_file_name), 'wb'))
# out = [sample_size, p, memsize, time_parallelize, time_clusterrun, time_wallclock]
# print(", ".join(format(x, "10.4f") for x in out))