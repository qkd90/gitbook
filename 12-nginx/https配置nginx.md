## 配置文件

```nginx
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
    '$status $body_bytes_sent "$http_referer" '
    '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    default_type application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    # 郴州负载均衡
    upstream psychologyhealth {
        server 172.16.109.32:9990;
        server 172.16.109.49:9990;
    }

    server {
        listen 80;
        server_name xljk.cz6yy.com;
        root /trasen;
        #将所有HTTP请求通过rewrite指令重定向到HTTPS。
        rewrite ^(.*)$ https://$host$1 permanent;
    }

    # Settings for a TLS enabled server.
    server {
        #HTTPS的默认访问端口443。
        #如果未在此处配置HTTPS的默认访问端口，可能会造成Nginx无法启动。
        listen 443 ssl;

        #填写证书绑定的域名
        server_name xljk.cz6yy.com;

        #填写证书文件绝对路径
        ssl_certificate /etc/nginx/cert/xljk.cz6yy.com.pem;
        #填写证书私钥文件绝对路径
        ssl_certificate_key /etc/nginx/cert/xljk.cz6yy.com.key;

        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;

        #自定义设置使用的TLS协议的类型以及加密套件（以下为配置示例，请您自行评估是否需要配置）
        #TLS协议版本越高，HTTPS通信的安全性越高，但是相较于低版本TLS协议，高版本TLS协议对浏览器的兼容性较差。
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;
        ssl_protocols TLSv1.1 TLSv1.2 TLSv1.3;

        #表示优先使用服务端加密套件。默认开启
        ssl_prefer_server_ciphers on;

        location ~* /MP_verify_(?<code>[\w\d]+)\.txt$ {
            set $text '';
            set $text '$code';
            default_type text/html;
            return 200 $text;
        }

        location ^~/ts-evaluation {
            alias /trasen/ts-evaluation/;
            try_files $uri $uri/ /ts-evaluation/index.html;
        }

        location ^~/ts-mental {
            # 路径重写这样会根据最长路径匹配
            rewrite ^/ts-mental(.*)$ $1 break;
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_pass http://psychologyhealth;
        }

        location ^~/wechat {
            proxy_pass http://psychologyhealth;
        }

        location ^~/mental-mobile {
            alias /rgzn/mental-mobile/;
            try_files $uri $uri/ /mental-mobile/index.html;
        }

        location / {
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Credentials true;
            proxy_pass https://cms.womei.org/;
        }

        location = /.well-known/pki-validation/fileauth.txt {
            return 200 '202009291209380jldpefa30gdql1tkveotkm20tof9hawbawm1z73gl6n5qff8q';
        }
    }
}


```

