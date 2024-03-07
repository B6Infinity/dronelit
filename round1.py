import json
from DroneTerminal import Drone
from datetime import datetime


drone = Drone()

vehicle = drone.get_vehicle()


AUX_CHANNEL = 8 #!6 - SWD




# ----------------------------------------------DO NOT TOUCH-------------------------------------------------------------

@vehicle.on_message('RC_CHANNELS')
def RC_CHANNEL_listener(vehicle, name, message):

    set_rc(1, message.chan1_raw)
    set_rc(2, message.chan2_raw)
    set_rc(3, message.chan3_raw)
    set_rc(4, message.chan4_raw)
    set_rc(5, message.chan5_raw)
    set_rc(6, message.chan6_raw)
    set_rc(7, message.chan7_raw)
    set_rc(8, message.chan8_raw)
    vehicle.notify_attribute_listeners('channels', vehicle.channels)

def set_rc(channel_num, value):
    vehicle._channels._update_channel(str(channel_num), value)

# ----------------------------------------------DO NOT TOUCH-------------------------------------------------------------


try:
    clicked = False
    while True:

        val = vehicle.channels[f'{AUX_CHANNEL}']

        try:
            if val < 1500:
                clicked = False
            else: # Click
                if not clicked:
                    clicked = True
                    d = {}
                    try:
                        with open('coord_log.json', 'r') as f:
                            d = json.load(f)
                    except Exception as e:
                        print(e)
                    d[str(datetime.now())] = drone.get_gps_coords()
                    print(d)
                    with open('coord_log.json', 'w') as f:
                        json.dump(d, f)
        except TypeError:
            pass

        print(f"\r{val}", end="", flush=True)

except KeyboardInterrupt:
    drone.close_vehicle()
    print("\n\nClosed Vehicle Successfully!")
except Exception as e:
    print(e)
    drone.close_vehicle()

print("Exiting...")
