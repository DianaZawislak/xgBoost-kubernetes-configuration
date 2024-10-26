# Kubernetes Command Reference for XGBoost Cluster

## Cluster Connection and Context
```bash
# Get current context
kubectl config current-context

# Set namespace for current context
kubectl config set-context --current --namespace=xgboost-service

# Get all namespaces
kubectl get namespaces

# Create namespace
kubectl create namespace xgboost-service
```

## Deployment Commands
```bash
# Deploy resources
kubectl apply -f mongodb-service.yaml
kubectl apply -f mongo-secret.yaml
kubectl apply -f xgboost-model-pvc.yaml
kubectl apply -f xgboost-training-job.yaml
kubectl apply -f xgboost-api-deployment.yaml

# Apply all YAML files in current directory
kubectl apply -f .
```

## Cleanup and Deletion
```bash
# Delete specific resources
kubectl delete deployment xgboost-api-deployment -n xgboost-service
kubectl delete job xgboost-training-job -n xgboost-service
kubectl delete service mongodb -n xgboost-service
kubectl delete pvc xgboost-model-pvc -n xgboost-service
kubectl delete secret mongodb-credentials -n xgboost-service

# Delete multiple resources
kubectl delete pods --all -n xgboost-service
kubectl delete services --all -n xgboost-service

# Force delete a stuck pod
kubectl delete pod <pod-name> -n xgboost-service --force --grace-period=0
```

## Status and Debugging
```bash
# Get resource status
kubectl get all -n xgboost-service
kubectl get pods -n xgboost-service
kubectl get services -n xgboost-service
kubectl get deployments -n xgboost-service
kubectl get pvc -n xgboost-service
kubectl get secrets -n xgboost-service

# Detailed resource information
kubectl describe pod <pod-name> -n xgboost-service
kubectl describe service mongodb -n xgboost-service
kubectl describe pvc xgboost-model-pvc -n xgboost-service

# View logs
kubectl logs <pod-name> -n xgboost-service
kubectl logs -f <pod-name> -n xgboost-service  # Follow logs
kubectl logs --previous <pod-name> -n xgboost-service  # Previous container logs

# Get events
kubectl get events -n xgboost-service --sort-by='.metadata.creationTimestamp'
```

## Testing and Debugging
```bash
# Test MongoDB connection
kubectl run mongodb-test -n xgboost-service --rm -it --image=mongo -- mongosh "mongodb://10.108.0.15:27017"

# Execute commands in a pod
kubectl exec -it <pod-name> -n xgboost-service -- /bin/bash
kubectl exec -it <pod-name> -n xgboost-service -- python

# Port forwarding for local testing
kubectl port-forward service/xgboost-api-service 8080:80 -n xgboost-service
```

## Monitoring
```bash
# Watch pod status
kubectl get pods -n xgboost-service -w

# Monitor resource usage
kubectl top pods -n xgboost-service
kubectl top nodes

# Get pod details with IP and node information
kubectl get pods -o wide -n xgboost-service
```

## Configuration and Secrets
```bash
# View config maps and secrets
kubectl get configmaps -n xgboost-service
kubectl get secrets -n xgboost-service

# Decode secret
kubectl get secret mongodb-credentials -n xgboost-service -o jsonpath='{.data}'
```

## Storage
```bash
# Check storage
kubectl get pv  # Persistent Volumes
kubectl get pvc -n xgboost-service  # Persistent Volume Claims

# Check storage class
kubectl get storageclass
```

## Health Checks
```bash
# Check node status
kubectl get nodes
kubectl describe node <node-name>

# Check cluster info
kubectl cluster-info
kubectl get componentstatuses
```

## Common Aliases
```bash
alias k='kubectl'
alias kns='kubectl config set-context --current --namespace'
alias kgp='kubectl get pods -n xgboost-service'
alias kgs='kubectl get services -n xgboost-service'
alias kgd='kubectl get deployments -n xgboost-service'
alias kl='kubectl logs -n xgboost-service'
```

## Advanced Troubleshooting
```bash
# Check RBAC permissions
kubectl auth can-i --list -n xgboost-service

# Network debugging
kubectl run nettest --rm -it --image=nicolaka/netshoot -- /bin/bash

# Resource usage and limits
kubectl describe resourcequota -n xgboost-service
kubectl describe limits -n xgboost-service
```