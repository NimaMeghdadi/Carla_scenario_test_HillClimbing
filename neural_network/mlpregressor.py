import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.neural_network import MLPRegressor

from sklearn import metrics

from sklearn.model_selection import GridSearchCV

import pickle

class MlpRegressor:
    def __init__(self):
        pass
    def train(self, dir_csv_data='./result.csv',iterations=300,hidden_layer_size=(150,100,50)):
        df = pd.read_csv(dir_csv_data)
        # df = df.drop(["collision",'speed_car','distance_ped_start','speed_ped'], axis=1)
        # print(df)

        x = df.drop('collision', axis=1)
        y = df['collision']

        trainX, testX, trainY, testY = train_test_split(x, y, test_size = 0.2)

        sc=StandardScaler()

        scaler = sc.fit(trainX)
        trainX_scaled = scaler.transform(trainX)
        testX_scaled = scaler.transform(testX)

        mlp_reg = MLPRegressor(hidden_layer_sizes=hidden_layer_size,
                       max_iter = iterations,activation = 'relu',
                       solver = 'adam')

        mlp_reg.fit(trainX_scaled, trainY)
        
        self.save_model(mlp_reg)

        return mlp_reg

    def save_model(self,model,dir=""):
        filename = dir + "model.pickle"
        pickle.dump(model, open(filename, "wb"))
        
    def load_model(self,dir=""):
        filename = dir + "model.pickle"
        loaded_model = pickle.load(open(filename, "rb"))
        return loaded_model
    
    def predict(self,data,model="",dir_csv_data='./result.csv'):
        if model == "":
            model = self.load_model()
        df = pd.read_csv(dir_csv_data)
        trainX = df.drop('collision', axis=1)
        sc = StandardScaler()
        scaler = sc.fit(trainX)
        norm_data = scaler.transform([data])
        pred = model.predict(norm_data)
        if pred < 0:
            pred = 0
        else:
            pred = pred[0]
        return pred
