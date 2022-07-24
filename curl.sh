#!/bin/bash

curl -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' \
--data '{"email": "edw125@example.com", "username": "edw125", "first_name": "edw", "last_name": "edw", "password": "edw1234567890"}' \
http://127.0.0.1:8000/auth/users/

curl -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' \
--data '{"email": "edw125@example.com", "password": "edw1234567890"}' \
http://127.0.0.1:8000/auth/jwt/create/ | jq -r '.access'

curl -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}" \
--data '{"name": "edw125", "message": "test"}' \
http://127.0.0.1:8000/users/logs/

curl -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}" \
--data '{name: "edw125", message: "history 3"}' \
http://127.0.0.1:8000/users/logs/

curl -X DELETE -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" http://127.0.0.1:8000/users/logs/1/

curl -X POST -H 'Accept: application/json' -H 'Content-Type: application/json' -H "Authorization: Bearer ${TOKEN}" \
--data '{name: "edw125", message: "history 3"}' \
http://127.0.0.1:8000/users/logs/