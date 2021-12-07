import warnings

import pywt

import data.excelLoader as el
import data.dataLoader as dl
import os
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import math

#el.read_weather_data_from_excel(base_dir, None)

sqlTextWindBelgium = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20160101' AND '20210401' "


sqlTextWindBelgiumAll = "SELECT	SUBSTR(TIME_ID,1,12) AS DATE," \
          "	WIND_PW AS PW," \
          "	WIND_PW_CAPA AS CAPA," \
          "	TEMP_MAX, " \
          "	TEMP_MIN, " \
          "	RADIATION " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20160101' AND '20210401' "

sqlTextSolarBelgium = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	SOLAR_PW AS PW," \
          "	SOLAR_PW_CAPA AS CAPA," \
          "	TEMP_MAX " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20160101' AND '20210401' "


sqlTextSolarBelgiumAll = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	SOLAR_PW AS PW," \
          "	SOLAR_PW_CAPA AS CAPA," \
          "	TEMP_MAX, " \
          "	TEMP_MIN, " \
          "	RADIATION " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20160101' AND '20210401' "


sqlTextBelgiumEnergyAll = "SELECT SUBSTR(TIME_ID,1,12) AS DATE," \
          "	SOLAR_PW + WIND_PW AS PW," \
          "	SOLAR_PW_CAPA + WIND_PW_CAPA AS CAPA," \
          "	SOLAR_PW AS SOLAR_PW," \
          "	SOLAR_PW_CAPA AS SOLAR_CAPA," \
          "	WIND_PW AS WIND_PW," \
          "	WIND_PW_CAPA AS WIND_CAPA," \
          "	TEMP_MAX, " \
          "	TEMP_MIN, " \
          "	RADIATION " \
          "FROM	AST0401 " \
          "WHERE	1 = 1	" \
          "AND TIME_ID BETWEEN '20160101' AND '20210401' "


sqlTextSolar2 = "SELECT CONCAT(REG_YMD,REG_HH24,REG_MM) AS DATE," \
             "           PW_P AS PW ," \
             "           CAPACITY_MW AS CAPA" \
             "          FROM AST0203" \
             "          WHERE REG_YMD BETWEEN '20061101' AND '20070201' ;"


base_dir="./DataFiles/"


def dataFileExists(target):
    result = False
    file_list = os.listdir(base_dir)

    for filename in file_list:
        if filename.endswith('.csv'):
            if filename == target:
                result = True
    return result


def windDataFileExists():
    result = False
    file_list = os.listdir(base_dir)

    for filename in file_list:
        if filename.endswith('.csv'):
            if filename == "WindData.csv":
                result = True

    return result


def solarDataFileExists():
    result = False
    file_list = os.listdir(base_dir)

    for filename in file_list:
        if filename.endswith('.csv'):
            if filename == "SolarData.csv":
                result = True
    return result


# init funciton, DownaLoad DB
def init():

    if windDataFileExists() is False:
        print(">Download Wind data From DB...")
        dl.dataLoadSQL(sqlTextWindBelgium, base_dir + "WindData.csv", indexSet=False)

    if dataFileExists("WindAllData.csv") is False:
        print(">Download Wind data From Wind All DB...")
        dl.dataLoadSQL(sqlTextWindBelgiumAll, base_dir + "WindAllData.csv", indexSet=False)

    if solarDataFileExists() is False:
        print(">Download Solar data From DB...")
        dl.dataLoadSQL(sqlTextSolarBelgium, base_dir + "SolarData.csv", indexSet=False)

    if dataFileExists("SolarAllData.csv") is False:
        print(">Download Wind data From Solar All DB...")
        dl.dataLoadSQL(sqlTextSolarBelgium, base_dir + "SolarAllData.csv", indexSet=False)

    if dataFileExists("BelgiumAllData.csv") is False:
        print(">Download Wind data From Belgium Energy All DB...")
        dl.dataLoadSQL(sqlTextBelgiumEnergyAll, base_dir + "BelgiumAllData.csv", indexSet=False)


def main():
    ## import data
    #df = pd.read_csv('windData.csv')
    figsizeSet = (15, 5)
    if windDataFileExists():
        dfWind = pd.read_csv(base_dir + 'WindData.csv')

        print(dfWind.head())
        print(dfWind.tail())
        print(dfWind.shape)
        print(dfWind.columns)

        fig, ax = plt.subplots(figsize=figsizeSet)
        ax.plot(dfWind.index, dfWind['PW'], label='Wind Power')
        ax.set(xlabel="15min",
               ylabel="MW",
               title="Wind Power Belgium(2016-2021)")
        plt.tight_layout()
        plt.show()

        fig, ax = plt.subplots(figsize=figsizeSet)
        ax.plot(dfWind.index, dfWind['PW'], label='Wind Power')
        ax.plot(dfWind.index, dfWind['CAPA'], label='Power Installation')
        ax.set(xlabel="15min",
               ylabel="MW",
               title="Wind Power Belgium(2016-2021) && Installation")
        plt.tight_layout()
        plt.show()

        fftDataProcess(dfWind, base_dir+"WindDataFFT.csv")


    if solarDataFileExists():
        dfSolar = pd.read_csv(base_dir + 'SolarData.csv')
        fig, ax = plt.subplots(figsize=figsizeSet)
        ax.plot(dfSolar.index, dfSolar['PW'], label='Solar Power')
        ax.set(xlabel="15min",
               ylabel="MW",
               title="Solar Power Belgium(2016-2021)")
        plt.tight_layout()
        plt.show()

        fig, ax = plt.subplots(figsize=figsizeSet)
        ax.plot(dfSolar.index, dfSolar['PW'], label='Solar Power')
        ax.plot(dfSolar.index, dfSolar['CAPA'], label='Power Installation')
        ax.set(xlabel="15min",
               ylabel="MW",
               title="Solar Power Belgium(2016-2021) && Installation")
        plt.tight_layout()
        plt.show()

        fftDataProcess(dfSolar, base_dir+"SolarDataFFT.csv")

    if dataFileExists("BelgiumAllData.csv"):
        dfData = pd.read_csv(base_dir + 'BelgiumAllData.csv')
        fig, ax = plt.subplots(figsize=figsizeSet)
        ax.plot(dfData.index, dfData['PW'], label='Solar+Wind Power')
        ax.plot(dfData.index, dfData['CAPA'], label='Installed Solar+Wind Power')
        ax.set(xlabel="15min",
               ylabel="MW",
               title="Solar+Wind  Power Belgium(2016-2021)")
        plt.tight_layout()
        plt.show()

        fig, ax = plt.subplots(figsize=figsizeSet)
        ax.plot(dfData.index, dfData['TEMP_MAX'], label='Temperatures Max')
        ax.plot(dfData.index, dfData['TEMP_MIN'], label='Temperatures Min')

        # ax.plot(dfSolar.index, dfSolar['TEMP_MAX'], label='Temp Max')
        ax.set(xlabel="Days(15min Points)",
               ylabel="degree",
               title="Belgium Temperature(2016-2021)")
        # date_form = DateFormatter("%Y%m%d%H%M")
        # ax.xaxis.set_major_formatter(date_form)
        plt.legend()
        plt.tight_layout()
        plt.show()

        fig, ax = plt.subplots(figsize=figsizeSet)
        ax.plot(dfData.index, dfData['RADIATION'], label='RADIATION MAX PER DAY')
        # ax.plot(dfSolar.index, dfSolar['TEMP_MAX'], label='Temp Max')
        ax.set(xlabel="Days(15min Points)",
               ylabel="W/M",
               title="Belgium RADIATION(2016-2021)")
        # date_form = DateFormatter("%Y%m%d%H%M")
        # ax.xaxis.set_major_formatter(date_form)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # db1 = pywt.Wavelet('db1')
        # (cA2, cD2), (cA1, cD1) = pywt.swt(dfData['PW'] / 6000 , db1, level=2)
        # ax.plot(dfData.index, cA2, label='Wavelet cA2')
        # ax.plot(dfData.index, cD2, label='Wavelet cD2')
        # ax.plot(dfData.index, cA1, label='Wavelet cA1')
        # ax.plot(dfData.index, cD1, label='Wavelet cD1')
        # plt.show()

        fftDataProcess(dfSolar, base_dir+"BelgiumAllDataFFT.csv")



def fftDataProcess(df, filename):

    warnings.filterwarnings(action='ignore') # waring ignore
    df_technicalIndicated = get_technical_indicators(df)
    warnings.filterwarnings(action='default') # waring ignore

    dataset = df_technicalIndicated.iloc[20:, :].reset_index(drop=True)
    datasetFFT = get_fourier_transfer(dataset)

    dataJoined = pd.concat([dataset, datasetFFT], axis=1)
    # print(Final_data.head())
    dataJoined.to_csv(filename, index=False)

    # show indicator plot
    plot_technical_indicators(df_technicalIndicated, 17000)
    # show ifft plot
    warnings.filterwarnings(action='ignore') # waring ignore
    plot_Fourier(dataset, filename)
    warnings.filterwarnings(action='default') # waring ignore

    convert_Wavelet(dataset, filename)



def get_technical_indicators(data):
    # # Create 7 and 21 days Moving Average
    # data['MA7'] = data.iloc[:, 1].rolling(window=7).mean()
    # data['MA21'] = data.iloc[:, 1].rolling(window=21).mean()
    # # Create MACD
    # data['MACD'] = data.iloc[:, 1].ewm(span=26).mean() - data.iloc[:,1].ewm(span=12,adjust=False).mean()
    # # Create Bollinger Bands
    # data['20SD'] = data.iloc[:, 1].rolling(20).std()
    # data['upper_band'] = data['MA21'] + (data['20SD'] * 2)
    # data['lower_band'] = data['MA21'] - (data['20SD'] * 2)

    data['MA1H'] = data.iloc[:, 1].rolling(window=4).mean()
    data['MA1D'] = data.iloc[:, 1].rolling(window=96).mean()
    # Create MACD
    data['MACD'] = data.iloc[:,1].ewm(span=2496).mean() - data.iloc[:,1].ewm(span=1152,adjust=False).mean()
    # Create Bollinger Bands
    data['20SD'] = data.iloc[:, 1].rolling(1920).std()
    data['upper_band'] = data['MA1D'] + (data['20SD'] * 2)
    data['lower_band'] = data['MA1D'] - (data['20SD'] * 2)

    # Create Exponential moving average
    data['EMA'] = data.iloc[:,1].ewm(com=0.5).mean()
    # Create LogMomentum
    data['logmomentum'] = np.log(data.iloc[:,1] - 1)

    return data


def get_fourier_transfer(dataset):
    # Get the columns for doing fourier
    #data_FT = dataset[['IDX', 'PW']]
    dataset["IDX"] = dataset.index
    dataIndexed = dataset[["IDX", 'PW']]
    pw_fft = np.fft.fft(np.asarray(dataIndexed['PW'].tolist()))
    fft_df = pd.DataFrame({'fft': pw_fft})
    fft_df['absolute'] = fft_df['fft'].apply(lambda x: np.abs(x))
    fft_df['angle'] = fft_df['fft'].apply(lambda x: np.angle(x))
    fft_list = np.asarray(fft_df['fft'].tolist())

    fft_com_df = pd.DataFrame()

    for num_ in [3, 6, 9]:
        fft_list_m10 = np.copy(fft_list);
        fft_list_m10[num_:-num_] = 0
        fft_ = np.fft.ifft(fft_list_m10)
        fft_com = pd.DataFrame({'fft': fft_})
        fft_com['absolute of ' + str(num_) + ' comp'] = fft_com['fft'].apply(lambda x: np.abs(x))
        fft_com['angle of ' + str(num_) + ' comp'] = fft_com['fft'].apply(lambda x: np.angle(x))
        fft_com = fft_com.drop(columns='fft')
        fft_com_df = pd.concat([fft_com_df, fft_com], axis=1)
    return fft_com_df


def plot_technical_indicators(dataset, last_days):
    plt.figure(figsize=(16, 10), dpi=100)
    dataset = dataset.iloc[-last_days:, :]
    x_ = list(dataset.index)

    plt.plot(dataset['PW'], label='Power', color='b')

    # # Plot first subplot
    # plt.plot(dataset['MA7'], label='MA 7', color='g', linestyle='--')
    # plt.plot(dataset['MA21'], label='MA 21', color='r', linestyle='--')

    # Plot first subplot
    plt.plot(dataset['MA1H'], label='MA 1Hour', color='g', linestyle='--')
    plt.plot(dataset['MA1D'], label='MA 1Day', color='r', linestyle='--')

    plt.plot(dataset['upper_band'], label='Upper Band', color='c')
    plt.plot(dataset['lower_band'], label='Lower Band', color='c')
    plt.fill_between(x_, dataset['lower_band'], dataset['upper_band'], alpha=0.35)
    plt.title('Power Band'.format(last_days))
    plt.ylabel('Power MW')
    plt.legend()
    plt.legend()
    plt.show()


def plot_Fourier(dataset, plotname):
    data_FT = dataset[['IDX', 'PW']]
    #print(data_FT.info())
    PW_fft = np.fft.fft(np.asarray(data_FT['PW'].tolist()))
    fft_df = pd.DataFrame({'fft': PW_fft})
    fft_df['absolute'] = fft_df['fft'].apply(lambda x: np.abs(x))
    fft_df['angle'] = fft_df['fft'].apply(lambda x: np.angle(x))

    fft_list = np.asarray(fft_df['fft'].tolist())
    figsizeSet = (15, 5)
    plt.figure(figsize=figsizeSet, dpi=100)
    fft_list = np.asarray(fft_df['fft'].tolist())
    for num_ in [3, 6, 9]:
        fft_list_m10 = np.copy(fft_list);
        fft_list_m10[num_:-num_] = 0
        plt.plot(np.fft.ifft(fft_list_m10), label='Fourier transform with {} components'.format(num_))
    # plt.plot(data_FT['PW'], label='Real')
    plt.xlabel('Time Line(15min)')
    plt.ylabel('MW')
    if plotname is None:
        plotname = "Belgium Power Data: "
    else:
        plotname = "Belgium Power Data: " + plotname
    plt.title(plotname + 'Time Series Data(FFT> IFFT Components)')
    plt.tight_layout()
    plt.legend()
    plt.show()


def convert_Wavelet(dataset, filename):
    # dataset['row'] = dataset.reset_index().index # 인덱스를 읽어서 새로운 row 생성
    # dataset.set_index('row', inplace=True) # row를 새로운 인덱스로 설정
    if filename is not None:
        infoFile = filename
    else:
        infoFile = ''
    figsizeSet = (15, 5)

    # dataset.to_csv('origin.csv')
    # FFT 처리
    data_power = dataset[['IDX', 'PW']]
    npData_power = np.asarray(data_power['PW'].tolist())

    # Single Level dwt
    coeffs = pywt.dwt(npData_power, 'db1', 'smooth')
    cA, cD = coeffs
    A = pywt.idwt(cA, None, 'db1', 'smooth')
    D = pywt.idwt(None, cD, 'db1', 'smooth')

    plt.figure(figsize=figsizeSet)
    plt.plot(A, label='Wavelet A')
    plt.plot(D, label='Wavelet D')
    plt.title(infoFile + "DWT db1/smooth")
    plt.tight_layout()
    plt.legend()
    plt.show()

    # MultiLevel 2
    coeffsMultiLevel2 = pywt.wavedec(npData_power, 'db1', level=2)
    cA2, cD2, cD1 = coeffsMultiLevel2

    plt.figure(figsize=figsizeSet)
    plt.plot(cA2, label='Wavelet cA2')
    plt.plot(cD2, label='Wavelet cD2')
    plt.plot(cD1, label='Wavelet cD1')
    plt.title(infoFile + " DWT MultiLevel 2")
    plt.tight_layout()
    plt.legend()
    plt.show()

    # MultiLevel 3
    coeffsMultiLevel3 = pywt.wavedec(npData_power, 'db1', level=3)
    cA4, cD32, cD22, cD12 = coeffsMultiLevel3

    plt.figure(figsize=figsizeSet)
    plt.plot(cA4, label='Wavelet cA4', color='blue')
    plt.plot(cD32, label='Wavelet cD32', color='g')
    plt.plot(cD22, label='Wavelet cD22', color='r')
    plt.plot(cD12, label='Wavelet cD12', color='c')
    plt.title(infoFile + "DWT MultiLevel 3")
    plt.tight_layout()
    plt.legend()
    plt.show()

    # SWT MultiLevel 2
    db1 = pywt.Wavelet('db1')
    (cA2, cD2), (cA1, cD1) = pywt.swt(npData_power[1:], db1, level=2)

    plt.figure(figsize=figsizeSet)
    plt.plot(cA2, label='Wavelet cA2', color='blue')
    plt.plot(cD2, label='Wavelet cD2', color='g')
    plt.plot(cA1, label='Wavelet cA1', color='r')
    plt.plot(cD1, label='Wavelet cD1', color='c')
    plt.title(infoFile + "SWT(Stationary wavelet transform) MultiLevel 2")
    plt.tight_layout()
    plt.legend()
    plt.show()

    return



# 프로그램 시작처리
if __name__ == '__main__':
    print('################ LoadData To CSV #########################')
    init()
    main()
