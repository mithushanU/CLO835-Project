FROM ubuntu:20.04

# Update and install dependencies
RUN apt-get update -y && \
    apt-get install -y python3-pip mysql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application files to /app directory
COPY . /app
WORKDIR /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the application port
EXPOSE 8080

# Define entry point and default command
ENTRYPOINT ["python3"]
CMD ["app.py"]
