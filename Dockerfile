FROM python:3.7.8-alpine3.12

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk add -U --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev

RUN pip install --no-cache-dir -r requirements.txt

ARG MONGO_URI
ENV MONGO_URI $MONGO_URI
ARG CRYPTO_KEY
ENV CRYPTO_KEY $CRYPTO_KEY
ARG JWT_KEY
ENV JWT_KEY $JWT_KEY

COPY . .

CMD [ "python", "./runner.py" ]