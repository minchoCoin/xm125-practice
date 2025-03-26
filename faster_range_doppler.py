# Copyright (c) Acconeer AB, 2022-2024
# All rights reserved
'''
acconeer-python-exploration-master\src\acconeer\exptool\a121\_core\entities\configs\sensor_config.py
@utils.no_dynamic_member_creation
class SensorConfig:
    """Sensor configuration

    The sensor config represents a 1-1 mapping to the RSS service config.

    By default, the sensor config holds a single :class:`SubsweepConfig`. The parameters defined by
    the subsweep config, like :attr:`start_point`, can be accessed via the sensor config. If
    multiple subsweeps are used, those parameters must be accessed via their respective subsweep
    configs.

    For example, a sensor config can be created like this:

    .. code-block:: python

        SensorConfig(sweeps_per_frame=16, start_point=123)

    Note that the :attr:`start_point` is implicitly set in the underlying subsweep config. If you
    want to explicitly set the subsweep config(s), you can do

    .. code-block:: python

        SensorConfig(
            sweeps_per_frame=16,
            subsweeps=[
                SubsweepConfig(start_point=123),
            ],
        )

    Parameters can also be accessed via the class attributes:

    .. code-block:: python

        sensor_config = SensorConfig()
        sensor_config.sweeps_per_frame = 16
        sensor_config.start_point = 123

    If you want to use multiple subsweeps with this style of setting/getting the attributes, you
    can do like this:

    .. code-block:: python

        sensor_config = SensorConfig(num_subsweeps=3)
        sensor_config.sweeps_per_frame = 16
        sensor_config.subsweeps[0].start_point = 123

    .. note::

        The sensor config does not control on which sensor it should be run. That is handled by
        the :class:`SessionConfig`.

    :param subsweeps:
        The list of subsweeps to initialize with. May not be combined with ``num_subsweeps``.
    :param num_subsweeps:
        Initialize with a given number of subsweeps. May not be combined with ``subsweeps``.
    :raises ValueError: If ``subsweeps`` and ``num_subsweeps`` are both given.
    :raises ValueError: If the given list of ``subsweeps`` is empty.
    :raises ValueError: If subsweeps parameters are both given implicitly and via ``subsweeps``.
    """

    MAX_HWAAS = SubsweepConfig.MAX_HWAAS

    _subsweeps: List[SubsweepConfig]

    _sweeps_per_frame: int
    _sweep_rate: Optional[float]
    _frame_rate: Optional[float]
    _continuous_sweep_mode: bool
    _double_buffering: bool
    _inter_frame_idle_state: IdleState
    _inter_sweep_idle_state: IdleState

    # Seems like there is a false positive where mypy confuses
    # the below descriptors (class members) of attrs.fields with __slots__ variables.
    start_point = subsweep_delegate_field(SubsweepConfig.start_point, type_=int)  # type: ignore[misc]
    num_points = subsweep_delegate_field(SubsweepConfig.num_points, type_=int)  # type: ignore[misc]
    step_length = subsweep_delegate_field(SubsweepConfig.step_length, type_=int)  # type: ignore[misc]
    profile = subsweep_delegate_field(SubsweepConfig.profile, type_=Profile)  # type: ignore[misc]
    hwaas = subsweep_delegate_field(SubsweepConfig.hwaas, type_=int)  # type: ignore[misc]
    receiver_gain = subsweep_delegate_field(SubsweepConfig.receiver_gain, type_=int)  # type: ignore[misc]
    enable_tx = subsweep_delegate_field(SubsweepConfig.enable_tx, type_=bool)  # type: ignore[misc]
    enable_loopback = subsweep_delegate_field(SubsweepConfig.enable_loopback, type_=bool)  # type: ignore[misc]
    phase_enhancement = subsweep_delegate_field(SubsweepConfig.phase_enhancement, type_=bool)  # type: ignore[misc]
    prf = subsweep_delegate_field(SubsweepConfig.prf, type_=PRF)

    def __init__(
        self,
        *,
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
    ) -> None:
        if subsweeps is not None and num_subsweeps is not None:
            msg = "It is not allowed to pass both `subsweeps` and `num_subsweeps`. Choose one."
            raise ValueError(msg)
        if subsweeps == []:
            msg = "Cannot pass an empty `subsweeps` list."
            raise ValueError(msg)
'''
from acconeer.exptool import a121
import acconeer.exptool as et
from acconeer.exptool.a121.algo.sparse_iq import AmplitudeMethod, Processor, ProcessorConfig
import numpy as np
import time
import matplotlib.pyplot as plt
def get_distance_axis(config,distance_velocity_map):
    #get distance range
    start_m=config.start_point * 0.0025
    step_m = config.step_length * 0.0025

    x_axis_label = [start_m + step_m * idx for idx in range(distance_velocity_map.shape[1])]
    return x_axis_label

def get_velocity_axis(config,max_sweep_rate):
    #c=299792458
    wavelength = 299792458.0 / 6e+10 / 2
    prf = config.prf.frequency
    
    pri = 1.0/prf

    if config.sweep_rate is not None:
        sweep_rate = config.sweep_rate
    else:
        sweep_rate = max_sweep_rate

    sweep_period = 1.0/sweep_rate

    v_max=wavelength / (4*sweep_period)
   
    
    velocities = np.linspace(-v_max, v_max, config.sweeps_per_frame)
    return velocities

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
processor_config = ProcessorConfig()

processor_config.amplitude_method = AmplitudeMethod.COHERENT  # Either COHERENT or FFTMAX
sensor_id = 1
# To be able to start a session, we must first configure the session
sensor_config = a121.SensorConfig()
sensor_config.num_points = 100
sensor_config.sweeps_per_frame = 10
sensor_config.step_length=3
sensor_config.hwaas = 16


# Now we are ready to start it:

session_config = a121.SessionConfig(
        [{sensor_id: sensor_config}],
        extended=True,
    )
client.setup_session(session_config)
client.start_session()
processor = Processor(session_config=session_config, processor_config=processor_config)
interrupt_handler = et.utils.ExampleInterruptHandler()
print("Press Ctrl-C to end session")
results=[]
i=0
while not interrupt_handler.got_signal:
    result = client.get_next()
    results.append(result)
    print(f'result {i} is collected at {time.process_time()} seconds')
    
    i=i+1
print("Disconnecting...")
client.close()

print("Distance velocity results of first group")

# sensor config of 1st subsweep from second group is in session_config.groups[1][sensor_id]
print(f'Maximum Measureable Distance: {session_config.groups[0][sensor_id].prf.mmd}')
print(f'Maximum Unambiguous Range: {session_config.groups[0][sensor_id].prf.mur}')
print(session_config.groups[0][sensor_id])
for i,result in enumerate(results):
        result_sensor_configs = processor.process(result)
        
        # Sparse IQ results contain amplitudes, phases, and distance velocity
        try:
            #print("Amplitudes results of 3rd subsweep from first group ")
            #print(result_third_subsweep.amplitudes)

            # sensor config
            #https://docs.acconeer.com/en/latest/exploration_tool/api/a121.html
            
            distance_velocity_map = result_sensor_configs[0][sensor_id][0].distance_velocity_map
            #print(distance_velocity_map)
            #print(f'size: {distance_velocity_map.shape}')
            
            x_axis_label = get_distance_axis(session_config.groups[0][sensor_id],distance_velocity_map)
            y_axis_label = get_velocity_axis(session_config.groups[0][sensor_id],result[0][sensor_id]._context.metadata.max_sweep_rate)

            plt.figure(figsize=(12, 8))
            
            plt.imshow(distance_velocity_map, aspect='auto', origin='lower', cmap='hot', interpolation='nearest',
               extent=[x_axis_label[0], x_axis_label[-1], y_axis_label[0], y_axis_label[-1]])
            plt.colorbar(label='Magnitude (dB)')
            plt.xlabel('Range (m)')
            plt.ylabel('Velocity (m/s)')
            plt.title(f'range-doppler heatmap (results {i})')
            plt.tight_layout()
            plt.savefig(f'./range_velocity_map/results{i}.png')
            print(f'figure {i} has been saved')
            plt.close()
            
        except et.PGProccessDiedException:
            break
