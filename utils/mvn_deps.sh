#!/bin/bash

cd $1

mvn dependency:list -DexcludeTransitive=true -DoutputFile=$2.txt