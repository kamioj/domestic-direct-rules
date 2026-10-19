# 本机常用软件直连补充

检查日期：2026-10-19。仅修改本地规则，未提交、发布订阅或修改客户端运行配置。

## 本机证据

通过 Win32_Process 确认 Weixin.exe、WXWork.exe、cloudmusic.exe、HBuilderX.exe、GameViewer.exe 及 GameViewerServer.exe 均在运行。UU 远程仍沿用 GameViewer 进程名；公开记录不保存本机安装路径。

一次已建立 TCP 连接计数：微信 3、企业微信 116、网易云音乐 5、GameViewerServer 1、HBuilderX 0。计数只代表采样时刻，不表示连通性验收。没有保存远端设备地址、会话内容、进程命令行或凭据。DNS 缓存筛选没有返回可用的匹配主机记录，未据此推断应用没有域名请求。

## 已覆盖与新增

| 应用 | 已有规则覆盖 | 本次补充 | 证据及限制 |
|---|---|---|---|
| 微信 | weixin.qq.com、wx.qq.com、res.wx.qq.com、下载入口均被 qq.com 覆盖 | www.wechat.com、wx.qlogo.cn、mmbiz.qpic.cn | 官网直接链接 WeChat；头像与图片以腾讯官方文档为依据，仅精确主机 |
| 企业微信 | work.weixin.qq.com、open.work.weixin.qq.com、wwcdn.weixin.qq.com 等被 qq.com 覆盖 | wework.qpic.cn | 腾讯官方企业微信文档出现该图片主机；没有整域放行 myqcloud.com |
| 网易云音乐 | music.163.com、st.music.163.com、y.music.163.com、music.126.net 下资源 | 无需重复条目 | 实际读取 music.163.com 公开首页，发现 p1/p3/p5/p6/s1/s2/s3/s4/s5.music.126.net，均已覆盖 |
| UU 远程 | uuyc.163.com、uu.163.com | gv.res.netease.com、uuyc.res.netease.com、uuyc-res.fp.ps.netease.com、gameviewer.qiyukf.com | 官网 HTML 直接引用；没有把所有网易资源、广告统计、外链一起放行 |
| HBuilderX | 此前缺失 | account/ext/stream.dcloud.net.cn、ide/update.liuyingyong.cn、ide.dcloud.io、download1.dcloud.net.cn、hx.dcloud.net.cn | DCloud 员工官方回复列出的六个主机，加官方文档与下载主机；不整体放行开发者托管内容 |

## 官方来源

- 微信官网：https://weixin.qq.com/ （实际读取公开首页链接）
- 企业微信官网：https://work.weixin.qq.com/ （实际读取公开首页链接）
- 微信头像示例：https://wx.gtimg.com/static/cdn/pay_mkt/pay_guide_service/mock/product_documentation.pdf
- 微信图片主机：https://main.qcloudimg.com/raw/document/product/pdf/213_15385_cn.pdf
- 企业微信图片示例：https://main.qcloudimg.com/raw/document/product/pdf/1318_53205_cn.pdf
- 网易云音乐：https://music.163.com/ （实际读取公开首页资源主机）
- UU 远程：https://uuyc.163.com/ （实际读取公开首页资源与客服主机）
- HBuilderX 官方员工答复：https://ask.dcloud.net.cn/question/140034
- HBuilderX 网络文档：https://hx.dcloud.net.cn/Tutorial/Other/hx_domain_list （网页抓取未呈现清单正文，六个主机依据上项官方答复）
- 官方下载主机引用：https://hx.dcloud.net.cn/ExtensionTutorial/views

## 边界与后续验证

- 本次新增 16 条精确主机规则，总计 41 条。不是五个程序的所有流量放行，也不是系统防火墙规则。
- 官网引用只证明主机用于产品入口或资源，不证明运行中的客户端此刻访问了该主机。
- 未执行登录、发消息、音乐播放、远程控制、插件安装或云打包测试。
- UU 远程点对点连接可能使用 IP/UDP；域名清单不能保证其全部连接直连。不能将远端用户地址加入公共规则。
- HBuilderX 插件、自建项目、npm/GitHub、云打包资源等可能有额外依赖；不批量放行整个 IDE 进程，避免其代理/AI 请求被带入直连。
- 第三方头像主机、共享 CDN 和缺少本轮充分依据的域名暂未加入；后续按实际客户端命中记录补充，不宣称零遗漏。
