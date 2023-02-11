FROM pytorch/pytorch:latest
WORKDIR /code
COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip
COPY . .
CMD ["python", "main.py"]