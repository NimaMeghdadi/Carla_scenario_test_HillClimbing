import random
import csv
import sys
import numpy as np
import itertools
from itertools import permutations
import random
import matplotlib.pyplot as plt
import pickle   
import constant
sys.path.append('E:\GitHub\Carla_scenario_test_HillClimbing')
import neural_network 

class HillClimbing:
# class HillClimbing:
    def __init__(self):
        pass

    def optimize(self,distance_ped_starts,speed_cars,speed_peds,x="",no_model = ""):
        # nn = neural_network.mlpregressor.MlpRegressor()
        nn_distance = pickle.load(open(constant.MODEL_DIR+"collision_distance{}_model.pickle".format(no_model), "rb"))
        nn_time = pickle.load(open(constant.MODEL_DIR+"collision_time{}_model.pickle".format(no_model), "rb"))
        if x== "" : x = [random.choice(speed_cars),random.choice(distance_ped_starts),random.choice(speed_peds)]
        scaler = pickle.load(open(constant.MODEL_DIR+"scaler.pickle", "rb"))
        x_scaled = scaler.transform([x])
        y_distance = nn_distance.predict(x_scaled)
        y_time = nn_time.predict(x_scaled)
        
        selected_y_distance = [y_distance]
        selected_y_time = [y_time]
        # start hill climbing
        while True:
            improve = False
            neighbors = self.generate_neighbor(x,speed_cars,distance_ped_starts,speed_peds)
            for _ in neighbors:
                neighbor , neighbors = self.select_random_delete(neighbors)
                reshaped_array = np.concatenate(neighbor, axis=0).reshape(1, -1)
                x_scaled = scaler.transform(reshaped_array)
                y_distance_negh = nn_distance.predict(list(x_scaled))
                y_time_negh = nn_time.predict(list(x_scaled))
                if  y_distance_negh < y_distance and y_time_negh < y_time:
                    x = neighbor
                    y_distance = y_distance_negh
                    y_time=y_time_negh
                    improve = True
                    selected_y_distance.append(y_distance_negh)
                    selected_y_time.append(y_time_negh)

            if not improve:
                break
        return x,selected_y_distance,selected_y_time

    def read_csv(self,dir_csv_data='./result.csv'):
        with open(dir_csv_data, 'r') as file:
            csv_reader = csv.DictReader(file)
            data = [row for row in csv_reader]
        return data
    
    def generate_neighbor(self,x,speed_cars,distance_ped_starts,speed_peds):
        index_speed_car = np.where(speed_cars == x[0])[0]
        index_distance_ped_start = np.where(distance_ped_starts == x[1])[0]
        index_speed_ped = np.where(speed_peds == x[2])[0]

        res_speed_cars = []
        res_distance_ped_starts = []
        res_speed_peds = []
        
        if len(distance_ped_starts)-1 >= index_distance_ped_start+1 : res_distance_ped_starts.append(distance_ped_starts[index_distance_ped_start+1])
        if 0 <= index_distance_ped_start-1: res_distance_ped_starts.append(distance_ped_starts[index_distance_ped_start-1])
        res_distance_ped_starts.append(distance_ped_starts[index_distance_ped_start])
        if len(speed_cars)-1 >= index_speed_car+1: res_speed_cars.append(speed_cars[index_speed_car+1]) 
        if 0 <= index_speed_car-1: res_speed_cars.append(speed_cars[index_speed_car-1]) 
        res_speed_cars.append(speed_cars[index_speed_car]) 
        if len(speed_peds)-1 >= index_speed_ped+1: res_speed_peds.append(speed_peds[index_speed_ped+1])
        if 0 <= index_speed_ped-1: res_speed_peds.append(speed_peds[index_speed_ped-1])
        res_speed_peds.append(speed_peds[index_speed_ped])

        all_res = [res_speed_cars,res_distance_ped_starts,res_speed_peds]
        
        combinations = list(itertools.product(*all_res))
        return combinations


    def select_random_delete(self,neighbors):
        random_index = random.randint(0, len(neighbors) - 1)
        random_element = neighbors[random_index]
        neighbors.pop(random_index)
        return random_element ,neighbors