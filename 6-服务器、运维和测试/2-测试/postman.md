# Postman 使用指南

## 适用场景

Postman 主要用于接口调试、联调验收、环境变量管理和简单自动化测试。后端接口交付前，至少应使用 Postman 验证正常请求、异常请求、权限请求和边界参数。

## 基本使用

### 创建请求

1. 新建 Collection。
2. 新建 Request。
3. 选择请求方法，例如 `GET`、`POST`、`PUT`、`DELETE`。
4. 填写 URL。
5. 配置 Header、Params、Body。
6. 点击 Send 发送请求。

### 常见 Header

| Header | 说明 |
| --- | --- |
| `Content-Type: application/json` | 请求体为 JSON |
| `Authorization: Bearer xxx` | token 鉴权 |
| `Cookie: token=xxx` | Cookie 鉴权 |
| `tenant-id: xxx` | 租户标识 |

## 环境变量

创建环境变量后，请求地址可以这样写：

```text
{{baseUrl}}/api/users
```

常用变量：

| 变量 | 示例 |
| --- | --- |
| `baseUrl` | `http://127.0.0.1:8080` |
| `token` | 登录后返回的 token |
| `tenantId` | 当前租户 ID |
| `userId` | 当前用户 ID |

Header 中引用：

```text
Authorization: Bearer {{token}}
```

## 登录后自动保存 token

在登录接口的 Tests 中写入：

```javascript
const json = pm.response.json();
pm.environment.set("token", json.data.token);
```

后续接口即可通过 `{{token}}` 使用。

## 接口断言

```javascript
pm.test("状态码为 200", function () {
    pm.response.to.have.status(200);
});

pm.test("业务码成功", function () {
    const json = pm.response.json();
    pm.expect(json.code).to.eql(200);
});
```

## 常用 Body

### JSON

```json
{
  "name": "张三",
  "age": 18
}
```

### form-data

适合文件上传：

```text
file: 选择本地文件
type: avatar
```

### x-www-form-urlencoded

适合传统表单：

```text
username=admin
password=123456
```

## 联调检查清单

- 请求方法是否正确。
- 请求地址是否包含网关前缀。
- Header 中 token、租户、Content-Type 是否正确。
- Body 是否为合法 JSON。
- 时间格式是否与后端约定一致。
- 分页参数是否传递。
- 异常参数是否返回明确错误。

## 常见问题

### 后端拿不到 JSON 参数

检查：

- Header 是否设置 `Content-Type: application/json`。
- Body 是否选择 `raw` 和 `JSON`。
- JSON 是否存在多余逗号或注释。

### token 未生效

检查：

- Header 名称是否和后端一致。
- 是否缺少 `Bearer ` 前缀。
- 当前环境变量是否选对。
- 登录接口是否把 token 保存到了当前环境。

### 文件上传失败

检查：

- Body 是否选择 `form-data`。
- 文件字段名是否与后端 `MultipartFile` 参数一致。
- 不要手动设置 `Content-Type`，让 Postman 自动生成 boundary。
