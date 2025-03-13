# Copyright (c) Acconeer AB, 2022-2024
# All rights reserved

from acconeer.exptool import a121
import numpy as np
import matplotlib.pyplot as plt
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
'''
sensor_config = a121.SensorConfig()
sensor_config.start_point=25
sensor_config.step_length=2
sensor_config.num_points=30
sensor_config.hwaas = 10
client.setup_session(sensor_config)
'''

sensor_config = a121.SensorConfig()
sensor_config.num_points = 15
sensor_config.sweeps_per_frame = 10
sensor_config.hwaas = 16
client.setup_session(sensor_config)

# Now we are ready to start it:
client.start_session()

def custom_graph(result):
    # 실수부와 허수부 추출
    rows, cols = result.shape
    real_part = np.real(result)
    imag_part = np.imag(result)

    # 1. 2D 히트맵으로 실수부와 허수부 시각화
    plt.figure(figsize=(14, 6))

    # 실수부 히트맵
    plt.subplot(121)
    im1 = plt.imshow(real_part, cmap='viridis')
    plt.colorbar(im1, label='Amplitude')
    plt.title('Real(I) heatmap')
    plt.xlabel('distance point')
    plt.ylabel('frame/sweep')
    for i in range(rows):
        for j in range(cols):
            plt.text(j, i, f"{real_part[i, j]:.0f}", 
                    ha="center", va="center", color="white", fontsize=9)

    # 허수부 히트맵
    plt.subplot(122)
    im2 = plt.imshow(imag_part, cmap='plasma')
    plt.colorbar(im2, label='Amplitude')
    plt.title('Imaginary(Q) heatmap')
    plt.xlabel('distance point')
    plt.ylabel('frame/sweep')
    for i in range(rows):
        for j in range(cols):
            plt.text(j, i, f"{imag_part[i, j]:.0f}", 
                    ha="center", va="center", color="white", fontsize=9)

    plt.tight_layout()
    plt.savefig('iq_heatmap.png')
    plt.close()

   
    plt.figure(figsize=(15, 10))

    # 실수부 선 그래프
    plt.subplot(211)
    for i in range(rows):
        plt.plot(real_part[i, :], 'o-', label=f'frame/sweep {i+1}')
    plt.grid(True)
    plt.title('Real(I) value')
    plt.xlabel('distance point')
    plt.ylabel('Amplitude')
    plt.legend()

    # 허수부 선 그래프
    plt.subplot(212)
    for i in range(rows):
        plt.plot(imag_part[i, :], 'o-', label=f'frame/sweep {i+1}')
    plt.grid(True)
    plt.title('Imaginary(Q) value')
    plt.xlabel('distance point')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.tight_layout()
    plt.savefig('iq_lineplot.png')
    plt.close()

    # 3. I/Q 산점도 (실수부 vs 허수부)
    plt.figure(figsize=(12, 10))

    # 전체 데이터의 I/Q 산점도
    plt.subplot(221)
    plt.scatter(real_part.flatten(), imag_part.flatten(), alpha=0.7)
    plt.grid(True)
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.title(' I/Q scatterplot')
    plt.xlabel('Real part(I)')
    plt.ylabel('Imaginary part(Q)')

    # 각 행(프레임/스윕)별 I/Q 산점도
    colors = ['r', 'g', 'b', 'm', 'c', 'y']
    for i in range(min(rows, 3)):
        plt.subplot(2, 2, i+2)
        plt.scatter(real_part[i, :], imag_part[i, :], color=colors[i], alpha=0.7)
        plt.grid(True)
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        plt.title(f'frame/sweep {i+1} IQ scatterplot')
        plt.xlabel('Real part(I)')
        plt.ylabel('Imaginary part(Q)')
        
        
        for j in range(cols):
            plt.annotate(f"{j}", (real_part[i, j], imag_part[i, j]), 
                        fontsize=9, xytext=(5, 5), textcoords='offset points')

    plt.tight_layout()
    plt.savefig('iq_scatter.png')
    plt.close()

    # 4. 극좌표 표현 (진폭과 위상)
    magnitude = np.abs(result)
    phase = np.angle(result, deg=True) 

    plt.figure(figsize=(15, 10))

    # 진폭 그래프
    plt.subplot(211)
    for i in range(rows):
        plt.plot(magnitude[i, :], 'o-', label=f'frame/sweep {i+1}')
    plt.grid(True)
    plt.title('signal amplitude(abs)')
    plt.xlabel('distance point')
    plt.ylabel('Amplitude')
    plt.legend()

    # 위상 그래프
    plt.subplot(212)
    for i in range(rows):
        plt.plot(phase[i, :], 'o-', label=f'frame/sweep {i+1}')
    plt.grid(True)
    plt.title('signal phase')
    plt.xlabel('distance point')
    plt.ylabel('phase(degree)')
    plt.legend()

    plt.tight_layout()
    plt.savefig('magnitude_phase.png')
    plt.close()
    
    
    from mpl_toolkits.mplot3d import Axes3D

    # 실수부 3D 플롯
    fig = plt.figure(figsize=(15, 12))
    ax1 = fig.add_subplot(221, projection='3d')
    x, y = np.meshgrid(range(cols), range(rows))
    ax1.plot_surface(x, y, real_part, cmap='viridis', alpha=0.8)
    ax1.set_title('real(I) 3D ')
    ax1.set_xlabel('distance point')
    ax1.set_ylabel('frame/sweep')
    ax1.set_zlabel('Amplitude')

    # 허수부 3D 플롯
    ax2 = fig.add_subplot(222, projection='3d')
    ax2.plot_surface(x, y, imag_part, cmap='plasma', alpha=0.8)
    ax2.set_title('Imaginary (Q) 3D')
    ax2.set_xlabel('distance point')
    ax2.set_ylabel('frame/sweep')
    ax2.set_zlabel('Amplitude')

    # 진폭 3D 플롯
    ax3 = fig.add_subplot(223, projection='3d')
    ax3.plot_surface(x, y, magnitude, cmap='magma', alpha=0.8)
    ax3.set_title('Amplitude 3D')
    ax3.set_xlabel('distance point')
    ax3.set_ylabel('frame/sweep')
    ax3.set_zlabel('Amplitude')

    # 위상 3D 플롯
    ax4 = fig.add_subplot(224, projection='3d')
    ax4.plot_surface(x, y, phase, cmap='coolwarm', alpha=0.8)
    ax4.set_title('Phase 3D')
    ax4.set_xlabel('distance point')
    ax4.set_ylabel('frame/sweep')
    ax4.set_zlabel('phase(degree)')

    plt.tight_layout()
    plt.savefig('iq_3d.png')
    plt.close()

n = 1
results=[]
for i in range(n):

    result = client.get_next()
    results.append(result.frame)
    print(f"Result {i + 1}:")
    print(result)
    
client.close()

for result in results:
    custom_graph(result)