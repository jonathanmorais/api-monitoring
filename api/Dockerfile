FROM python:3.6-alpine

# EXPOSE 5000

WORKDIR /app

RUN mkdir /csv

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "-u", "./request.py" ]s