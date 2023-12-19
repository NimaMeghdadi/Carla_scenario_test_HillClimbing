import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import pickle
from sklearn.preprocessing import MinMaxScaler

import constant
class MlpRegressor:
    def __init__(self):
        pass
    def train(self, name_csv= "result.csv",iterations=100,hidden_layer_size=(100,50),
              y_name="collision_distance",param_no=4,save_name="collision_distance"):
        # Read data from csv
        df = pd.read_csv(constant.DATA_DIR + name_csv)
        y_no = df.shape[1] - param_no
        x = df.drop(columns=df.columns[0:y_no], axis=1)
        y = df[y_name]
        trainX, testX, trainY, testY = train_test_split(x, y, test_size = 0.2)
        # print("trainX.shape",trainX.head())
        # Scale data
        sc=MinMaxScaler()
        scaler = sc.fit(trainX)
        trainX_scaled = scaler.transform(trainX)
        testX_scaled = scaler.transform(testX)
        # Train model
        mlp_reg = MLPRegressor(hidden_layer_sizes=hidden_layer_size,
                       max_iter = iterations,activation = 'relu',
                       solver = 'adam')
        mlp_reg.fit(trainX_scaled, trainY)
        # mlp_reg.predict(testX_scaled)
        print(mlp_reg.score(testX_scaled, testY))
        self.save_model(mlp_reg,name=save_name)
        self.save_model(scaler,name="scaler")
        return mlp_reg

    def save_model(self,model,name =""):
        print("saving model")
        filename = constant.MODEL_DIR + "{}.pickle".format(name)
        pickle.dump(model, open(filename, "wb"))

    # def load_model(self,name="collision_distance_model.pickle"):
    #     filename = constant.MODEL_DIR + name
    #     loaded_model = pickle.load(open(filename, "rb"))
    #     return loaded_model

    # def model_predict(self,data,name_model="",param_no=3):
    #     print("data",data)
    #     # Load model
    #     if name_model == "":
    #         model = self.load_model()
    #     else:
    #         model = self.load_model(name=name_model)
    #     # Scale data
    #     sc = self.load_model(name="scaler.pickle")
    #     data = np.array(data)
    #     norm_data = sc.transform([data])
    #     print("norm_data",norm_data)
        
    #     # Predict
    #     pred = model.predict(norm_data)
    #     if pred < 0:
    #         pred = 0
    #     else:
    #         pred = pred[0]
    #     return pred
