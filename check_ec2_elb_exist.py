#! /usr/bin/python

from pynag.Plugins import WARNING, CRITICAL, OK, UNKNOWN, simple as Plugin
import boto

## Create the plugin option
np = Plugin()

## Add a command line argument
np.add_arg("n","name", "Amazon ELB name", required=True)

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
  elbs = conn.get_all_load_balancers(elb_name)
except:
  np.nagios_exit(UNKNOWN, "Unable to get elb list. Is network up ? Is region configured ? (Region %s)" % ( conn.DefaultRegionName))

# Return value
if not elbs:
  np.nagios_exit(CRITICAL, "No ELB named %s" % elb_name)
else:
  np.nagios_exit(OK, "ELB exist")




