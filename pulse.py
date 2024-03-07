from DroneTerminal import Drone
from time import sleep


drone = Drone(connection_string='127.0.0.1:14550') # Connects to connection_string

print("Takeoff!")
drone.arm_and_takeoff(5)
sleep(1)
print("RTL!")
drone.rtl()

drone.close_vehicle()

print("Closed!")