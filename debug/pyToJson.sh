#!/bin/bash

echo "${1}" | sed "s/'/\"/g" | sed "s/True/true/g" | sed "s/False/false/g" | jq
