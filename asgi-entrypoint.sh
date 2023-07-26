#!/bin/sh


until alembic upgrade head
do
    echo "Waiting for migrations..."
    sleep 2
done

cd src/

until uvicorn main:app --reload --host 0.0.0.0;
do
    echo "Waiting for database connection..."
    sleep 2
done
