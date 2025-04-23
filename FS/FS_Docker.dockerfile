FROM python:3.9
WORKDIR /app
COPY fibonacci_server.py .
RUN pip install flask
CMD ["python", "fibonacci_server.py"]
