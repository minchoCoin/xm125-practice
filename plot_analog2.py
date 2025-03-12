# Copyright (c) Acconeer AB, 2022-2024
# All rights reserved

from acconeer.exptool import a121
import numpy as np
import matplotlib.pyplot as plt
import math

NUM_POINTS=15
SWEEP_PER_FRAME=10
HWAAS=16

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
sensor_config.num_points = NUM_POINTS
sensor_config.sweeps_per_frame = SWEEP_PER_FRAME
sensor_config.hwaas = HWAAS
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
import numpy as np
import matplotlib.pyplot as plt
import os

class A121Visualizer:
    def __init__(self, num_points=15, sweeps_per_frame=10, hwaas=16):
       
        self.num_points = num_points
        self.sweeps_per_frame = sweeps_per_frame
        self.hwaas = hwaas
        
        
        
    
    def process_frame_data(self, frame_data):
        # 입력 데이터가 1D 배열이면 재구성
        if frame_data.ndim == 1:
            if len(frame_data) == self.sweeps_per_frame * self.num_points:
                frame_data = frame_data.reshape(self.sweeps_per_frame, self.num_points)
            else:
                raise ValueError(f"입력 데이터 길이 ({len(frame_data)})가 예상된 크기 ({self.sweeps_per_frame * self.num_points})와 일치하지 않습니다.")
        
        # 복소수 데이터인 경우 크기와 위상 계산
        if np.iscomplexobj(frame_data):
            magnitude = np.abs(frame_data)
            phase = np.angle(frame_data)
            i_values = np.real(frame_data)
            q_values = np.imag(frame_data)
        
        
        return {
            'complex': frame_data if np.iscomplexobj(frame_data) else None,
            'magnitude': magnitude,
            'phase': phase,
            'i_values': i_values,
            'q_values': q_values
        }
    
    def plot_distance_line(self, processed_data):
        
        
        magnitude = processed_data['magnitude']
        phase = processed_data['phase']
        i_values = processed_data['i_values']
        q_values = processed_data['q_values']
        
        # x축 값 (거리 포인트 인덱스)
        x = np.arange(self.num_points)
        
        # 각 스윕별로 플롯 생성
        for sweep in range(self.sweeps_per_frame):
            # 하나의 그림에 4개의 서브플롯 생성
            fig, axs = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle(f'distance point of sweep {sweep+1}', fontsize=16)
            
            # I 값 플롯
            axs[0, 0].plot(x, i_values[sweep], 'r-', linewidth=2, marker='o')
            axs[0, 0].set_title('I values')
            axs[0, 0].set_xlabel('distance point')
            axs[0, 0].set_ylabel('values')
            axs[0, 0].grid(True)
            
            # Q 값 플롯
            axs[0, 1].plot(x, q_values[sweep], 'b-', linewidth=2, marker='o')
            axs[0, 1].set_title('Q values')
            axs[0, 1].set_xlabel('distance point')
            axs[0, 1].set_ylabel('values')
            axs[0, 1].grid(True)
            
            # Magnitude 플롯
            axs[1, 0].plot(x, magnitude[sweep], 'g-', linewidth=2, marker='o')
            axs[1, 0].set_title('Magnitude')
            axs[1, 0].set_xlabel('distance point')
            axs[1, 0].set_ylabel('values')
            axs[1, 0].grid(True)
            
            # Phase 플롯
            axs[1, 1].plot(x, phase[sweep], 'm-', linewidth=2, marker='o')
            axs[1, 1].set_title('Phase (radian)')
            axs[1, 1].set_xlabel('distance point')
            axs[1, 1].set_ylabel('values')
            axs[1, 1].grid(True)
            
            plt.tight_layout()
            plt.subplots_adjust(top=0.9)
            
            # 파일로 저장
            plt.savefig(f'./distance_point/distance_of_swip_{sweep+1}.png', dpi=300)
            plt.close(fig)
            
    
    def plot_sweep_line(self, processed_data):
       
        # 데이터 추출
        magnitude = processed_data['magnitude']
        phase = processed_data['phase']
        i_values = processed_data['i_values']
        q_values = processed_data['q_values']
        
        
        x = np.arange(self.sweeps_per_frame)
        
        
        for point in range(self.num_points):
            
            fig, axs = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle(f'sweep of distance point  {point+1}', fontsize=16)
            
            # I 값 플롯
            axs[0, 0].plot(x, i_values[:, point], 'r-', linewidth=2, marker='o')
            axs[0, 0].set_title('I values')
            axs[0, 0].set_xlabel('sweep')
            axs[0, 0].set_ylabel('values')
            axs[0, 0].grid(True)
            
            # Q 값 플롯
            axs[0, 1].plot(x, q_values[:, point], 'b-', linewidth=2, marker='o')
            axs[0, 1].set_title('Q values')
            axs[0, 1].set_xlabel('sweep')
            axs[0, 1].set_ylabel('values')
            axs[0, 1].grid(True)
            
            # Magnitude 플롯
            axs[1, 0].plot(x, magnitude[:, point], 'g-', linewidth=2, marker='o')
            axs[1, 0].set_title('Magnitude')
            axs[1, 0].set_xlabel('sweep')
            axs[1, 0].set_ylabel('values')
            axs[1, 0].grid(True)
            
            # Phase 플롯
            axs[1, 1].plot(x, phase[:, point], 'm-', linewidth=2, marker='o')
            axs[1, 1].set_title('Phase (radian)')
            axs[1, 1].set_xlabel('sweep')
            axs[1, 1].set_ylabel('values')
            axs[1, 1].grid(True)
            
            plt.tight_layout()
            plt.subplots_adjust(top=0.9)
            
            # 파일로 저장
            
            plt.savefig(f'./sweep/sweep_of_distance_point_{point+1}.png', dpi=300)
            plt.close(fig)
            
    
    
# Now we are ready to start it:
client.start_session()

n = 1
results=[]
for i in range(n):
    # Data is retrieved from the sensor with "get_next".
    result = client.get_next()
    print(result)
    results.append(result.frame)

# When we are done, we should close the connection to the server.
client.close()


for result in results:
     # 시각화 객체 생성
    visualizer = A121Visualizer(
        num_points=NUM_POINTS,
        sweeps_per_frame=SWEEP_PER_FRAME,
        hwaas=HWAAS,
       
    )
    processed_data = visualizer.process_frame_data(result)
    visualizer.plot_distance_line(processed_data)
    visualizer.plot_sweep_line(processed_data)