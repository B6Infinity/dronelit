from DroneTerminal import Drone
from time import sleep
import json

TOLERANCE = 12


coord_sequence = [] # Lat and Lons

print("Fetching coords from 'coord_log.json'...")
with open('coord_log.json', 'r') as f:
    d = json.load(f)
    for timestamp in d:
        coord = d[timestamp]
        coord_sequence.append(tuple(coord))

print(f'{len(coord_sequence)} coords found!')
print(coord_sequence)


drone = Drone() # Connects to connection_string
# drone = Drone(connection_string='127.0.0.1:14550')

# Initialise for Launch
drone.arm_and_takeoff(5)
sleep(1)


print(f"Starting journey... {len(coord_sequence)} spots to cover.")
i = 0
try:
    for coord in coord_sequence:
        i+=1
    
        drone.goto_gps(coord)

        try:
            while True:
                x, y = drone.get_gps_coords()
                errorx = abs(round((coord[0] - x) * 10 ** 6, 3))
                errory = abs(round((coord[1] - y) * 10 ** 6, 3))

                # print(f"\r{coord}  | {(x, y)}  | {(errorx, errory)}", end="", flush=True)

                if errorx + errory < 12:
                    print("Lock acquired! Sleeping for 5...")
                    sleep(5)
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            print(f"\nMoved to point {i}...")


except KeyboardInterrupt:
    pass


print("Sending RTL!")
drone.rtl()

drone.close_vehicle()