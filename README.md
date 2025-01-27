# Project requirements
![](https://img.shields.io/badge/python-3.12-green)
![](https://img.shields.io/badge/Redis-7.4-red)
![](https://img.shields.io/badge/PostgreSQL-v17-blue)

## To run in docker
1. Check .env file for having properly set env variables (especially
redis and postgres ports). So you need to change docker-compose ports also
2. Jump to project root and run ```docker compose up``` 
3. Go for http://0.0.0.0:8081/docs to check if swagger is visible
4. You're awesome!

# To run locally
1. Check if postgres and redis installed on your PC
2. Check if host in .env equals 'localhost'
3. Run a few commands in psql terminal e.g:
``` 
create database <env database name>;
create user <env user>;
grant all priviliges on database <env database name> to <env user>
grant all priviliges on schema public to <env user>
```

4. Run command in your IDE terminal or jump into project dir and start
```
uvicorn code.main:app 
``` 
So yo can add some flags e.g --port for launch in specific port

5. (optional)
To start coverage/pytest
```
coverage run -m pytest -v
```
6. To look at coverage results you can use following command
```
coverage report -m
```