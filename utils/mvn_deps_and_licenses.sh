#!/bin/bash

cd $1

mvn project-info-reports:dependencies

cp target/site/dependencies.html $2.html