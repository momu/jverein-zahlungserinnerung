#!/bin/bash

for yaml in data/*.yaml; 
do 
    pandoc --template=zahlungserinnerung.latex \
    --pdf-engine=xelatex ${yaml} verein.yaml \
    -o data/$(basename ${yaml} .yaml).pdf; 
done 