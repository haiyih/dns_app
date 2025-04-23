FROM python:3.9
WORKDIR /app
COPY user_server.py .
RUN pip install flask requests
CMD ["python", "user_server.py"]
