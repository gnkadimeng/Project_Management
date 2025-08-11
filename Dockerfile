FROM python:3.12-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apk add --no-cache \
    postgresql-client \
    postgresql-dev \
    gcc \
    musl-dev \
    linux-headers \
    netcat-openbsd

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
RUN mkdir -p /app/staticfiles
EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]
