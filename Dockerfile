FROM python:3.10-alpine
WORKDIR /code
COPY requirements.txt ./
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip
COPY . .
CMD ["python", "main.py"]