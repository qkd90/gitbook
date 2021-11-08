# linux上用docker部署nginx

#### 拉取nginx官方镜像

```
docker pull nginx
```

#### 运行nginx镜像并进入容器

```
docker run -ti nginx /bin/bash
```

/bin/bash的只能用一下很基本的unix命令，我们ls一下发现nginx容器有以下目录



![img](https://upload-images.jianshu.io/upload_images/6955829-1dbcd4fbb8d38369.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1042/format/webp)



其中nginx的配置目录在/etc/nginx

这样我们就运行了一个基本的nginx容器了，但是怎么样才能外部能访问到呢，我们可以映射容器的端口到外部主机端口。

```
docker run -p 8888:80 -d nginx
```

![img](https://upload-images.jianshu.io/upload_images/6955829-7d787e6378ca0e81.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1200/format/webp)

这样我们就将外部的8888端口指向nginx容器的80端口了，OK，打开浏览器测试一下



![img](https://upload-images.jianshu.io/upload_images/6955829-56e749cda1b3098e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/642/format/webp)

可是我们每次要修改nginx的配置都要进入到容器内部去修改是不是太麻烦了，ok，目录也来映射一下。
先停止刚刚启动的容器

```
docker stop 268527ecab7c
```

在主机上创建目录/disk2/docker/nginx,在该目录下创建conf，logs，www三个目录，分别是干什么的也不用我多说了吧。
然后执行

```
 docker run -p 8888:80 -v /disk2/docker/nginx/conf:/etc/nginx/conf.d -v /disk2/docker/nginx/www:/usr/share/nginx/html -v /disk2/docker/nginx/logs:/var/log/nginx -d nginx
```

在/disk2/docker/nginx/conf目录下新增文件default.conf,写入

```
server {
    listen       80;
    server_name  localhost;

    #charset koi8-r;
    access_log  /var/log/nginx/access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}
```

然后在/disk2/docker/nginx/www目录下新增文件index.html,写入

```
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx in docker!</title>
<body>
<h1>docker!!!!</h1>
</body>
</html>
```

查看结果



![img](https://upload-images.jianshu.io/upload_images/6955829-2b8177fcdceabf0f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1200/format/webp)



![img](https://upload-images.jianshu.io/upload_images/6955829-dcdb80cfde55ac2a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/465/format/webp)

这样就能将容器内的目录映射到外部的目录去了，修改配置或查看日志便不用进入容器中去修改了