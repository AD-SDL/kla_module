#!/bin/bash

session="WEI"

folder="~/repos/AD-SDL/tecan_module/test"

tmux new-session -d -s $session
tmux set -g mouse on

window=0
tmux rename-window -t $session:$window 'redis'
tmux send-keys -t $session:$window 'cd ' $folder C-m
# Start the redis server, or ping if it's already up
if [ "$(redis-cli ping)" != "PONG" ]; then
	tmux send-keys -t $session:$window 'redis-server' C-m
fi

window=1
tmux new-window -t $session:$window -n 'server'
tmux send-keys -t $session:$window 'cd ' $folder C-m
tmux send-keys -t $session:$window 'python3 -m wei.server --workcell ./test_kla_workcell.yaml' C-m

window=2
tmux new-window -t $session:$window -n 'engine'
tmux send-keys -t $session:$window 'cd ' $folder C-m
# Uncomment the following for ROS support
# tmux send-keys -t $session:$window 'source ~/wei_ws/install/setup.bash' C-m
tmux send-keys -t $session:$window 'python3 -m wei.engine --workcell ./test_kla_workcell.yaml' C-m

window=3
tmux new-window -t $session:$window -n 'kla'
tmux send-keys -t $session:$window 'cd ' $folder C-m
tmux send-keys -t $session:$window 'python3 ../scripts/kla_rest_node.py' C-m

tmux attach-session -t $session
