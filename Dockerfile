# Dockerfile

# Official python image
FROM python:3.11.3-alpine

RUN apk update

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint /entrypoint
RUN chmod +x /entrypoint

# Mounts the application code to the image
COPY . app
WORKDIR /app

EXPOSE 8000

# Run server
ENTRYPOINT ["/entrypoint"]