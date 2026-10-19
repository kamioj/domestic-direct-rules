# OSS Browser 与汽水音乐

日期：2026-10-19。本轮只整理本地规则，没有修改客户端或发布订阅。

## 汽水音乐

官方入口：https://qishui.douyin.com/ 。页面标明开发者为北京抖音科技有限公司；没有采用搜索结果中自称官网的第三方下载站。

实际读取该公开 HTML，提取主机名，不下载或运行安装包：
- qishui.douyin.com、luna-web.douyin.com、music.douyin.com：已由 douyin.com 覆盖。
- p26-luna.douyinpic.com：已由 douyinpic.com 覆盖。
- www.qishui.com、lf-luna.qishui.com、lf-luna-release.qishui.com：新增三个精确主机。
- bytescm.com、ibytedapm.com、edge-byted.com 等共享服务没有整域加入。

规则总计 92 条。此证据涵盖官网和发布资源，不证明客户端播放、登录、音频 CDN 全部直连；没有 Mac 实测或播放测试。

## OSS Browser

阿里云官方仓库明确支持 Mac：
https://github.com/aliyun/oss-browser

官方 Endpoint 说明：
https://www.alibabacloud.com/help/en/oss/user-guide/access-oss-via-bucket-domain-name

官方 2.0 登录说明：
https://www.alibabacloud.com/help/en/oss/developer-reference/login-to-ossbrowser-2-0

用户存储桶访问地址通常由 bucket、地域 endpoint 或自定义域名决定，不存在仅凭“OSS Browser”产品名即可覆盖所有个人业务请求的专用域名。当前没有获取用户的实际 Endpoint、存储桶域名或版本，没有读取 AccessKey 或访问存储桶。

官方仓库引用下载主机 oss-attachment.oss-cn-zhangjiakou.aliyuncs.com，但这是公共安装包下载，不是用户的数据存储桶；本轮未新增共享云规则，现有代理路由仍保留。

待补项：实际 Endpoint / 自定义域名。具体存储桶规则应仅写入 home/private 下的本地覆写，不放入公共规则仓库。不添加 aliyuncs.com 后缀、不按所有地域批量放行，也不为了此项解除规则校验器的共享云保护。

本机进程名匹配 oss-browser/ossbrowser/qishui/luna 未发现匹配项；只说明此时此匹配范围未发现，不能据此判断 Mac 安装或运行状态。
