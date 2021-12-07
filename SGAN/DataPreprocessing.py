import os
import pandas as pd
import numpy as np
import pandas as pd
import statsmodels.api as sm
from numpy import *
from math import sqrt
from pandas import *
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from pickle import dump

DataFilesDir="./DataFiles/"
ProcessedFilesDir="./ProcessedFiles/"


def dataProcess(filePreFixName):
    if filePreFixName is None:
        return
    elif filePreFixName == "Wind":
        preFix = "Wind"
    elif filePreFixName == "Solar":
        preFix = "Solar"
    else:
        return

    # %% - Load Data  -----------------------------------------------------------------
    dataset = pd.read_csv(DataFilesDir + preFix + "DataFFT.csv", parse_dates=['DATE'])
    #dataset.replace(0, np.nan, inplace=True)
    dataset.isnull().sum()

    print(dataset.columns)
    # Set the date to datetime data
    datetime_series = pd.to_datetime(dataset['DATE'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    dataset = dataset.set_index(datetime_index)
    dataset = dataset.sort_values(by='DATE')
    dataset = dataset.drop(columns='DATE')

    # 아래 항목은 데이터 처리중 불필요및 오류발생
    dataset = dataset.drop(columns='IDX')
    dataset = dataset.drop(columns='logmomentum')

    print(dataset.columns)
    # Check NA and fill them
    dataset.iloc[:, 1:] = pd.concat([dataset.iloc[:, 1:].ffill(), dataset.iloc[:, 1:].bfill()]).groupby(level=0).mean()

    # Get features and target
    X_value = pd.DataFrame(dataset.iloc[:, :]) # 모든 열
    y_value = pd.DataFrame(dataset.iloc[:, 0]) # 목포값 첫번째 열

    print(X_value)
    print(y_value)
    # Autocorrelation Check
    sm.graphics.tsa.plot_acf(y_value.squeeze(), lags=100)
    plt.show()

    # Normalized the data
    X_scaler = MinMaxScaler(feature_range=(-1, 1))
    y_scaler = MinMaxScaler(feature_range=(-1, 1))
    X_scaler.fit(X_value)
    y_scaler.fit(y_value)

    X_scale_dataset = X_scaler.fit_transform(X_value)
    y_scale_dataset = y_scaler.fit_transform(y_value)

    dump(X_scaler, open(ProcessedFilesDir+ preFix+'X_scaler.pkl', 'wb'))
    dump(y_scaler, open(ProcessedFilesDir+ preFix+'y_scaler.pkl', 'wb'))

    # Reshape the data
    '''Set the data input steps and output steps, 
        we use 30 days data to predict 1 day price here, 
        reshape it to (None, input_step, number of features) used for LSTM input'''
    n_steps_in = 3
    n_features = X_value.shape[1]
    n_steps_out = 1

    # Get data and check shape ##################################################
    X, y, yc = get_X_y(X_scale_dataset, y_scale_dataset, n_steps_in, n_steps_out)
    # ###########################################################################
    X_train, X_test, = split_train_test(X,X)
    y_train, y_test, = split_train_test(y,X)
    yc_train, yc_test, = split_train_test(yc,X)
    index_train, index_test, = predict_index(dataset, X_train, n_steps_in, n_steps_out)

    # %% - Save dataset -----------------------------------------------------------------
    print('X shape: ', X.shape)
    print('y shape: ', y.shape)
    print('X_train shape: ', X_train.shape)
    print('y_train shape: ', y_train.shape)
    print('y_c_train shape: ', yc_train.shape)
    print('X_test shape: ', X_test.shape)
    print('y_test shape: ', y_test.shape)
    print('y_c_test shape: ', yc_test.shape)
    print('index_train shape:', index_train.shape)
    print('index_test shape:', index_test.shape)

    np.save(ProcessedFilesDir+ preFix+"_X_train.npy", X_train)
    np.save(ProcessedFilesDir+ preFix+"_y_train.npy", y_train)
    np.save(ProcessedFilesDir+ preFix+"_X_test.npy", X_test)
    np.save(ProcessedFilesDir+ preFix+"_y_test.npy", y_test)
    np.save(ProcessedFilesDir+ preFix+"_yc_train.npy", yc_train)
    np.save(ProcessedFilesDir+ preFix+"_yc_test.npy", yc_test)
    np.save(ProcessedFilesDir+ preFix+'_index_train.npy', index_train)
    np.save(ProcessedFilesDir+ preFix+'_index_test.npy', index_test)
    np.save(ProcessedFilesDir+ preFix+'_train_predict_index.npy', index_train)
    np.save(ProcessedFilesDir+ preFix+'_test_predict_index.npy', index_test)


# Get X/y dataset
def get_X_y(X_data, y_data, n_steps_in, n_steps_out):
    X = list()
    y = list()
    yc = list()
    length = len(X_data)
    for i in range(0, length, 1):
        X_value = X_data[i: i + n_steps_in][:, :]
        y_value = y_data[i + n_steps_in: i + (n_steps_in + n_steps_out)][:, 0]
        yc_value = y_data[i: i + n_steps_in][:, :]
        if len(X_value) == 3 and len(y_value) == 1:
            X.append(X_value)
            y.append(y_value)
            yc.append(yc_value)

    return np.array(X), np.array(y), np.array(yc)

# get the train test predict index
def predict_index(dataset, X_train, n_steps_in, n_steps_out):

    # get the predict data (remove the in_steps days)
    train_predict_index = dataset.iloc[n_steps_in : X_train.shape[0] + n_steps_in + n_steps_out - 1, :].index
    test_predict_index = dataset.iloc[X_train.shape[0] + n_steps_in:, :].index

    return train_predict_index, test_predict_index


# Split train/test dataset
def split_train_test(data, X):
    train_size = round(len(X) * 0.7)
    data_train = data[0:train_size]
    data_test = data[train_size:]
    return data_train, data_test


# 프로그램 시작처리
if __name__ == '__main__':
    print('################ Data PreProcessing #########################')
    dataProcess("Solar")
    dataProcess("Wind")
