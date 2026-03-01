FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, cron, and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Playwright browsers and system dependencies
RUN playwright install --with-deps chromium

# Copy the application code
COPY *.py .

# Copy .env file if it exists (optional)
COPY .env* ./

# Copy cron configuration
COPY crontab /etc/cron.d/timetable-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/timetable-cron

# Create the log file to be able to run tail
RUN touch /app/cron.log

# Apply cron job
RUN crontab /etc/cron.d/timetable-cron

# Run the script immediately on container start, then start cron in foreground
CMD python3 main.py && cron -f
