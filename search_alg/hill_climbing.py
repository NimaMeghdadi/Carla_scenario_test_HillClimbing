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
    
    def optimize(self,distance_ped_starts,speed_cars,speed_peds):
        nn = neural_network.mlpregressor.MlpRegressor()
        # distance_ped_starts = np.linspace(9.0, 20.0, num=20)
        # speed_cars = np.linspace(30.8, 80.0, num=100)
        # speed_peds = np.linspace(0.2, 0.5, num=10)
        x_star = [random.choice(speed_cars),random.choice(distance_ped_starts),random.choice(speed_peds)]
        y_star = nn.predict(x_star)
        selected_neighbors = [y_star]
        print("type",type(x_star))
        print("init",x_star,y_star)
        while True:
            improve = False
            neighbors = self.generate_neighbor(x_star,speed_cars,distance_ped_starts,speed_peds)
            print("neighbors",neighbors)
            for i in range(len(neighbors)):
                neighbor , neighbors = self.select_random_delete(neighbors)
                y_neighbor = nn.predict(list(neighbor))
                print ("neighbor y_neighbor",list(neighbor),y_neighbor)
                y_star = nn.predict(x_star)
                print("y_neighbor,y_star",y_neighbor,y_star)
                if  y_neighbor < y_star:
                    x_star = neighbor
                    improve = True
                    selected_neighbors.append(y_neighbor)
            if not improve:
                break
        print("sel",selected_neighbors)
        plt.plot(selected_neighbors)
        plt.show()
        return x_star

    def read_csv(self,dir_csv_data='./result.csv'):
        with open(dir_csv_data, 'r') as file:
            csv_reader = csv.DictReader(file)
            data = [row for row in csv_reader]
        return data
    def generate_neighbor(self,x_star,speed_cars,distance_ped_starts,speed_peds):
        index_speed_car = np.where(speed_cars == x_star[0])[0][0]
        index_distance_ped_start = np.where(distance_ped_starts == x_star[1])[0][0]
        index_speed_ped = np.where(speed_peds == x_star[2])[0][0]
        
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

