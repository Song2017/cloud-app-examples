#!/bin/bash

BRANCH=$1
WORK_DIR=/app

echo "start shell"
# Clone the repository
#git clone https://username:token@github.com/username/repo.git

REPO_DIR=$WORK_DIR/repo
git clone --branch $BRANCH $REPO_URL $REPO_DIR

echo $REPO_URL
ls $REPO_DIR

# Navigate to the repository directory
cd $REPO_DIR
echo "dockerfile $REPO_DIR/$DOCKER_DIR/$DOCKER_FILE, image $DOCKER_IMAGE, --username=$DOCKER_REGISTRY_NAME $DOCKER_REGISTRY"
# Build the image using Kaniko
# docker login --username=$DOCKER_REGISTRY_NAME -p $DOCKER_REGISTRY_PASS $DOCKER_REGISTRY
auth=$(echo -n "$DOCKER_REGISTRY_NAME:$DOCKER_REGISTRY_PASS" | base64)
cat <<EOF > /kaniko/.docker/config.json
{
  "auths": {
    "$DOCKER_REGISTRY": {
      "auth": "$auth"
    }
  }
}
EOF

cat /kaniko/.docker/config.json
/kaniko/executor --dockerfile $REPO_DIR/$DOCKER_DIR/$DOCKER_FILE --context $REPO_DIR/$DOCKER_DIR --destination $DOCKER_IMAGE

# # Clean up
 rm -rf $REPO_DIR