#!/bin/bash

# Clean up
rm -f /root/QuickEscape/data/accommodation/*.log

# Run the jobs
export PYTHONPATH=$PYTHONPATH:/root/QuickEscape

python3 -u /root/QuickEscape/data/accommodation/job.py > /root/QuickEscape/data/accommodation/job.log

# Once completed
wait
echo "Jobs completed" > /root/QuickEscape/data/accommodation/complete.log