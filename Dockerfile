FROM python:3.13.1-alpine
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY . /app
CMD ["python3", "./main.py", "--port", "8080"]