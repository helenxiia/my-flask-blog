#!/bin/bash

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

# Let's first spin containers down to prevent out of 
# memory issues on our VPS instances when building in the next step

docker compose -f docker-compose.prod.yml down

docker compose -f docker-compose.prod.yml up -d --build

echo "SERVER HAS RESTARTED"

