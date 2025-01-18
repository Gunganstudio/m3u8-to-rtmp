# Use Ubuntu as the base image
FROM ubuntu:20.04

# Set environment variable to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install FFmpeg, Python, and Supervisor
RUN apt-get update && apt-get install -y \
    ffmpeg \
    python3 \
    python3-pip \
    curl \
    supervisor && \
    apt-get clean

# Install Flask for the API
RUN pip3 install flask

# Create working directories
WORKDIR /app
RUN mkdir -p /app/logs /app/scripts

# Copy project files
COPY restream.sh /app/scripts/
COPY supervisord.conf /app/
COPY api.py /app/

# Make the script executable
RUN chmod +x /app/scripts/restream.sh

# Expose logs as a volume for debugging
VOLUME ["/app/logs"]

# Run Supervisor to manage processes
CMD ["supervisord", "-c", "/app/supervisord.conf"]
