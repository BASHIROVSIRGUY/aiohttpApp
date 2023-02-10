FROM python:3.10-alpine
WORKDIR /code
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["python", "main.py"]