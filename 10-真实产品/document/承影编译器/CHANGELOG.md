# 《承影低代码开发工具》- Changelog
[raines]:http://192.168.18.23/zeylei
[duanzhiqiang]:http://192.168.18.23/duanzhiqiang
[penglunjiao]:http://192.168.18.23/penglunjiao
[coder]:http://192.168.18.23/rdcenter/algorithm/ChengYing-Backend-Coder
[storage]:http://192.168.18.23/rdcenter/algorithm/storage
[mapper]:http://192.168.18.23/rdcenter/algorithm/ChengYing-Backend-Mapper
[composer]:http://192.168.18.23/rdcenter/algorithm/ChengYing-Frontend-Composer
[designer]:http://192.168.18.23/rdcenter/algorithm/ChengYing-Frontend-Designer
### 当前项目
简称|英文名|全称|负责人
-|-|-|-
[设计器][designer]| designer| 页面设计工具|[彭论姣][penglunjiao]
[编排器][composer]| composer| 逻辑编排工具|[彭论姣][penglunjiao]
[生成器][coder]| coder| 代码生成工具|[雷泽宇][raines]
[映射器][mapper]| mapper| 关系映射工具|[雷泽宇][raines]
[存储器][storage]| storage| 数据存储工具|[段志强][duanzhiqiang]
### 当前团队
姓名|职责|联系方式
-|-|-
[雷泽宇][raines]| 项目经理、算法工程师|wx: raines1220
[段志强][duanzhiqiang]| 后端工程师|phone:18583920528
[彭论姣][penglunjiao]| 前端工程师|phone:15074851533

## [Unreleased]
### Added
##### 页面设计工具
- 支持Vue代码生成 by [@雷泽宇][raines]
- 新增数据源面板，支持新增变量 by [@彭论姣][penglunjiao]

## [0.6.5] - 2021-6-23
### Added
##### 页面设计工具
- 新增文本、卡片组件 by [@彭论姣][penglunjiao]
- 属性面板新增属性配置列比例、列间距、行间距、内容、最大行数、尺寸、按钮类型 by [@彭论姣][penglunjiao]
- 样式面板新增宽、高、margin、padding、文字、不透明度 by [@彭论姣][penglunjiao]

##### 逻辑编排工具
- 配置查询、流程图及服务文档等多个接口，对应增删改查功能的单元测试 by [@段志强][duanzhiqiang]

## [0.6.5] - 2021-6-15
### Added
##### 页面设计工具
- 组件增加复制功能 by [@彭论姣][penglunjiao]
- 整体页面改装成组件渲染功能 by [@彭论姣][penglunjiao]
- 实现了高性能的“下一步”、“上一步”功能 by [@彭论姣][penglunjiao]
- 操作历史保存到本地，重新打开浏览器后，可以自动显示上一次编辑的页面 by [@彭论姣][penglunjiao]

### Changed
##### 页面设计工具、逻辑编排工具
- 接口名称命名不规范，现在已经统一进行了更改 by [@段志强][duanzhiqiang]
- 实体类及实现类命名规则不统一，进行已经统一更改 by [@段志强][duanzhiqiang]
- 接口地址不符合规范，已经根据接口文档中的Restful规范进行改动 by [@段志强][duanzhiqiang]
- 多个服务复用了一个服务的log，现在已经进行了区分 by [@段志强][duanzhiqiang]
- 原始项目代码文件结构比较乱，现在已经进行了整理 by [@段志强][duanzhiqiang]
- 更新数据时，data不再返回ID信息，而是直接置空 by [@段志强][duanzhiqiang]
### Fixed
##### 页面设计工具
- 多个服务复用了一个服务的log，现在已经进行了区分 by [@段志强][duanzhiqiang]
- 修复了更新接口时会误删内容的bug by [@段志强][duanzhiqiang]
- 修复了删除空数据时不报错的问题，已经增加了相应的报错 by [@段志强][duanzhiqiang]
- 新增相同数据时，新增接口不会报错，现已修复 by [@段志强][duanzhiqiang]
- 修复了查询基础组件，得到的却是复合组件的问题 by [@段志强][duanzhiqiang]

