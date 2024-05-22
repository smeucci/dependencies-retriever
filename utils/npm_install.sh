#!/bin/bash

cd $1

if [ -e package.json ]
then
    npm install