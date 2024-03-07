import math
from DroneTerminal import Drone
from time import sleep


drone = Drone(connection_string='127.0.0.1:14550') # Connects to connection_string

drone.land_and_disarm()
drone.close_vehicle()