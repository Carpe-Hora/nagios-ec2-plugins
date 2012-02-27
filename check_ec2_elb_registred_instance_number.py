#! /usr/bin/python

from pynag.Plugins import WARNING, CRITICAL, OK, UNKNOWN, simple as Plugin
import boto


## Create the plugin option
np = Plugin()

## Add a command line argument
np.add_arg("n","name", "Amazon ELB name", required=True)
np.add_arg("N","numbers", "Numbers of desired instance running in the pool. Default will be half total number of node", required=False)

## This starts the actual plugin activation
np.activate()

## Use specified ELB name
elb_name = np['name']

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

number_of_instance=len(instances_health)
number_of_running_instance=0
for instance_health in instances_health:
  if instance_health.state == 'InService':
    number_of_running_instance += 1

if np["numbers"] == None:
  desired_number = number_of_instance/2
else:
  desired_number = int(np["numbers"])

# Performance Data
warn_perfdata = desired_number*1.25
if warn_perfdata > desired_number:
  warn_perfdata = desired_number

np.add_perfdata("running", number_of_running_instance, None, warn_perfdata, desired_number, 0, number_of_instance)
np.add_perfdata("all", number_of_instance)

# Return value
if desired_number > number_of_running_instance:
  np.nagios_exit(CRITICAL, "Only %d instance running, %d desired" % ( number_of_running_instance, desired_number ))
else:
  np.nagios_exit(OK, "%d instance run, %d desired" % ( number_of_running_instance, desired_number ))




