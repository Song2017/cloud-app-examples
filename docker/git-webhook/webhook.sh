#!/bin/bash

REPO_URL=$1
BRANCH=$2
WORK_DIR=/workspace

# Clone the repository
git clone --branch $BRANCH $REPO_URL $WORK_DIR/repo

echo $REPO_URL
ls $WORK_DIR/repo

# Navigate to the repository directory
cd $WORK_DIR/repo
echo "dockerfile $WORK_DIR/$DOCKER_DIR/$DOCKER_FILE, image $DOCKER_IMAGE, --username=$DOCKER_REGISTRY_NAME $DOCKER_REGISTRY"
# Build the image using Kaniko
# docker login --username=$DOCKER_REGISTRY_NAME -p $DOCKER_REGISTRY_PASS $DOCKER_REGISTRY
cat <<EOF > /kaniko/.docker/config.json
{
  "auths": {
    "$DOCKER_REGISTRY": {
      "auth": "$(echo -n '$DOCKER_REGISTRY_NAME:$DOCKER_REGISTRY_PASS' | base64)"
    }
  }
}
EOF

cat /kaniko/.docker/config.json
/kaniko/executor --dockerfile $WORK_DIR/$DOCKER_DIR/$DOCKER_FILE --context $WORK_DIR/$DOCKER_DIR --destination $DOCKER_IMAGE

# # Clean up
# rm -rf $WORK_DIR/repo