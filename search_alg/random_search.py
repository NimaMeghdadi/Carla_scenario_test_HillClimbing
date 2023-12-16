import neural_network
import random
import matplotlib.pyplot as plt

import neural_network 
class RandomSearch():
    def __init__(self):
        pass
    def optimize(self,distance_ped_starts,speed_cars,speed_peds,iteration = 0,x=""):
        nn = neural_network.mlpregressor.MlpRegressor()
        if x== "" : x = [random.choice(speed_cars),random.choice(distance_ped_starts),random.choice(speed_peds)]
        y = nn.predict(x,name_model = "collision_distance_model.pickle" )
        y1 = nn.predict(x,name_model = "collision_time_model.pickle")
        
        selected_y = [y]
        selected_y1 = [y1]
        
        for _ in range(iteration):
            x_rand = [random.choice(speed_cars),random.choice(distance_ped_starts),random.choice(speed_peds)]
            y_rand = nn.predict(list(x_rand),name_model = "collision_distance_model.pickle")
            y1_rand = nn.predict(list(x_rand),name_model = "collision_time_model.pickle")
            if  y_rand < y and y1_rand < y1:
                x = x_rand
                y = y_rand
                y1=y1_rand
                improve = True
            selected_y.append(y)
            selected_y1.append(y1)
        
        # plt.plot(selected_y, label = "Distance to collision")
        # plt.plot(selected_y1, label = "Time to collision")
        # plt.title("Random Search")
        # plt.xlabel("Iteration")
        # plt.ylabel("Distance car stops")
        # plt.legend() 
        # plt.show()
        return x,selected_y,selected_y1