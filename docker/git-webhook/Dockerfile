FROM python:3.12-slim

# Install dependencies
RUN apt-get update && apt-get install -y git curl

# Install Flask
RUN pip install Flask

# Copy Kaniko executor
COPY --from=gcr.io/kaniko-project/executor:latest /kaniko /kaniko

# Set work directory
WORKDIR /app

# Copy application files
COPY server.py .
COPY webhook.sh .
RUN chmod +x webhook.sh

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "server.py"]