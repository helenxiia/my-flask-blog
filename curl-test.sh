#!/bin/bash

curl --request POST http://localhost:5000/api/timeline_post -d 'name=scripty&email=localhost@localhost.com&content=testing from my curl test script!'

curl http://localhost:5000/api/timeline_post
