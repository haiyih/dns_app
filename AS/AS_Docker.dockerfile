FROM python:3.9
WORKDIR /app
COPY authoritative_server.py .
CMD ["python", "authoritative_server.py"]
