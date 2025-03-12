# Copyright (c) Acconeer AB, 2022-2024
# All rights reserved

from acconeer.exptool import a121
import numpy as np
import matplotlib.pyplot as plt
import math
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
sensor_config.num_points = 15
sensor_config.sweeps_per_frame = 10
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


def process_complex_frame(complex_frame):
    
    # 복소수 데이터에서 I(실수부)와 Q(허수부) 값 추출
    i_values = np.real(complex_frame)
    q_values = np.imag(complex_frame)
    
    # 크기(magnitude) 계산
    magnitude = np.abs(complex_frame)
    
    # 위상(phase) 계산
    phase = np.angle(complex_frame)
    
    return {
        'i_values': i_values,
        'q_values': q_values,
        'complex': complex_frame,
        'magnitude': magnitude,
        'phase': phase
    }

def convert_to_analog_signal(processed_data, method='magnitude'):
   
    if method == 'magnitude':
        
        signal = processed_data['magnitude'].flatten()
    elif method == 'phase':
        
        signal = processed_data['phase'].flatten()
    elif method == 'i_values':
        
        signal = processed_data['i_values'].flatten()
    elif method == 'q_values':
        
        signal = processed_data['q_values'].flatten()
    else:
        raise ValueError(f"지원되지 않는 변환 방법: {method}")
    
    # 신호 정규화 (-1 ~ 1 범위)
    max_abs = np.max(np.abs(signal))
    if max_abs > 0:
        normalized_signal = signal / max_abs
    else:
        normalized_signal = signal
    
    return normalized_signal

def plot_iq_data(processed_data):
    
    rows, cols = processed_data['i_values'].shape
    
    
    fig = plt.figure(figsize=(16, 12))
    
    # I/Q 좌표 평면에 데이터 점들 그리기
    ax1 = fig.add_subplot(221)
    for i in range(rows):
        for j in range(cols):
            ax1.plot(processed_data['i_values'][i, j], processed_data['q_values'][i, j], 'bo')
            ax1.text(processed_data['i_values'][i, j], processed_data['q_values'][i, j], 
                    f'({i},{j})', fontsize=8)
    ax1.set_title('I/Q data')
    ax1.set_xlabel('I (In-phase)')
    ax1.set_ylabel('Q (Quadrature)')
    ax1.grid(True)
    
    # Magnitude heatmap
    ax2 = fig.add_subplot(222)
    im2 = ax2.imshow(processed_data['magnitude'], cmap='viridis', interpolation='nearest')
    ax2.set_xlabel('distance point')
    ax2.set_ylabel('frame/swip')
    ax2.set_title('Magnitude')
    plt.colorbar(im2, ax=ax2)
    
    
    for i in range(rows):
        for j in range(cols):
            ax2.text(j, i, f'{processed_data["magnitude"][i, j]:.1f}',
                    ha='center', va='center', color='w', fontsize=8)
    
    # 3. Phase 2d heatmap
    ax3 = fig.add_subplot(223)
    im3 = ax3.imshow(processed_data['phase'], cmap='magma', interpolation='nearest', vmin=-np.pi, vmax=np.pi)
    ax3.set_xlabel('distance point')
    ax3.set_ylabel('frame/swip')
    ax3.set_title('Phase(Radian)')
    plt.colorbar(im3, ax=ax3)
    
    # 4. I Q lineplot
    ax4 = fig.add_subplot(224)
    x = np.arange(rows * cols)
    i_flat = processed_data['i_values'].flatten()
    q_flat = processed_data['q_values'].flatten()
    ax4.plot(x, i_flat, 'r-', label='I')
    ax4.plot(x, q_flat, 'b-', label='Q')
    ax4.set_title('I and Q')
    ax4.set_xlabel('sample Index')
    ax4.set_ylabel('value')
    ax4.legend()
    ax4.grid(True)
    
    plt.tight_layout()
    plt.savefig('plot_iq_data.png')

def plot_analog_signals(processed_data):
    
   
    methods = ['magnitude', 'phase', 'i_values', 'q_values']
    signals = {}
    
    for method in methods:
        signals[method] = convert_to_analog_signal(processed_data, method)
    
    
    plt.figure(figsize=(12, 10))
    
    x = np.arange(len(signals['magnitude']))
    
    for i, method in enumerate(methods, 1):
        plt.subplot(4, 1, i)
        plt.plot(x, signals[method])
        plt.title(f'analog_signal: ({method})')
        plt.xlabel('sample index')
        plt.ylabel('Amplitude(normalized)')
        plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('plot_analog_signal.png')
    #plt.show()
    
    return signals

# Now we are ready to start it:
client.start_session()

n = 1
results=[]
for i in range(n):
    # Data is retrieved from the sensor with "get_next".
    result = client.get_next()
    results.append(result.frame)
    print(f"Result {i + 1}:")
    print(result)

    
    

# When we are done, we should close the connection to the server.
client.close()

for result in results:
    processed_data = process_complex_frame(result)
    
    
    plot_iq_data(processed_data)
    
   
    signals = plot_analog_signals(processed_data)