# Prototype-System-with-an-API-that-provides-a-Distributed-Service-Interface

## Run Docker Environment

```Terminal
cd .\dashboard\
```

```Terminal
docker-compose -f "dashboard\docker-compose.deploy.yml" up -d --build
```

### Initialise Database

Open the command line interface for the user-service container and enter the following:

```CLI
flask db init
```

```CLI
flask db migrate
```

```CLI
flask db upgrade
```

## References

cloudacademy (2020) Mastering Microservices with Python, Flask, and Docker. Available at: [https://github.com/cloudacademy/python-flask-microservices](https://github.com/cloudacademy/python-flask-microservices) (Accessed: 19 July 2021).