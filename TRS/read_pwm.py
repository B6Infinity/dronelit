from dronekit import connect


vehicle = connect('/dev/ttyACM0', wait_ready=True)
# vehicle = connect('127.0.0.1:14550')


print("Connected")

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

try:
    while True:
        print(f"\r{vehicle.channels[3]}   {vehicle.channels[5]}", end="", flush=True)
        # print(" Ch3 override: %s" % vehicle.channels[3])
        # print(" Ch5 override: %s" % vehicle.channels[5])
except KeyboardInterrupt:
    pass

vehicle.close()


