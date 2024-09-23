#!/bin/bash

REPO_URL=$1
BRANCH=$2
WORK_DIR=/workspace

# Clone the repository
git clone --branch $BRANCH $REPO_URL $WORK_DIR/repo

# Navigate to the repository directory
cd $WORK_DIR/repo

# Build the image using Kaniko
/kaniko/executor --dockerfile $WORK_DIR/repo/Dockerfile --context $WORK_DIR/repo --destination your-docker-registry/your-image:latest

# Clean up
rm -rf $WORK_DIR/repo