# Dockerfile
FROM python:3.8
COPY requirements.txt /auth/requirements.txt
WORKDIR /auth
RUN pip install -r requirements.txt
COPY . /auth
ENTRYPOINT ["python"]
CMD ["run.py"]