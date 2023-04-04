# cmds

## read sensor values

### IMU

- IMU-Group: 0x20
<!-- - Temp: 0xA1
- accelerometer: 0xA2
- magnetometer: 0xA3
- gyroscope: 0xA4
- euler: 0xA5
- linear_accel: 0xA6
- gravity: 0xA7
- quaternion: 0xA8 -->

## Ultraschall

- US-Group: 0x21
<!-- - US-Sensor 1:
- US-Sensor 2:
- US-Sensor 3:
- US-Sensor 4:
- US-Sensor 5:
- US-Sensor 6: -->

### Encoder

- Encoder-Group: 0x22
<!-- - Encoder 1:
- Encoder 2:
- Encoder 3:
- Encoder 4: -->

### LUX

- Helligkeit: 0x23

### temp

- Temp: 0x24

### Bat voltage

- Bat voltage: 0x25

### User Button:

- user button: 0x26

### LED

- run animation: 0x27

### Motor

- drive: 0x28

### POZYX

- Power ON/OFF: 0x29
- pozyx group: 0x2A
- read pozyx config: 0x2B

# data

## sensor data

### IMU

- vec4: 0x01
  - accelerometer
  - magnetometer
  - gyroscope
  - euler
  - linear_accel
  - gravity
  - quaternion

### Ultraschall

- US-Sensot group: 0x02

### Encoder

- Encoder Group: 0x03

### LUX

- Helligkeit: 0x04

### temp

- Temp: 0x05

### Bat voltage

- Bat voltage: 0x06

### User Button:

- user button: 0x07

### POZYX

- pos / orientation: 0x08
- config: 0x09

### Status

- cmd status: 0x00
