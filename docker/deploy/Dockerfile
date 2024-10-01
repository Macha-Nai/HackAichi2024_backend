FROM python:3.10.10

RUN apt-get update && apt-get install -y \
    default-mysql-client \
    tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY app /usr/src/app
COPY db /usr/src/db 
COPY scripts /usr/src/scripts
COPY docker/deploy/requirements.txt .

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/usr/src/app

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]

