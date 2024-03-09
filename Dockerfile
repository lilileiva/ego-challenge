# Dockerfile

# Official python image
FROM python:3.11.3-alpine

RUN apk update

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script and set execute permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN apk add dos2unix && dos2unix /entrypoint.sh

# Mount the application code to the image
COPY . app
WORKDIR /app

EXPOSE 8000

# Run server
ENTRYPOINT ["/entrypoint.sh"]