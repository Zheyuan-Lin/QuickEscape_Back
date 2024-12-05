#!/bin/bash

# Settings
WORKERS=20

# Clean up
rm -f /root/QuickEscape/data/flight/*.log

# Run the jobs
export PYTHONPATH=$PYTHONPATH:/root/QuickEscape

for (( i=1; i<=WORKERS; i++ )); do
    python3 -u /root/QuickEscape/data/flight/job.py "$i" $WORKERS > /root/QuickEscape/data/flight/"$i".log &
done

# Once completed
wait
echo "Jobs completed" > /root/QuickEscape/data/flight/complete.log