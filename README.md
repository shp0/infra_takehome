## Takehome

### Setup
- Install NGINX ingress controller:
  - Run **kind-ingress-registry.sh** to create a kind cluster with ingress and local registry. https://kind.sigs.k8s.io/docs/user/ingress/#ingress-nginx
  - Create controller:
    - kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
  - Wait for controller:
    - kubectl wait --namespace ingress-nginx --for=condition=ready pod --selector=app.kubernetes.io/component=controller --timeout=90s
- Build Docker image and deploy:
  - docker build . -t localhost:5001/birds:1.17.0
  - docker push localhost:5001/birds:1.17.0 
  - kind load docker-image localhost:5001/birds:1.17.0
  - helm install birds helm/birds

- Add mapping to hosts file:
  - 127.0.0.1 birds.local
- Go to http://birds.local