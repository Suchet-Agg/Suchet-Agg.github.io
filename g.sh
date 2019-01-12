#!/bin/sh
user="Suchet-Agg"
repo='abcd'

git init
git add .
git commit -m "Starting Out"

git remote rm origin
git remote add origin git@github.com:$user/$repo.git

git push origin master -f


