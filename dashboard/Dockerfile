FROM python:3.8
COPY requirements.txt /dashboard/requirements.txt
WORKDIR /dashboard
RUN pip install -r requirements.txt
COPY . /dashboard
ENTRYPOINT ["python"]
CMD ["run.py"]