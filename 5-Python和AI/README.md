# Python 和 AI

## 章节定位

本章节记录 Python 环境管理、FastAPI 服务部署、Hugging Face、DeepSeek、CGMformer 等 AI 相关实践，适合作为 Java 后端之外的工程扩展能力。

## 技术路线

```text
Python 基础环境
  ├─ Miniconda / Anaconda
  ├─ PyCharm 配置
  └─ 虚拟环境和依赖管理

Web 服务
  ├─ FastAPI
  ├─ 接口部署
  └─ 服务启动和日志

AI 模型
  ├─ Hugging Face
  ├─ DeepSeek-R1 部署
  ├─ 模型代码总结
  └─ CGMformer
```

## 推荐阅读顺序

1. Anaconda3 相关配置。
2. PyCharm + Miniconda3 配置项目启动。
3. Python 环境 + FastAPI 服务部署。
4. Hugging Face 和模型代码总结。
5. DeepSeek-R1、CGMformer 等具体模型实践。

## 工程建议

- 每个 Python 项目都要使用独立虚拟环境。
- 依赖版本写入 `requirements.txt` 或 `environment.yml`。
- 模型文件和代码分开管理，避免把大模型权重提交到 Git。
- 服务部署时要关注显存、内存、并发、超时和日志。
