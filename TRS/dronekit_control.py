import dronekit
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil


connection_string = "127.0.0.1:14550"
# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string,wait_ready=True)

def arm():

    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode    = VehicleMode("GUIDED")    # Copter should arm in GUIDED mode
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

def get_grf_location():
    '''Use .lat .lon .alt | Returns the global relative frame (grf) location of the vehicle.'''
    return vehicle.location.global_relative_frame

def move(char):
    '''Moves a certain distance in specific directions: wasd'''
    if char == 'w': # FORWARD
        send_ned_velocity(1, 0, 0, 0.1) # W

    elif char == 'a': # LEFT
        send_ned_velocity(0, -1, 0, 0.1) # A
        
    elif char == 's': # BACKWARD
        send_ned_velocity(-1, 0, 0, 0.1) # S
    
    elif char == 'd': # RIGHT
        send_ned_velocity(0, 1, 0, 0.1) # D
    
    
    


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and flies to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode    = VehicleMode("GUIDED")    # Copter should arm in GUIDED mode
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(f"\r{vehicle.location.global_relative_frame.alt}", end="", flush=True)
        
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print("\nReached target altitude")
            break
        time.sleep(1)

def land_and_disarm():
    print("Intiating Landing sequence...")
    vehicle.mode = VehicleMode("LAND")


def close_vehicle():
    '''Close vehicle object before exiting script'''
    vehicle.close()
    print("Completed! EXITING...")

def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)


    # send command to vehicle on 1 Hz cycle
    for x in range(0,int(duration * 10)):
        vehicle.send_mavlink(msg)
        time.sleep(0.1)


def condition_yaw(heading: float, relative=False):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)




# arm_and_takeoff(4)
# print("Snoring for 5 seconds...")
# time.sleep(5)


# print("PIMP!")
# send_ned_velocity(1, 0, 0, 1) # W
# time.sleep(1)
# send_ned_velocity(0, 1, 0, 1) # D
# time.sleep(1)
# send_ned_velocity(0, -1, 0, 1) # A
# time.sleep(1)
# send_ned_velocity(-1, 0, 0, 1) # S
# time.sleep(1)

# land_and_disarm()
# close_vehicle()


# # Shut down simulator