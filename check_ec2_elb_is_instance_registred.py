#! /usr/bin/python

from pynag.Plugins import WARNING, CRITICAL, OK, UNKNOWN, simple as Plugin
import boto


## Create the plugin option
np = Plugin()

## Add a command line argument
np.add_arg("n","name", "Amazon ELB name", required=True)
np.add_arg("i","instance", "Amazon EC2 instance ID", required=True)

## This starts the actual plugin activation
np.activate()

## Use specified ELB name
elb_name = np['name']
instance_id = np['instance']

## Unable to connect
try:
  conn = boto.connect_elb()
except boto.exception.NoAuthHandlerFound:
  np.nagios_exit(UNKNOWN, "Unable to log into AWS. Please Check your /etc/boto.cfg file or AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variable.")

## Unable to get elbs
try:
  instances_health = conn.describe_instance_health(elb_name)
except:
  np.nagios_exit(UNKNOWN, "Unable to get elb list. Is network up ? Is region configured ? (Region %s)" % ( conn.DefaultRegionName))

## Get desired instance
instance_health = [instance for instance in instances_health if instance.instance_id == instance_id]

## If instance is not registered
if len(instance_health) == 0:
  np.nagios_exit(WARNING, "Instance %s is not registered into %s" % ( instance_id, elb_name))

## Return value
map_instance_status = {}
map_instance_status["InService"] = ('Instance is correctly register into ELB', OK)
map_instance_status["OutOfService"] = ('Instance is out of ELB', CRITICAL)

try:
  nagios_message = map_instance_status[instance_health[0].state][0]
  nagios_status = map_instance_status[instance_health[0].state][1]
except KeyError:
  np.nagios_exit(UNKNOWN, "Unknown return status")

np.nagios_exit(nagios_status, nagios_message)

