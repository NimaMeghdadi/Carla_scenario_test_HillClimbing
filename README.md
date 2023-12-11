# Use of Hill Climbing Search for finding Crash scenarios in Autonomous Cars 

## A fully functional Example project written in python showing how to run hand made scenario in Carla and test the ADAS by Hill Climbing algorithm

This Repo try to search from car scenarios to find the crash scenario by Hill Climbing search Algorithm for better understanding this project is the simple implementation of this paper with Hill Climbing search Algorithm [paper](https://ieeexplore.ieee.org/document/7582746)

* create hand made scenario in Town01 of CARLA 0.9.13
* create Neural Network MLPRegressor to predict the distance of car when it stops for pedestrian.
* create Hill Climbing Algorithm for finding the min distance

## How to run this repo

1. clone this repo
2. instal dependency
3. instal [carla](https://carla.org/) 0.9.13 and install python package of carla
4. get additional carla [maps](https://github.com/carla-simulator/carla)
5. run carla 
6. run main.py

## Find a bug?

if you found an issue or would like to submit an improvement to this project pls submit issue using the issues tab above.

## Reference

#### change map

carla0.9.13\PythonAPI\util
python config.py --map Town01

#### pedestrian
Pedestrians and their implementation [youtube](https://www.youtube.com/watch?v=Uoz2ihDwaWA)

[carlawalker] (https://carla.readthedocs.io/en/latest/python_api/#carlawalker)

#### Vehicle
Positioning on the map [youtube](https://www.youtube.com/watch?v=f9NGX2T6bmY)

Inspect the vehicles [link](https://carla.readthedocs.io/en/latest/catalogue_vehicles/)

set destination [link](https://carla.readthedocs.io/en/0.9.12/adv_agents/)

#### NN
mlp [link](https://michael-fuchs-python.netlify.app/2021/02/10/nn-multi-layer-perceptron-regressor-mlpregressor/#introduction)