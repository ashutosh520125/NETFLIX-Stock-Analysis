import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#load the data
NETFLIX = pd.read_csv('NETFLIX.csv')
print(NETFLIX['Volume'])


#create the simple moving average with a 30 days window
SP30 = pd.DataFrame()
SP30['Close'] = NETFLIX['Close'].rolling(window=30).mean()
SP100 = pd.DataFrame()
SP100['Close'] = NETFLIX['Close'].rolling(window=100).mean()


#create a new data frame to store all the Data
data = pd.DataFrame()
data['NETFLIX'] = NETFLIX['Close']
data['SP30'] = SP30['Close']
data['SP100'] = SP100['Close']
#print(data)
#create a func to signal when to buy and sell the stock
def buy_sell(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):
        if data['SP30'][i] > data['SP100'][i]:
            if flag != 1:
                sigPriceBuy.append(data['NETFLIX'][i])
                sigPriceSell.append(np.nan)
                flag=1;
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SP30'][i] < data['SP100'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['NETFLIX'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return  (sigPriceBuy, sigPriceSell)


#store the buy and sell data into a variable
buy_sell_data = buy_sell(data)
data['Buy_Signal_Price'] = buy_sell_data[0]
data['Sell_Signal_Price'] = buy_sell_data[1]
#print(data)

#visualize the data and market trend of buy and sell
plt.figure(figsize=(12.5,5.5))
plt.plot(data['NETFLIX'], label='NETFLIX Close Price', alpha=0.5)
plt.plot(data['SP30'], label ='SP30', alpha=0.5)
plt.plot(data['SP100'], label ='SP100', alpha=0.5)
plt.scatter(data.index, data['Buy_Signal_Price'], label = 'Buy', marker = '^', color='green')
plt.scatter(data.index, data['Sell_Signal_Price'], label = 'Sell', marker = 'v', color='red')
plt.title('NETFLIX Close price history of buy and sell')
plt.xlabel('23 May, 2002 - 20 May, 2021')
plt.ylabel('Close Price')
plt.legend(loc='upper left')
plt.show()
