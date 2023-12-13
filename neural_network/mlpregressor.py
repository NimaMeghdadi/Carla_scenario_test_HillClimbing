import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import pickle

import constant
class MlpRegressor:
    def __init__(self):
        pass
    def train(self, name_csv= "result.csv",iterations=300,hidden_layer_size=(150,100,50),y_name="collision_distance",param_no=3):
        df = pd.read_csv(constant.DATA_DIR + name_csv)
        y_no = df.shape[1] - param_no
        x = df.drop(columns=df.columns[0:y_no], axis=1)
        y = df[y_name]
        trainX, testX, trainY, testY = train_test_split(x, y, test_size = 0.2)

        sc=StandardScaler()

        scaler = sc.fit(trainX)
        trainX_scaled = scaler.transform(trainX)
        testX_scaled = scaler.transform(testX)

        mlp_reg = MLPRegressor(hidden_layer_sizes=hidden_layer_size,
                       max_iter = iterations,activation = 'relu',
                       solver = 'adam')

        mlp_reg.fit(trainX_scaled, trainY)

        self.save_model(mlp_reg,name=y_name)

        return mlp_reg

    def save_model(self,model,name =""):
        print("saving model")
        filename = constant.MODEL_DIR + "{}_model.pickle".format(name)
        pickle.dump(model, open(filename, "wb"))

    def load_model(self,name="collision_distance_model.pickle"):
        print("loading model")
        
        filename = constant.MODEL_DIR + name
        loaded_model = pickle.load(open(filename, "rb"))
        return loaded_model

    def predict(self,data,name_model="",name_csv='result.csv',param_no=3):
        if name_model == "":
            model = self.load_model()
        else:
            model = self.load_model(name=name_model)
        df = pd.read_csv(constant.DATA_DIR + name_csv)
        y_no = df.shape[1] - param_no 
        trainX =  df.drop(columns=df.columns[0:y_no], axis=1)
        sc = StandardScaler()
        scaler = sc.fit(trainX)
        norm_data = scaler.transform([data])
        pred = model.predict(norm_data)
        if pred < 0:
            pred = 0
        else:
            pred = pred[0]
        return pred
