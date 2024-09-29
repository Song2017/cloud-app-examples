## readme
`Build image in serverless service, like Ali Cloud Function compute`
- setup api for github webhook
- api1 for webhook, api2 for image build
- pull code from git repo
- kaniko build and push image in Docker
### OS envs
```json
{
    "DOCKER_DIR": "server",
    "DOCKER_FILE": "deploy/Dockerfile",
    "DOCKER_IMAGE": "registry.cn-shanghai.aliyuncs.com/public_00/yaso:fc",
    "DOCKER_REGISTRY": "registry.cn-shanghai.aliyuncs.com",
    "DOCKER_REGISTRY_NAME": "son**",
    "DOCKER_REGISTRY_PASS": "**",
    "REPO_URL": "https://**@github.com/goyaso/project-ben.git",
    "WEBHOOK_ASYNC": "https://yaso-webhook-release-***.cn-shanghai.fcapp.run/webhook-sleep"
}
```
