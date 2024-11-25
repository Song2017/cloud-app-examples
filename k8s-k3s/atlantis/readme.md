deployment: https://www.runatlantis.io/docs/deployment

1. secrert
kubectl create secret generic atlantis-vcs --from-literal=token=aa --from-literal=ado-webhook-user=atlantis_test_ben --from-literal=ado-webhook-password=a
kubectl get secrets
kubectl describe secret my-secret
kubectl edit secret <secret-name>

kubectl get secrets -o yaml > all-secrets.yaml
 <!-- --from-file=webhook-secret -->
2. atlantis
kubectl apply -f atlantis.yaml