
本项目支持通过 Docker 进行容器化部署，提供了三种不同的运行模式。

## 快速开始

### 前置要求

- Docker
- Docker Compose
- PyCharm Professional（用于一键部署）

### 部署方式

#### 1. PyCharm 一键部署（推荐）

在 PyCharm 中，你可以直接使用预配置的运行配置：

1. **Flask API 服务**：选择 "Docker Compose - Flask API" 运行配置
2. **FastAPI 服务**：选择 "Docker Compose - FastAPI" 运行配置  
3. **Streamlit 应用**：选择 "Docker Compose - Streamlit" 运行配置

点击运行按钮即可一键部署到 Docker 容器。

#### 2. 命令行部署

**启动 Flask API 服务（默认）：**
```bash
docker-compose up videocaptioner-flask
```

**启动 FastAPI 服务：**
```bash
docker-compose --profile fastapi up videocaptioner-fastapi
```

**启动 Streamlit 应用：**
```bash
docker-compose --profile streamlit up videocaptioner-streamlit
```

**构建并启动所有服务：**
```bash
docker-compose --profile fastapi --profile streamlit up --build
```

## 服务端口

- **Flask API**: http://localhost:10006
- **FastAPI**: http://localhost:8000
- **Streamlit**: http://localhost:8501

## 环境变量配置

可以通过环境变量来配置应用：

```bash
# 对于 Streamlit 应用，可能需要配置 OpenAI 相关变量
export OPENAI_BASE_URL="your_openai_base_url"
export OPENAI_API_KEY="your_openai_api_key"
```

## 数据持久化

容器会将以下目录挂载到宿主机：

- `./temp` -> `/app/temp`：临时文件存储
- `./AppData` -> `/app/AppData`：应用数据和模型文件

## 健康检查

所有服务都配置了健康检查，Docker 会自动监控服务状态。

## 故障排除

### 常见问题

1. **端口冲突**：确保指定端口未被其他服务占用
2. **权限问题**：确保 Docker 有权限访问项目目录
3. **模型文件缺失**：首次运行时需要下载模型文件到 `AppData/models` 目录

### 查看日志

```bash
# 查看特定服务日志
docker-compose logs videocaptioner-flask
docker-compose logs videocaptioner-fastapi
docker-compose logs videocaptioner-streamlit

# 实时查看日志
docker-compose logs -f videocaptioner-flask
```

### 重新构建

```bash
# 重新构建镜像
docker-compose build --no-cache

# 清理并重新启动
docker-compose down
docker-compose up --build
```

## 开发模式

如果需要在开发过程中实时更新代码，可以将源代码目录挂载到容器：

```yaml
volumes:
  - .:/app
  - ./temp:/app/temp
  - ./AppData:/app/AppData
```

## 生产部署建议

1. 使用具体的镜像标签而不是 `latest`
2. 配置适当的资源限制
3. 使用外部数据库和存储服务
4. 配置反向代理（如 Nginx）
5. 启用 HTTPS
6. 配置日志轮转
7. 设置监控和告警

## API 文档

- **Flask API**: 访问 http://localhost:10006 查看可用接口
- **FastAPI**: 访问 http://localhost:8000/docs 查看 Swagger 文档
- **Streamlit**: 访问 http://localhost:8501 使用 Web 界面