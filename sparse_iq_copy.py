# Copyright (c) Acconeer AB, 2023-2024
# All rights reserved

from __future__ import annotations

import acconeer.exptool as et
from acconeer.exptool import a121
from acconeer.exptool.a121._core.entities.configs.config_enums import PRF, IdleState, Profile
from acconeer.exptool.a121.algo.sparse_iq import AmplitudeMethod, Processor, ProcessorConfig
import matplotlib.pyplot as plt
import numpy as np
# sensor config
#https://docs.acconeer.com/en/latest/exploration_tool/api/a121.html

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



def main():
    args = a121.ExampleArgumentParser().parse_args()
    et.utils.config_logging(args)

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
    processor_config = ProcessorConfig()

    processor_config.amplitude_method = AmplitudeMethod.COHERENT  # Either COHERENT or FFTMAX
    sensor_id = 1

    sensor_config = a121.SensorConfig(
        sweeps_per_frame=8,
        sweep_rate=None,
        frame_rate=None,
        inter_frame_idle_state=IdleState.READY,
        inter_sweep_idle_state=IdleState.READY,
        continuous_sweep_mode=False,
        double_buffering=False,
        subsweeps=[
            # Generate 3 subsweep configurations
            a121.SubsweepConfig(start_point=70),
            a121.SubsweepConfig(),
            a121.SubsweepConfig(profile=Profile.PROFILE_2),
        ],
    )

    # Multiple subsweep configuration can be assigned in single group SensorConfig
    # through 'subweeps' fields shown above or in these way below
    sensor_config.subsweeps[0].num_points = 140
    sensor_config.subsweeps[1].prf = PRF.PRF_13_0_MHz

    # Create a SessionConfig with (e.g.) two groups SensorConfig
    # First group will contain multiple subsweeps, second group will contain single subsweep
    # Multiple group configurations are required when certain parameters cannot be configured in subsweep config
    session_config = a121.SessionConfig(
        [
            {
                sensor_id: sensor_config,
            },
            {
                sensor_id: a121.SensorConfig(
                    sweeps_per_frame=20,
                )
            },
        ],
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
        print(f'results {i} collected')
        i=i+1
    print("Disconnecting...")
    client.close()

    for i,result in enumerate(results):
        result_sensor_configs = processor.process(results=result)
        result_first_sensor_config = result_sensor_configs[0][sensor_id]
        result_third_subsweep = result_first_sensor_config[2]
        # Sparse IQ results contain amplitudes, phases, and distance velocity
        try:
            #print("Amplitudes results of 3rd subsweep from first group ")
            #print(result_third_subsweep.amplitudes)

            # sensor config
            #https://docs.acconeer.com/en/latest/exploration_tool/api/a121.html
            print("Distance velocity results of 1st subsweep from second group ")
            distance_velocity_map = result_sensor_configs[1][sensor_id][0].distance_velocity_map
            print(distance_velocity_map)
            print(f'size: {distance_velocity_map.shape}')
            # sensor config of 1st subsweep from second group is in session_config.groups[1][sensor_id]
            print(f'Maximum Measureable Distance: {session_config.groups[1][sensor_id].prf.mmd}')
            print(f'Maximum Unambiguous Range: {session_config.groups[1][sensor_id].prf.mur}')
            print(session_config.groups[1][sensor_id])
            
            x_axis_label = get_distance_axis(session_config.groups[1][sensor_id],distance_velocity_map)
            y_axis_label = get_velocity_axis(session_config.groups[1][sensor_id],result[1][sensor_id]._context.metadata.max_sweep_rate)

            plt.figure(figsize=(12, 8))
            
            plt.imshow(distance_velocity_map, aspect='auto', origin='lower', cmap='hot', interpolation='nearest',
               extent=[x_axis_label[0], x_axis_label[-1], y_axis_label[0], y_axis_label[-1]])
            plt.colorbar(label='Magnitude (dB)')
            plt.xlabel('Range (m)')
            plt.ylabel('Velocity (m/s)')
            plt.title(f'range-doppler heatmap (results {i})')
            plt.tight_layout()
            plt.savefig(f'./range_velocity_map/results{i}.png')
            
        except et.PGProccessDiedException:
            break

if __name__ == "__main__":
    main()
