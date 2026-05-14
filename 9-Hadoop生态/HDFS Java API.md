# HDFS Java API

## 概述

HDFS 提供了 Java API，允许通过编程方式操作 HDFS 中的文件和数据。

## 环境准备

### Maven 依赖

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.hadoop</groupId>
        <artifactId>hadoop-client</artifactId>
        <version>3.X.X</version>
    </dependency>
    <dependency>
        <groupId>junit</groupId>
        <artifactId>junit</artifactId>
        <version>4.13.2</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

## FileSystem 类

`FileSystem` 是 HDFS Java API 的核心类，所有文件操作都通过它完成。

### 获取 FileSystem 实例

```java
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import java.net.URI;

public class HDFSClient {
    private FileSystem fs;

    public void init() throws Exception {
        Configuration conf = new Configuration();
        // 设置 HDFS 地址
        URI uri = new URI("hdfs://hadoop102:9000");
        // 设置用户名（如果不设置，默认使用当前系统用户）
        conf.set("fs.defaultFS", "hdfs://hadoop102:9000");
        // 获取 FileSystem 实例
        fs = FileSystem.get(uri, conf, "hadoop");
    }

    public void close() throws Exception {
        fs.close();
    }
}
```

## 文件操作

### 1. 创建目录

```java
public void mkdir() throws Exception {
    boolean result = fs.mkdirs(new Path("/test/java_api"));
    System.out.println("创建目录：" + result);
}
```

### 2. 上传文件

```java
public void putFile() throws Exception {
    // 参数1：是否删除源文件
    // 参数2：是否覆盖
    // 参数3：本地路径
    // 参数4：HDFS路径
    fs.copyFromLocalFile(false, true,
        new Path("D:/test.txt"),
        new Path("/test/java_api/"));
}
```

### 3. 下载文件

```java
public void getFile() throws Exception {
    // 参数1：是否使用本地文件系统
    // 参数2：HDFS路径
    // 参数3：本地路径
    // 参数4：是否使用原始本地文件系统
    fs.copyToLocalFile(false,
        new Path("/test/java_api/test.txt"),
        new Path("D:/download/"),
        true);
}
```

### 4. 删除文件/目录

```java
public void delete() throws Exception {
    // 参数2：是否递归删除
    boolean result = fs.delete(new Path("/test"), true);
    System.out.println("删除结果：" + result);
}
```

### 5. 文件重命名

```java
public void rename() throws Exception {
    boolean result = fs.rename(
        new Path("/test/java_api/test.txt"),
        new Path("/test/java_api/renamed.txt"));
    System.out.println("重命名结果：" + result);
}
```

### 6. 查看文件详情

```java
public void listFiles() throws Exception {
    RemoteIterator<LocatedFileStatus> iterator =
        fs.listFiles(new Path("/"), true);

    while (iterator.hasNext()) {
        LocatedFileStatus file = iterator.next();
        System.out.println("文件路径：" + file.getPath());
        System.out.println("文件权限：" + file.getPermission());
        System.out.println("文件所有者：" + file.getOwner());
        System.out.println("文件块大小：" + file.getBlockSize());
        System.out.println("文件大小：" + file.getLen());

        // 获取块信息
        BlockLocation[] blockLocations = file.getBlockLocations();
        for (BlockLocation block : blockLocations) {
            String[] hosts = block.getHosts();
            System.out.println("块所在节点：" + Arrays.toString(hosts));
        }
        System.out.println("-------------------");
    }
}
```

### 7. 查看目录信息

```java
public void listStatus() throws Exception {
    FileStatus[] statuses = fs.listStatus(new Path("/"));
    for (FileStatus status : statuses) {
        System.out.println("路径：" + status.getPath());
        System.out.println("是否是目录：" + status.isDirectory());
        System.out.println("权限：" + status.getPermission());
        System.out.println("所有者：" + status.getOwner());
    }
}
```

## 文件读写

### 1. 写入文件

```java
public void writeFile() throws Exception {
    // 创建输出流
    FSDataOutputStream out = fs.create(new Path("/test/output.txt"));
    // 写入数据
    out.writeUTF("Hello HDFS!");
    out.write("Hello World\n".getBytes());
    // 关闭流
    out.close();
}
```

### 2. 读取文件

```java
public void readFile() throws Exception {
    // 创建输入流
    FSDataInputStream in = fs.open(new Path("/test/output.txt"));
    // 读取数据
    byte[] buffer = new byte[1024];
    int len;
    while ((len = in.read(buffer)) != -1) {
        System.out.write(buffer, 0, len);
    }
    // 关闭流
    in.close();
}
```

### 3. 随机读取

```java
public void randomRead() throws Exception {
    FSDataInputStream in = fs.open(new Path("/test/large_file.txt"));
    // 定位到指定位置
    in.seek(1024);
    // 读取数据
    byte[] buffer = new byte[1024];
    in.read(buffer);
    System.out.println(new String(buffer));
    in.close();
}
```

## 完整示例

```java
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.*;
import org.apache.hadoop.io.IOUtils;
import java.net.URI;

public class HDFSExample {
    private FileSystem fs;

    public void init() throws Exception {
        Configuration conf = new Configuration();
        conf.set("fs.defaultFS", "hdfs://hadoop102:9000");
        fs = FileSystem.get(new URI("hdfs://hadoop102:9000"), conf, "hadoop");
    }

    public void close() throws Exception {
        fs.close();
    }

    // 上传文件
    public void upload() throws Exception {
        fs.copyFromLocalFile(false, true,
            new Path("D:/input.txt"),
            new Path("/user/hadoop/"));
    }

    // 下载文件
    public void download() throws Exception {
        fs.copyToLocalFile(false,
            new Path("/user/hadoop/input.txt"),
            new Path("D:/output/"),
            true);
    }

    // 读取文件
    public void read() throws Exception {
        FSDataInputStream in = fs.open(new Path("/user/hadoop/input.txt"));
        IOUtils.copyBytes(in, System.out, 4096, false);
        IOUtils.closeStream(in);
    }

    public static void main(String[] args) throws Exception {
        HDFSExample example = new HDFSExample();
        example.init();

        example.upload();
        example.read();
        example.download();

        example.close();
    }
}
```

## 注意事项

1. **Hadoop 配置**：确保 `core-site.xml` 和 `hdfs-site.xml` 在 classpath 中
2. **权限**：确保用户有权限操作 HDFS
3. **连接**：使用正确的 HDFS 地址和端口
4. **关闭流**：操作完成后关闭 FSDataInputStream 和 FSDataOutputStream

## 总结

HDFS Java API 提供了完整的文件操作接口，通过编程方式可以方便地集成 HDFS 操作到应用中。理解 FileSystem 类的常用方法是使用 HDFS API 的关键。
