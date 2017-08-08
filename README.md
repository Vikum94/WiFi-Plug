# WiFi-Plug

## Given python script is an easy method for you to control your Tp-link Wi-Fi plug using MQTT commands

## How to Configure
1. Change the Network address given as `cidr2='192.168.1.0/24'`
2. Change the host IP address according to your MQTT broker.
3. Change the MQTT topic as you wish at `topic='g1'`
4. Plug in new Wi-Fi plug and connect it to your Wi-Fi network.
 
## Adding Wi-Fi plugs
1. Run the script 'wifi_plug.py'
2. Plug in a new Tp-Link Wi-Fi plug and connect it to your network
3. Publish a MQTT message to the topic as 'wifiplug_add_(Device-ID)' 
> Device-ID start from 1
4. Continue step 2 and 3 to add new plugs and change the id as you go on

## Controlling Plug
1. After succcessfully adding plugs send MQTT messages as 'wifiplug_(Device-ID)_(on/off)'

## Used libraries

Credits go to [GadgetReactor](https://github.com/GadgetReactor/pyHS100)
