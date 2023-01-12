## Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import json
import datetime
import RPi.GPIO as GPIO
import time


# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = ""
CLIENT_ID = ""
PATH_TO_CERTIFICATE = ""
PATH_TO_PRIVATE_KEY = ""
PATH_TO_AMAZON_ROOT_CA_1 = ""
#MESSAGE = "Hello World"
TOPIC = ""
RANGE = 20

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')

Trigger = 16
Echo = 18

def checkdist():
    GPIO.output(Trigger, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(Trigger, GPIO.LOW)
    while not GPIO.input(Echo):
        pass
    t1 = time.time()
    while GPIO.input(Echo):
        pass
    t2 = time.time()
    return (t2-t1)*340/2

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Trigger,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(Echo,GPIO.IN)

try:
    while True:
        nowtime = datetime.datetime.now()
        timestamp = nowtime.strftime('%Y/%m/%d %H:%M:%S')
        get_date = nowtime.strftime('%Y/%m/%d')
        get_time = nowtime.strftime('%H:%M:%S')
        d = checkdist()
        df = "%0.2f" %d
        data = {
            'deviceid' : CLIENT_ID,
            'timestamp' : timestamp,
            'date' : get_date,
            'time' : get_time,
            'distance' : df
        }
        # client.publish(TOPIC, json.dumps(data), 1)
        mqtt_connection.publish(topic=TOPIC, payload=json.dumps(data), qos=mqtt.QoS.AT_LEAST_ONCE)
        print ('Distance: %s m' %df)
        time.sleep(3)

except KeyboardInterrupt:
    GPIO.cleanup()
    print ('GPIO cleeanup and end!')

disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()