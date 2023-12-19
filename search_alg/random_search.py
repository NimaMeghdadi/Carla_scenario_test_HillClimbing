import neural_network
import random
import matplotlib.pyplot as plt
import pickle
import neural_network 
import constant
class RandomSearch():
    def __init__(self):
        pass
    def optimize(self,distance_ped_starts,speed_cars,speed_peds,iteration = 0,x="",no_model = ""):
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
        
        for _ in range(iteration):
            x_rand = [random.uniform(1,200),random.uniform(1,100),random.uniform(1,100)]
            x_scaled = scaler.transform([x_rand])
            y_distance_rand = nn_distance.predict(list(x_scaled))
            y_time_rand = nn_time.predict(list(x_scaled))
            if  y_distance_rand < y_distance or y_time_rand < y_time:
                x = x_rand
                y_distance = y_distance_rand
                y_time=y_time_rand
            selected_y_distance.append(y_distance)
            selected_y_time.append(y_time)
        
        # plt.plot(selected_y, label = "Distance to collision")
        # plt.plot(selected_y1, label = "Time to collision")
        # plt.title("Random Search")
        # plt.xlabel("Iteration")
        # plt.ylabel("Distance car stops")
        # plt.legend() 
        # plt.show()
        return x,selected_y_distance,selected_y_time