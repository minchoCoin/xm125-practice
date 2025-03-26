# xm125-practice
XM125 mmWave sensor practice

# Installation
1. Download files from Quick start contents at [https://github.com/acconeer/acconeer-python-exploration](https://github.com/acconeer/acconeer-python-exploration)
2. Click update.bat
3. install CH340 driver at [https://www.arduined.eu/ch340-windows-10-driver-download/](https://www.arduined.eu/ch340-windows-10-driver-download/)
![image](https://github.com/user-attachments/assets/846afd27-e544-4d5f-b1c6-1ca799ba8434)
4. run run_app.bat
5. click A121
   ![image](https://github.com/user-attachments/assets/afdc622e-a9b1-418c-ac40-82a25132dd49)

![image](https://github.com/user-attachments/assets/266e5e9f-b891-4fca-8fc0-47e7e3be0201)

6. click setting and set the baudrate to 115200
   
![image](https://github.com/user-attachments/assets/69caabe3-5fb7-45b3-a513-bab92bfb697d)

7. click the connect and click sparseIQ or distance etc... and start measurement!
    
![image](https://github.com/user-attachments/assets/9476614c-0541-4f44-adb4-e7dd81593155)

# get raw data of XM125 mmWave sensor
1. Download examples at [https://github.com/acconeer/acconeer-python-exploration/tree/master/examples](https://github.com/acconeer/acconeer-python-exploration/tree/master/examples)
2. run cmd_with_path.bat
3. run basic.py and basic_plot.py(serial_port='COMx',override_baudrate=115200)
```
Server Info:
ServerInfo:
  rss_version ............ a121-v1.9.0
  sensor_count ........... 1
  ticks_per_second ....... 1000
  hardware_name .......... xm125
  max_baudrate ........... 2000000
  sensor_infos:
    SensorInfo @ slot 1:
      connected .............. True
      serial ................. None
Result 1:
Result(data_saturated=False, frame_delayed=False, calibration_needed=False, temperature=0, _frame=array([[( -75, 214), ( -84, 311), ( -94, 335), (-171, 334), (-210, 316),
        (-342, 255)],
       [(  44, 297), ( -78, 296), (-130, 380), (-146, 294), (-259, 256),
        (-308, 267)],
       [( -15, 381), ( -46, 359), (-110, 409), (-248, 287), (-257, 277),
        (-356, 227)],
       [( -14, 322), (-173, 409), ( -95, 293), (-250, 239), (-230, 292),
        (-431, 182)]], dtype=[('real', '<i2'), ('imag', '<i2')]), tick=1567, _context=ResultContext(metadata=Metadata(_frame_data_length=24, _sweep_data_length=6, _subsweep_data_offset=array([0]), _subsweep_data_length=array([6]), _calibration_temperature=2, _tick_period=0, _base_step_length_m=0.00250227400101721, _max_sweep_rate=8902.890625, _high_speed_mode=True), ticks_per_second=1000))
Result 2:
Result(data_saturated=False, frame_delayed=False, calibration_needed=False, temperature=1, _frame=array([[( -64, 323), (-138, 312), ( -42, 315), (-188, 223), (-230, 294),
        (-308, 225)],
       [(  41, 311), ( -42, 291), (-102, 324), (-213, 253), (-264, 292),
        (-314, 235)],
       [( -31, 283), (-128, 340), ( -94, 389), (-235, 357), (-175, 289),
        (-340, 193)],
       [( -85, 328), ( -76, 292), ( -82, 252), (-246, 231), (-329, 246),
        (-391, 228)]], dtype=[('real', '<i2'), ('imag', '<i2')]), tick=1586, _context=ResultContext(metadata=Metadata(_frame_data_length=24, _sweep_data_length=6, _subsweep_data_offset=array([0]), _subsweep_data_length=array([6]), _calibration_temperature=2, _tick_period=0, _base_step_length_m=0.00250227400101721, _max_sweep_rate=8902.890625, _high_speed_mode=True), ticks_per_second=1000))
Result 3:
```
![image](https://github.com/minchoCoin/xm125-practice/blob/main/iq_scatter.png)
![image](https://github.com/minchoCoin/xm125-practice/blob/main/iq_3d.png)

# get range-velocity heatmap

slow version(with many subsweeps): sparse_iq_copy.py
faste version(only one sweep): faster_range_doppler.py

![image](https://github.com/minchoCoin/xm125-practice/blob/main/range_velocity_map/results3.png)


# youtube video
- installation:
  [https://youtu.be/b6R--BpjOM4](https://youtu.be/b6R--BpjOM4)

- run basic.py and basic_plot.py to get graph from raw data:
  [https://youtu.be/ERDY-VRpA3k](https://youtu.be/ERDY-VRpA3k)

- run basic_plot.py to get 3d graph from raw data:
  [https://youtu.be/0qt5du7j4OU](https://youtu.be/0qt5du7j4OU)
  
- get range-doppler heatmap using sparse_iq_copy.py
  [https://youtu.be/xbgBpl3dfMc](https://youtu.be/xbgBpl3dfMc)

- distance measurement using examples/algo/a121/distance/processor.py
  [https://youtu.be/vF7i7laj-D8](https://youtu.be/vF7i7laj-D8)

- speed measurement using examples/algo/a121/speed/processor.py
  [https://youtu.be/zhe-X66ccDs](https://youtu.be/zhe-X66ccDs)
# references
- [acconeer-python-exploration/README.md](https://github.com/acconeer/acconeer-python-exploration/blob/master/README.md)
- [XM125_connect_troubleshooting](https://docs.sparkfun.com/SparkFun_Qwiic_Pulsed_Radar_Sensor_XM125/troubleshooting/#issue-1-connecting-to-the-acconeer-exploration-tool)
