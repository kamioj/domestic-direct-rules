# 首版筛选记录

审核日期：2026-10-19（Asia/Shanghai）。

## 候选来源

既有 ChinaMax 文件声明来源为 blackmatrix7/ios_rule_script，文件头标注更新时间 2024-11-05。实际下载内容为 101,752 条；头部声称 114,201 条，与实际不一致。此次不盲信头部统计，不整包继承。

上游项目：https://github.com/blackmatrix7/ios_rule_script

为避免发布私人订阅路径，本仓库不存放用户原规则源 URL、设备路径或完整配置。候选快照的哈希和统计见 `source-summary.json`。

## 方法

按人工允许清单选取可明确归属的国内服务域名，而非按字符串像中文、以 cn 结尾或 IP 地理位置自动推断。源中的 21 个具体域名后缀保留；原本整个 cn 的放行收窄成 12306.cn，共 22 条。其他条目没有进入首版，不代表它们都属于国外。

| 服务 | 收录范围 | 归属/产品核查入口 | 范围说明 |
|---|---|---|---|
| 腾讯 | qq.com | https://www.tencent.com/zh-cn/what-we-create/ ; https://en.security.tencent.com/policy | 用户明确接受腾讯整域服务范围；不放行整个腾讯云 |
| 网易 | 163.com、126.com、126.net | https://ir.netease.com/company-overview/products | 门户、邮箱及资源体系；用户接受 163.com 整域，不以服务器所在地保证 |
| 京东 | jd.com、360buyimg.com | https://www.jd.com/ | 官方页面版权和 360buyimg 资源链接；整域可能包含跨境业务 |
| 淘宝、天猫 | taobao.com、tmall.com | https://www.alibabagroup.com/en-US/about-businesses ; https://www.tmall.com/ | 国内电商服务体系；不放行整个 alicdn、aliyuncs 或 alipay |
| 哔哩哔哩 | bilibili.com、hdslb.com、biliimg.com、bilivideo.com | https://www.bilibili.com/ ; https://www.bilibili.com/protocal/privacy-pc-desktop.html | 主站及专用资源；资源域名结合上游服务分类核对 |
| 美团、大众点评 | meituan.com、meituan.net、dianping.com | https://www.meituan.com/ ; https://www.dianping.com/ | 生活服务及专用资源；美团页面引用 meituan.net。dpfile.com 在所查美团细分规则中未找到，首版暂不收录 |
| 豆瓣 | douban.com、doubanio.com | https://www.douban.com/ | 页面直接引用 doubanio 资源 |
| 知乎 | zhihu.com、zhimg.com | https://www.zhihu.com/explore | 主站及专用资源，结合上游服务分类核对 |
| 高德 | amap.com、autonavi.com | https://www.amap.com/ ; https://a.autonavi.com/outer/index.jsp | 地图/导航服务，包含 API；不承诺只服务境内用户 |
| 铁路 12306 | 12306.cn | https://www.12306.cn/ | 从 cn 宽泛后缀中单独保留，不使用 12306.com 替代官方域名 |

服务归属核查不等于每个域名都经过实际流量、DNS、IP 地理位置或所有子域审核；首次仅做静态筛选。所有权、子域用途可能变化，需要持续复核。

资源域名交叉核对来源：

- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/BiliBili/BiliBili.yaml （包含 biliimg.com、bilivideo.com）
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Zhihu/Zhihu.yaml （包含 zhimg.com）

## 明确剔除的类别

- IP-CIDR、IP-CIDR6、IP-ASN、PROCESS-NAME、DOMAIN-KEYWORD。
- cn 等整顶级域、微软/Apple 宽泛 IP 放行。
- recaptcha.net、CF 相关名字、stripe 关键词、共享云/CDN。
- 无法从候选和产品依据明确判断用途的条目，暂不收录。

源许可证按 GPL-2.0 保留，见 LICENSE；本次不把上游数据重新声明为独占作品。正式规则不包含源文件中的私人订阅信息。
