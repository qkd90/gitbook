### 删除pod

1、先删除pod

2、再删除对应的deployment

否则只是删除pod是不管用的，还会看到pod，因为deployment.yaml文件中定义了副本数量



```
查看pod：
kubectl get pod -n jenkins

删除对应名称pod：
kubectl delete pod jenkins2-8698b5449c-grbdm -n jenkins

查看deployment
kubectl get deployment -n jenkins

kubectl delete deployment jenkins2 -n jenkins


```



```
To access Minio from localhost, run the below commands:

  1. export POD_NAME=$(kubectl get pods --namespace minio -l "release=minio" -o jsonpath="{.items[0].metadata.name}")

  2. kubectl port-forward $POD_NAME 9000 --namespace minio

Read more about port forwarding here: http://kubernetes.io/docs/user-guide/kubectl/kubectl_port-forward/

You can now access Minio server on http://localhost:9000. Follow the below steps to connect to Minio server with mc client:

  1. Download the Minio mc client - https://docs.minio.io/docs/minio-client-quickstart-guide

  2. Get the ACCESS_KEY=$(kubectl get secret minio -o jsonpath="{.data.accesskey}" | base64 --decode) and the SECRET_KEY=$(kubectl get secret minio -o jsonpath="{.data.secretkey}" | base64 --decode)

  3. mc alias set minio-local http://localhost:9008 "$ACCESS_KEY" "$SECRET_KEY" --api s3v4

  4. mc ls minio-local

```

