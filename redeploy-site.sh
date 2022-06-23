#!/bin/bash

#CHECK CURRENT PROCESSES AND KILLS IF EXISTS
PROCESSES=$(pidof tmux)
if [[ "$PROCESSES" -ne "" ]]; then
    kill "$PROCESSES"
fi

#GETS THE PROJECT DIRECTORY
PROJECT_DIR="/root/flask-blog"
cd $PROJECT_DIR || exit

#CHECKS IF THE PROJECT IS GIT INTIALIZED
inside_git_repo="$(git rev-parse --is-inside-work-tree 2>/dev/null)"

if [ "$inside_git_repo" ]; then
    git fetch && git reset origin/main --hard
else
    echo "Current dir does not use git"
    exit
fi

# RUN FLASK APP
python -m venv python3-virtualenv
source python3-virtualenv/bin/activate

pip install -r requirements.txt

TMUX_SESSION="setup"
COMMAND="flask run --host=0.0.0.0"

tmux new-session -d -s "$TMUX_SESSION" "$COMMAND"

echo "name of tmux session is $TMUX_SESSION"

