# CollegeNetManager
校园网认证登录管理器

简介:
  基于校园网 Web端 认证登录上网, 通过在浏览器中获取登录时的 Request Headers 信息, 借助 requests库 实现自动化的认证登录.
  实现目标:
    1. 认证登录/登出/状态检查
    2. 账户管理
    3. 网卡启/禁用管理(校园网断网之后, 同时有线连接校园网, WIFI 连接热点时可能造成抢占导致的无法正常上网.)
