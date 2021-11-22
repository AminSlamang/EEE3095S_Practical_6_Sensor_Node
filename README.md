# EEE3095S_Practical_6_Sensor_Node (Pi 1)

## Authors:
### KTNRIO001 - Rio Katundulu
### SLMAMI010 - Amin Slamang

Reads the light level and temperature from a adc and accompanied analogue sensors and sends the sampled data to a server via tcp sockets. The sampling of this device is controlled by the server (Pi 2). Commands from the server are also received via tcp sockets and carried out by this device.

These commands are:
-Turning on sampling
-Turning off sampling
-Telling the server the status of the device and when it last sampled
