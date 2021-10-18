## token是什么

##### Token的引入：

Token是在客户端频繁向服务端请求数据，服务端频繁的去数据库查询用户名和密码并进行对比，判断用户名和密码正确与否，并作出相应提示，在这样的背景下，Token便应运而生。

##### Token的定义：

Token是服务端生成的一串字符串，以作客户端进行请求的一个令牌，当第一次登录后，服务器生成一个Token便将此Token返回给客户端，以后客户端只需带上这个Token前来请求数据即可，无需再次带上用户名和密码。

##### 使用Token的目的：

Token的目的是为了减轻服务器的压力，减少频繁的查询数据库，使服务器更加健壮。

##### jwt组成

一个JWT实际上就是一个字符串，它由三部分组成，头部、载荷与签名。
头部(Header)
头部用于描述关于该JWT的最基本的信息，例如其类型以及签名所用的算法等。这也可以 被表示成一个JSON对象。在头部指明了签名算法是HS256算法。 我们进行BASE64编码

```
eqJ0eZSiOiJKV1QiLSJhbGciOiJSUzI2NiJ0
复制代码
```

载荷
载荷就是存放有效信息的地方。然后将其进行base64编码，得到Jwt的第二部分。

```
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9
复制代码
```

签证
jwt的第三部分是一个签证信息，这个签证信息由三部分组成:

header (base64后的)
payload (base64后的)
secret

这个部分需要base64加密后的header和base64加密后的payload使用.连接组成的字符 串，然后通过header中声明的加密方式进行加盐secret组合加密，然后就构成了jwt的第 三部分。

```
TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
复制代码
```

将这三部分用.连接成一个完整的字符串,构成了最终的jwt:

```
eqJ0eZSiOiJKV1QiLSJhbGciOiJSUzI2NiJ0.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
复制代码
```

我在项目中的应用是，为了安全性考虑，当客户端登录系统以后服务端会生成token令牌，服务端返回给客户端，客户端拿到生成的token以后会保存到浏览器的localstorage里面，然后每次ajax发送请求，先去localstorage里面拿到生成的token值，作为head里面的参数传给服务端，服务端拿到请求头以后作解析判断。

## 项目代码

##### 登录服务端模块

```
      String token = jwtUtil.createJWT("1", "jijiadmin", "admin");
        Map<String,Object> params = new HashMap<>();
        params.put("token",token);
        params.put("role","admin");
        return R.ok().data(params);
复制代码
```

##### 登录前端模块

```
$.ajax({
	type: "post",
	url: "http://localhost:8008/test/login",
	datatype: "json",
	success: function(rep){
	localStorage.setItem("temp",rep.data.token);
	window.location.href="index.html"
	}
	})
复制代码
```

##### 服务端拦截器模块

获取请求头key值为Authorization，对里面的数据进行解析，获取到token以后再对token进行解析如果在有效期内，就放行

```
  String header = request.getHeader("Authorization");

        if (header!=null&&!"".equals(header)){
            if(header.startsWith("Bearer ")){
                String token = header.substring(7);
                try{
                    Claims claims = jwtUtil.parseJWT(token);
                    String roles = claims.get("roles").toString();
                    if (roles!=null||roles.equals("admin")){
                        request.setAttribute("claims_admin",claims);
                    }
                    System.out.println("码对");

                }catch (Exception e){
                    System.out.println("码不对");
                   throw new RuntimeException("令牌不对");
                }
            }
        }
        return true;
    }
复制代码
```

##### 删除功能服务端模块

收到客户端发送的请求后，先通过拦截器验证，如果正确就返回删除成功，如果获取的token不正确，就返回权限不足（也可以显示登录已过期或者重新登录）

```
Claims claims_admin = (Claims) request.getAttribute("claims_admin");
       // System.out.println("token:"+token);
        Map<String, Object> params = new HashMap<>();
        if (claims_admin==null){
            System.out.println("权限不足1111");
            params.put("json","删除失败权限不足");
            return R.error().data(params);
        }

        params.put("json","删除成功delete");
        return R.ok().data(params);
复制代码
```