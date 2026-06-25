# Nginx

## 章节定位

Nginx 常用于反向代理、负载均衡、静态资源服务、HTTPS 终止和网关入口。本目录整理 Nginx 基础命令、安装部署和常见配置示例。

## 常用场景

- 前端静态资源部署。
- 后端服务反向代理。
- 多实例负载均衡。
- HTTPS 证书配置。
- 文件下载和上传限制。
- 访问日志和错误日志排查。

## 基本配置结构

```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        root /data/www;
        index index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8080/;
    }
}
```

## 发布检查

```bash
nginx -t
systemctl reload nginx
systemctl status nginx
tail -f /var/log/nginx/error.log
```

## 常见问题

- 访问 404：检查 `root`、`alias`、路径和文件权限。
- 接口 502：检查后端服务是否启动、端口是否正确。
- 上传失败：检查 `client_max_body_size`。
- HTTPS 异常：检查证书路径、域名和有效期。
