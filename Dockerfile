FROM python:3.7

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY ./userservice /work/userservice
COPY ./tests /work/tests

WORKDIR /work

ENTRYPOINT ["python", "-m", "userservice"]
