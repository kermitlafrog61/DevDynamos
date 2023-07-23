#!/bin/sh

cd src/

until uvicorn main:app --reload --host 0.0.0.0;
do
    echo "Waiting for database connection..."
    sleep 2
done
