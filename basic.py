# Copyright (c) Acconeer AB, 2022-2024
# All rights reserved

from acconeer.exptool import a121


# Client is an object that is used to interact with the sensor.
client = a121.Client.open(
    # ip_address="<ip address of host (like a RPi). E.g. 192.168.XXX.YYY>",
    # or
    # serial_port="<serial port of module. E.g. COM3 or /dev/ttyUSBx for Window/Linux>",
    # or
    # usb_device=True,
    # or
    # mock=True,
    serial_port='COM4',
    override_baudrate=115200
)

# Once the client is connected, information about the server can be accessed.
print("Server Info:")
print(client.server_info)

# In order to get radar data from the server, we need to start a session.

# To be able to start a session, we must first configure the session
sensor_config = a121.SensorConfig()
sensor_config.num_points = 6
sensor_config.sweeps_per_frame = 4
sensor_config.hwaas = 16
client.setup_session(sensor_config)

'''
sensor config:
        subsweeps: Optional[list[SubsweepConfig]] = None,
        num_subsweeps: Optional[int] = None,
        sweeps_per_frame: int = 1,
        sweep_rate: Optional[float] = None,
        frame_rate: Optional[float] = None,
        continuous_sweep_mode: bool = False,
        double_buffering: bool = False,
        inter_frame_idle_state: IdleState = IdleState.DEEP_SLEEP,
        inter_sweep_idle_state: IdleState = IdleState.READY,
        start_point: Optional[int] = None,
        num_points: Optional[int] = None,
        step_length: Optional[int] = None,
        profile: Optional[Profile] = None,
        hwaas: Optional[int] = None,
        receiver_gain: Optional[int] = None,
        enable_tx: Optional[bool] = None,
        enable_loopback: Optional[bool] = None,
        phase_enhancement: Optional[bool] = None,
        prf: Optional[PRF] = None,

subsweeps: List of SubsweepConfig objects. Allows defining multiple subsweeps with different configurations (range, resolution, etc.) within a single frame.
num_subsweeps: Number of subsweeps to create with default settings. Used as an alternative to providing explicit subsweep configurations.
sweeps_per_frame: Number of sweeps that make up one frame. Higher values include more temporal samples in a single frame.
sweep_rate: Sweep frequency in Hz. Defines how many sweeps per second are performed.
frame_rate: Frame frequency in Hz. Defines how many frames per second are collected.
continuous_sweep_mode: When enabled, minimizes delays between sweeps for more continuous data acquisition.
double_buffering: Enables parallel processing of data collection and transmission for improved efficiency.
inter_frame_idle_state: Sensor's idle state between frames. Balances power saving and response time.
inter_sweep_idle_state: Sensor's idle state between sweeps within a frame.
start_point: Starting point for measurement (distance-related). Used for direct configuration instead of subsweeps.
num_points: Number of distance points to measure. Used for direct configuration instead of subsweeps.
step_length: Spacing between distance points. Used for direct configuration instead of subsweeps.
profile: Sensor profile preset that determines characteristics like sensitivity, speed, and accuracy.
hwaas (Hardware Accelerated Average Samples): Number of hardware-averaged samples. Higher values improve SNR (Signal-to-Noise Ratio) but increase power consumption.
receiver_gain: Receiver gain setting. Determines the amount of signal amplification.
enable_tx: Transmitter enable flag. Typically set to true to enable the transmitter.
enable_loopback: Loopback mode enable flag. Used for testing and diagnostic purposes.
phase_enhancement: Phase enhancement feature enable flag. Improves the quality of phase information.
prf (Pulse Repetition Frequency): Determines how frequently the radar emits pulses.
'''

# Now we are ready to start it:
client.start_session()

n = 5
for i in range(n):
    # Data is retrieved from the sensor with "get_next".
    result = client.get_next()

    print(f"Result {i + 1}:")
    print(result)

# When we are done, we should close the connection to the server.
client.close()
