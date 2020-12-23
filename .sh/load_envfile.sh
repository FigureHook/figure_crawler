#!/bin/bash
if [ -f .env ]
  export $(cat .env | sed 's/#.*//g' | xargs)
fi