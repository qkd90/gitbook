## mysql

```shell
sudo docker run -p 3306:3306 --name mysql \
-v /usr/local/docker/mysql/mysql-files:/var/lib/mysql-files \
-v /usr/local/docker/mysql/conf:/etc/mysql \
-v /usr/local/docker/mysql/logs:/var/log/mysql \
-v /usr/local/docker/mysql/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=Trasen@8812 \
-d mysql:8.0.43
```

## redis

```shell
docker run -itd --name redis -p 6379:6379 redis
```

## minio

```shell
docker run -p 9000:9000 -p 9002:9002 --name minio \
 -d --restart=always \
 -e MINIO_ACCESS_KEY=minio \
 -e MINIO_SECRET_KEY=minio@123 \
 -v /ssd/minio/data:/data \
 -v /ssd/minio/config:/root/.minio \
  minio/minio server /data  --console-address ":9002"
```

### 配置https

```shell
MINIO_DOMAIN=mentalcare.trasen.cn 
MINIO_ROOT_USER=minio 
MINIO_ROOT_PASSWORD=minio@123 minio server /home/ubuntu/minio/data 
--address "172.17.0.1:9000" 
--console-address ":9002"
```

```shell
[Unit]
Description=Minio Service
After=network.target

[Service]
Type=simple
User=minio-user
Group=minio-group
Environment="MINIO_DOMAIN=mentalcare.trasen.cn MINIO_ROOT_USER=minio MINIO_ROOT_PASSWORD=minio@123"
ExecStart=/usr/local/bin/minio server /home/ubuntu/minio/data --address "172.17.0.1:9000" --console-address ":9002"
Restart=on-failure

[Install]
WantedBy=multi-user.target

```

证书配置

```shell
docker run -d \
  --name minio2 \
  -p 9000:9000 \
  -p 9002:9002 \
  -v /home/ubuntu/minio/data:/data \
  -v /home/ubuntu/.minio/certs:/root/.minio/certs \
  -e "MINIO_DOMAIN=mentalcare.trasen.cn" \
  -e "MINIO_ROOT_USER=minio" \
  -e "MINIO_ROOT_PASSWORD=minio@123" \
  minio/minio server /data  --console-address ":9002"
```



## portainer

```shell
docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce
# 指定版本  
docker run -d -p 8000:8000 -p 9443:9443 --name=portainer --restart=always portainer/portainer-ce:2.18.2
# 运行portainerUI图形界面
# -d后台运行 --name 命名 -p 端口映射(需要确认端口号是开放的) -v挂载(后面博客详说)
docker run -d --name portainerUI -p 9010:9000 -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer
```

## nacos

```shell
docker run -d \
-e PREFER_HOST_MODE=ip \
-e MODE=standalone \
-e SPRING_DATASOURCE_PLATFORM=mysql \
-e MYSQL_SERVICE_HOST=192.168.18.17 \
-e MYSQL_SERVICE_PORT=3306 \
-e MYSQL_SERVICE_DB_NAME=nacos \
-e MYSQL_SERVICE_USER=root \
-e MYSQL_SERVICE_PASSWORD=Trasen@8812 \
-e NACOS_APPLICATION_PORT=8848 \
-p 8848:8848 -p 9848:9848 -p 9849:9849 \
--name nacos \
--restart=always \
--privileged=true \
nacos/nacos-server
```

## 禅道

```shell
sudo docker run \
--name zentao \
-p 9005:80 \
-v /ssd/chandao/data:/data \
-e MYSQL_INTERNAL=true \
-d easysoft/zentao:latest 

```

用户名密码：admin / Trasen@8812

