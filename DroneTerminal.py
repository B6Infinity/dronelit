from dronekit import connect, VehicleMode, Vehicle, LocationGlobalRelative

from time import sleep



class Drone:
    '''Creates a terminal to interact with the drone connected (tries connecting to the 'connection_string' parameter)'''
    
    def __init__(self, connection_string = "/dev/ttyACM0") -> None:
        
        # sitl = dronekit_sitl.start_default()

        # connection_string = "127.0.0.1:14550"
        # connection_string = "/dev/ttyUSB0"
        self.connection_string = connection_string

        print(f"\nAttempting to connect on {connection_string}...")
        self.vehicle = connect(self.connection_string, wait_ready=True)
        print("Connection successful!")

    def get_vehicle(self): return self.vehicle


    # ----------------------
    def get_gps_coords(self) -> tuple:
        '''Returns the Lattitude and Longitude of the vehicle e.g. -> (23.1781203, 80.0227357)'''
        return (
            self.vehicle.location.global_relative_frame.lat, 
            self.vehicle.location.global_relative_frame.lon
        )
    
    def get_altitude(self) -> float: return self.vehicle.location.global_relative_frame.alt
    def get_vehicle_mode_name(self): return self.vehicle.mode.name
    
    def get_vitals(self) -> float:
        '''Returns the following in sequence:
        last_heartbeat
        battery.level
        '''
        return (
            self.vehicle.last_heartbeat,
            self.vehicle.battery.level
        )

    #-----------------------


    def arm_and_takeoff(self, targetAltitude):
        """
        Arms vehicle and flies to targetAltitude.
        """

        print("Basic pre-arm checks")
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            sleep(1)

        print("Arming motors")
        self.vehicle.mode    = VehicleMode("GUIDED")    # Copter should arm in GUIDED mode
        self.vehicle.armed   = True

        # Confirm vehicle armed before attempting to take off
        while not self.vehicle.armed:
            print("Waiting for arming...")
            sleep(1)

        print("Taking off!")
        self.vehicle.simple_takeoff(targetAltitude) # Take off to target altitude

        while True:
            print(f"\r{self.vehicle.location.global_relative_frame.alt}", end="", flush=True)
            
            if self.vehicle.location.global_relative_frame.alt>=targetAltitude*0.96:
                print("\nReached target altitude")
                break
            sleep(0.5)

    def goto_gps(self, coords : tuple):
        self.vehicle.simple_goto(LocationGlobalRelative(
            coords[0],
            coords[1],
            self.vehicle.location.global_relative_frame.alt,
        ))

    def rtl(self):
        self.vehicle.mode = VehicleMode("RTL")


    #-----------------------
    def land_and_disarm(self):
        print("Intiating Landing sequence...")
        self.vehicle.mode = VehicleMode("LAND")

    def close_vehicle(self):
        self.vehicle.close()