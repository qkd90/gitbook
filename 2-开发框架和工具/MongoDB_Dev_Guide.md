# MongoDB 开发规范与快速上手指南

本文档基于 `sino-service` 项目中的 `ActivityConfigureServiceImpl.java` 代码风格整理，旨在帮助开发者快速上手公司内部 MongoDB 的增删改查（CRUD）开发规范。

## 1. 基础结构

### 1.1 Service 定义
业务 Service 类通常继承自 `BaseServiceImpl<Repository, Entity>` 并实现接口。
- **Repository**: 对应的 MongoDB Repository 接口。
- **Entity**: 对应的 MongoDB 实体类。

```java
@Service
@Slf4j
@RequiredArgsConstructor
public class ExampleServiceImpl extends BaseServiceImpl<ExampleRepository, ExampleEntity> 
        implements IExampleService {
    
    // BaseServiceImpl内部已注入 MongoTemplate，变量名为 template
    // BaseServiceImpl提供了基本的 save, updateById, removeById, getById 等方法
}
```

## 2. 增 (Create)

使用 `save` 方法保存实体。如果实体 ID 为空，则是新增；如果 ID 存在，则是保存（主要用于新增，更新通常用 updateById）。

```java
public void createExample(ExampleReq req) {
    ExampleEntity entity = BeanUtil.copy(req, ExampleEntity.class);
    
    // 初始化默认值
    if (Func.isBlank(entity.getStatus())) {
        entity.setStatus(SinoConstant.DB_STATUS_NORMAL);
    }
    
    // 新增时 ID 设为 null
    entity.setId(null);
    
    // save 方法返回 boolean
    boolean success = this.save(entity);
    if (!success) {
        throw new ServiceException("保存失败");
    }
}
```

## 3. 删 (Delete)

### 3.1 根据 ID 删除
使用 `removeById` 方法。

```java
public void deleteById(String id) {
    boolean success = this.removeById(id);
}
```

### 3.2 根据条件删除
使用 `template.remove` 配合 `Query`。

```java
public void deleteByCondition(String businessId) {
    // 构造查询条件
    Query query = new Query();
    query.addCriteria(Criteria.where("businessId").is(businessId));
    
    // 执行删除
    template.remove(query, ExampleEntity.class);
}
```

## 4. 改 (Update)

### 4.1 全量更新 (按 ID)
先查询出对象，修改属性后，调用 `updateById`。这是最推荐的方式，因为它会处理乐观锁（如果配置了）和 updateTime。

```java
public void updateExample(ExampleReq req) {
    // 1. 先查
    ExampleEntity entity = this.getById(req.getId());
    if (Func.isNull(entity)) {
        throw new ServiceException("数据不存在");
    }
    
    // 2. 拷贝属性/修改值
    BeanUtil.copy(req, entity);
    entity.setUpdateTime(LocalDateTime.now());
    
    // 3. 更新
    this.updateById(entity);
}
```

### 4.2 局部更新 (指定字段)
如果只需要更新个别字段，可以使用 `template.updateFirst` 或 `template.updateMulti`。

```java
public void updateStatusOnly(String id, Integer status) {
    Query query = new Query(Criteria.where("_id").is(id));
    
    Update update = new Update();
    update.set("status", status);
    update.set("updateTime", LocalDateTime.now());
    
    template.updateFirst(query, update, ExampleEntity.class);
}
```

## 5. 查 (Read)

### 5.1 根据 ID 查询
```java
ExampleEntity entity = this.getById(id);
```

### 5.2 根据条件查询单条
使用 `getOne` 配合 `Condition` 或 `Query`。

```java
public ExampleEntity getByName(String name) {
    // 方式1: 使用 QueryBuilder
    Query query = new Query();
    query.addCriteria(Criteria.where("name").is(name));
    query.addCriteria(Criteria.where("isDeleted").is(0)); // 逻辑删除过滤
    
    return this.getOne(query);
}
```

### 5.3 列表查询
```java
public List<ExampleEntity> listByType(Integer type) {
    Query query = new Query();
    query.addCriteria(Criteria.where("type").is(type));
    
    // 使用 template 直接查询
    return template.find(query, ExampleEntity.class);
}
```

### 5.4 分页查询
结合 `Condition.getPage(req)` 和 `Page` 对象。

```java
public IPage<ExampleEntity> page(ExamplePageReq req) {
    // 构造查询条件
    Query query = new Query();
    if (Func.isNotBlank(req.getName())) {
        // 模糊查询
        query.addCriteria(Criteria.where("name").regex(req.getName()));
    }
    
    // 构造分页对象 (Sino封装的IPage)
    IPage<ExampleEntity> page = Condition.getPage(req);
    
    // 计算总数
    long total = template.count(query, ExampleEntity.class);
    page.setTotal(total);
    
    if (total > 0) {
        // 设置分页参数
        query.with(pageToPageable(page)); // 需自行实现Page转Pageable或手动设置skip/limit
        // 或者直接手动设置
        query.skip(page.offset()).limit(page.getSize());
        
        // 执行查询
        List<ExampleEntity> list = template.find(query, ExampleEntity.class);
        page.setRecords(list);
    }
    
    return page;
}
```

## 6. 常用工具类
代码中广泛使用了 `sino-boot` 提供的工具类，通过静态导入使用：

- **Func**: `Func.isEmpty()`, `Func.isNotEmpty()`, `Func.equals()`, `Func.isBlank()`
- **StringPool**: `StringPool.ONE`, `StringPool.ZERO`
- **SinoConstant**: `SinoConstant.DB_STATUS_NORMAL`

## 核心方法

```
where(String key): 指定字段。
is(Object value): 等于。
ne(Object value): 不等于。
gt(Object value): 大于。
lt(Object value): 小于。
gte(Object value): 大于等于。
lte(Object value): 小于等于。
in(Object... values): 在...中。
nin(Object... values): 不在...中。
startsWith(String prefix) / endsWith(String suffix) / contains(String regex): 字符串匹配。
exists(boolean existence): 字段是否存在。
not(): 取反。
and(Criteria... criteria) / or(Criteria... criteria): 组合条件。
```

## 7. 完整示例代码

```java
package com.sino.platform.service.activity.service.impl;

import com.sino.boot.core.common.api.R;
import com.sino.boot.core.common.utils.BeanUtil;
import com.sino.boot.core.common.utils.Func;
import com.sino.boot.plugin.log.exception.ServiceException;
import com.sino.boot.plugin.mongo.base.BaseServiceImpl;
import com.sino.platform.service.demo.entity.DemoEntity;
import com.sino.platform.service.demo.dto.req.DemoSaveReq;
import com.sino.platform.service.demo.dto.req.DemoQueryReq;
import com.sino.platform.service.demo.repository.DemoRepository;
import com.sino.platform.service.demo.service.IDemoService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
@Slf4j
@RequiredArgsConstructor
public class DemoServiceImpl extends BaseServiceImpl<DemoRepository, DemoEntity> 
    implements IDemoService {

    /**
     * 新增/修改
     */
    @Override
    public R submit(DemoSaveReq req) {
        DemoEntity entity = BeanUtil.copy(req, DemoEntity.class);
        
        // 校验逻辑
        if (Func.isBlank(entity.getName())) {
            return R.fail("名称不能为空");
        }

        if (Func.isNotBlank(entity.getId())) {
            // 更新逻辑
            DemoEntity oldEntity = this.getById(entity.getId());
            if (Func.isNull(oldEntity)) {
                throw new ServiceException("数据不存在");
            }
            // 覆盖属性
            BeanUtil.copy(entity, oldEntity);
            oldEntity.setUpdateTime(LocalDateTime.now());
            this.updateById(oldEntity);
        } else {
            // 新增逻辑
            entity.setCreateTime(LocalDateTime.now());
            entity.setUpdateTime(LocalDateTime.now());
            this.save(entity);
        }
        
        return R.data(entity);
    }

    /**
     * 复杂查询示例
     */
    @Override
    public List<DemoEntity> listByCondition(DemoQueryReq req) {
        Query query = new Query();
        
        // 相等匹配
        if (Func.isNotBlank(req.getType())) {
            query.addCriteria(Criteria.where("type").is(req.getType()));
        }
        
        // 模糊查询
        if (Func.isNotBlank(req.getKeyword())) {
            query.addCriteria(Criteria.where("title").regex(req.getKeyword()));
        }
        
        // 范围查询
        if (Func.notNull(req.getStartTime())) {
            query.addCriteria(Criteria.where("createTime").gte(req.getStartTime()));
        }
        
        // 排序
        query.with(org.springframework.data.domain.Sort.by(org.springframework.data.domain.Sort.Direction.DESC, "createTime"));
        
        return template.find(query, DemoEntity.class);
    }
    
    /**
     * 批量操作示例
     */
    @Override
    public void batchUpdateStatus(List<String> ids, Integer status) {
        if (Func.isEmpty(ids)) return;
        
        Query query = new Query(Criteria.where("_id").in(ids));
        Update update = Update.update("status", status)
                              .set("updateTime", LocalDateTime.now());
        
        template.updateMulti(query, update, DemoEntity.class);
    }
}
```
