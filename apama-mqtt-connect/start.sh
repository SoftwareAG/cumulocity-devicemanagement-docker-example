#!/bin/bash
echo "Start start.sh ..."
correlator --config Project_deployed/config --logQueueSizePeriod 0 --logfile /dev/stdout &
echo "Correlator done"
sleep 5
echo "Sleep done"
engine_inject -c Project_deployed/apama-mqtt-connect.cdp
echo "Inject cdp file done"
for f in Project_deployed/monitors/*; do xargs engine_inject $f ; done
for f in Project_deployed/events/*; do xargs engine_send $f ; done
sleep infinity
