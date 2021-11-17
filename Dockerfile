# Language: dockerfile
# Path: Dockerfile
FROM python:3
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "main.py"]
