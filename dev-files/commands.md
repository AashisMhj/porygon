## Commands

```bash
docker compose up -d
docker compose down 
docker compose down -v
```

```bash
docker run --name porygon -e SERVER_URL=http://host.docker.internal:5000 -e LOKI_URL=http://host.docker.internal:3100 porygon:latest
```

```bash
eval $(minikube docker-env)
kubectl get pods --selector=job-name=step1-job
kubectl exec -it <pod-name> -- /bin/bash # bash into a pod
kubectl exec -it <pod-name> -c <container-name> -- /bin/bash # bash into multi container pod
eval $(minikube docker-env -u) # undo minikube docker-env
```

## push container to docker hub
```bash
docker build -t aashismhj/porygon:latest .
# OR
docker tag porygon:latest aashismhj/porygon:latest
# after building push to dockerhub
docker push aashismhj/porygon:latest
```
