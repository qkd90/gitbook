### gitbook目录如何自动生成

#### 1.首先安装插件包

```
$ npm i gitbook-plugin-summary --save

```

#### 2.需要添加 `book.json` the plugin, like this

```
{
  "plugins": [
    "summary"
  ]
}
```

#### 3.最后运行

```
$ gitbook serve
```