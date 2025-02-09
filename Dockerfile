FROM python:3.9-slim-buster

WORKDIR /app

# Copy subfinder binary - corrected path and ensure executable
COPY subfinder /app/subfinder
RUN chmod +x /app/subfinder

# Copy your web application code
COPY . /app/

# No need to copy requirements.txt again, it's already in /app
# Install dependencies
RUN pip install -r requirements.txt

# Install necessary utilities: dnsutils, curl, ping
RUN apt-get update && apt-get install -y dnsutils curl iputils-ping --no-install-recommends

# Set environment variables (if needed)
ENV PORT 5000
ENV DEBUG_PRINT "true"

CMD ["python3", "app.py"]
