# https://stackoverflow.com/questions/69182455/possible-to-add-kaniko-to-alpine-image-or-add-jq-to-kaniko-image
# It's also possible to use directly COPY --from=gcr.io/kaniko-project/executor
FROM gcr.io/kaniko-project/executor AS kaniko
FROM python:3.12-slim

# Install dependencies
RUN apt-get update \
    && apt-get install -y git curl

# Install Flask
RUN pip install Flask

# Copy Kaniko executor
# COPY --from=gcr.io/kaniko-project/executor:latest /kaniko /kaniko

# Set work directory
WORKDIR /app

# Copy application files
COPY . .
# COPY webhook.sh .
RUN chmod +x webhook.sh

# Expose port
EXPOSE 5000

#
# Add kaniko to this image by re-using binaries and steps from official image
#
COPY --from=kaniko /kaniko/executor /kaniko/executor
COPY --from=kaniko /kaniko/docker-credential-gcr /kaniko/docker-credential-gcr
COPY --from=kaniko /kaniko/docker-credential-ecr-login /kaniko/docker-credential-ecr-login
COPY --from=kaniko /kaniko/docker-credential-acr-env /kaniko/docker-credential-acr-env
COPY --from=kaniko /etc/nsswitch.conf /etc/nsswitch.conf
COPY --from=kaniko /kaniko/.docker /kaniko/.docker

ENV PATH=$PATH:/usr/local/bin:/kaniko
ENV DOCKER_CONFIG=/kaniko/.docker/
ENV DOCKER_CREDENTIAL_GCR_CONFIG=/kaniko/.config/gcloud/docker_credential_gcr_config.json


# Run the application
CMD ["python", "server.py"]