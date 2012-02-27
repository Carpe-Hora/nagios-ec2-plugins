#! /usr/bin/python

from pynag.Plugins import WARNING, CRITICAL, OK, UNKNOWN, simple as Plugin
import boto
import boto.ec2


## Create the plugin option
np = Plugin()

## Add a command line argument
np.add_arg("i","instance-id", "Amazon EC2 Instance ID", required=True)

## This starts the actual plugin activation
np.activate()

## Use specified Instance ID
ec2_instance_id = np['i']

## Unable to connect
try:
  conn = boto.connect_ec2()
except boto.exception.NoAuthHandlerFound:
  np.nagios_exit(UNKNOWN, "Unable to log into AWS. Please Check your /etc/boto.cfg file or AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variable.")

## Unable to get instance status
try:
  instance = conn.get_all_instance_status(ec2_instance_id)[0]
except:
  np.nagios_exit(UNKNOWN, "Unable to get instance %s. Is network up ? Is region configured ? (Region %s)" % ( ec2_instance_id, conn.DefaultRegionName))

## Confioguration return messge + code
map_instance_status = {}
map_instance_status[0] = ('instance is pending (maybe starting)', UNKNOWN)
map_instance_status[16] = ('instance is running', OK)
map_instance_status[32] = ('instance is shutting down', WARNING)
map_instance_status[48] = ('instance is terminated', CRITICAL)
map_instance_status[64] = ('instance is stopping', WARNING)
map_instance_status[80] = ('instance is stopped', CRITICAL)
map_instance_status[272] = ('instance is in an unknown state ...', UNKNOWN)

## Default value
try:
  nagios_message = map_instance_status[instance.state_code][0]
  nagios_status = map_instance_status[instance.state_code][1]
except KeyError:
  np.nagios_exit(UNKNOWN, "Unknown return code")

np.nagios_exit(nagios_status, nagios_message)


