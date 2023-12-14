import random
import csv
import sys
import numpy as np
import itertools
from itertools import permutations
import random
import matplotlib.pyplot as plt

sys.path.append('E:\GitHub\Carla_scenario_test_HillClimbing')
import neural_network 

class HillClimbing:
# class HillClimbing:
    def __init__(self):
        pass

    def optimize(self,distance_ped_starts,speed_cars,speed_peds,model_name='collision_distance_model.pickle'):
        nn = neural_network.mlpregressor.MlpRegressor()
        # Init Random
        x = [random.choice(speed_cars),random.choice(distance_ped_starts),random.choice(speed_peds)]
        y = nn.predict(x,name_model = "collision_distance_model.pickle" )
        y1 = nn.predict(x,name_model = "collision_time_model.pickle")
        # Init selected neighbors
        selected_neighbors_y = [y]
        selected_neighbors_y1 = [y1]
        # start hill climbing

        while True:
            improve = False
            neighbors = self.generate_neighbor(x,speed_cars,distance_ped_starts,speed_peds)
            print("neighbors",neighbors)
            for i in range(len(neighbors)):
                neighbor , neighbors = self.select_random_delete(neighbors)
                y_neighbor = nn.predict(list(neighbor),name_model = "collision_distance_model.pickle")
                y1_neighbor = nn.predict(list(neighbor),name_model = "collision_time_model.pickle")
                if  y_neighbor < y and y1_neighbor < y1:
                    x = neighbor
                    y = y_neighbor
                    y1=y1_neighbor
                    improve = True
                    selected_neighbors_y.append(y_neighbor)
                    selected_neighbors_y1.append(y1_neighbor)
            if not improve:
                break
        # Plot
        plt.plot(selected_neighbors_y, label = "Distance to collision")
        plt.plot(selected_neighbors_y1, label = "Time to collision")
        plt.xlabel("Iteration")
        plt.ylabel("Distance car stops")
        plt.legend() 
        plt.show()
        return x

    def read_csv(self,dir_csv_data='./result.csv'):
        with open(dir_csv_data, 'r') as file:
            csv_reader = csv.DictReader(file)
            data = [row for row in csv_reader]
        return data
    def generate_neighbor(self,x,speed_cars,distance_ped_starts,speed_peds):
        index_speed_car = np.where(speed_cars == x[0])[0][0]
        index_distance_ped_start = np.where(distance_ped_starts == x[1])[0][0]
        index_speed_ped = np.where(speed_peds == x[2])[0][0]

        print(index_speed_car)
        print(index_distance_ped_start)
        print(index_speed_ped)

        res_speed_cars = []
        res_distance_ped_starts = []
        res_speed_peds = []
        if len(distance_ped_starts)-1 >= index_distance_ped_start+1 : res_distance_ped_starts.append(distance_ped_starts[index_distance_ped_start+1])
        if 0 <= index_distance_ped_start-1: res_distance_ped_starts.append(distance_ped_starts[index_distance_ped_start-1])
        if len(speed_cars)-1 >= index_speed_car+1: res_speed_cars.append(speed_cars[index_speed_car+1]) 
        if 0 <= index_speed_car-1: res_speed_cars.append(speed_cars[index_speed_car-1]) 
        if len(speed_peds)-1 >= index_speed_ped+1: res_speed_peds.append(speed_peds[index_speed_ped+1])
        if 0 <= index_speed_ped-1: res_speed_peds.append(speed_peds[index_speed_ped-1])

        all_res = [res_speed_cars,res_distance_ped_starts,res_speed_peds]
        combinations = list(itertools.product(*all_res))
        return combinations


    def select_random_delete(self,neighbors):
        random_index = random.randint(0, len(neighbors) - 1)
        random_element = neighbors[random_index]
        neighbors.pop(random_index)
        return random_element ,neighbors