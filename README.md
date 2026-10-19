# 国内服务直连白名单

从既有 ChinaMax 候选中人工筛选、收窄的域名规则。适用于 FlClash / Clash Nyanpasu 等支持 Mihomo classical RULE-SET 的客户端。

**只提供规则集，不是完整代理配置。** 不包含节点、DNS、VPN 接管或断网保护设置。创建和更新仓库不会修改任何设备配置。

另含用户指定的 IDEA/WebStorm、Navicat、Termius 官方服务直连例外，因此名称中的“国内服务”不代表全部条目位于境内。Mac 应用依据与尚未覆盖的功能见 [docs/mac-apps-2026-10-19.md](docs/mac-apps-2026-10-19.md)。不按整个开发工具进程放行。

## 订阅地址

正式地址（仅发布通过自动校验的版本）：

```text
https://raw.githubusercontent.com/kamioj/domestic-direct-rules/release/rules/domestic-direct.yaml
```

## 接入示例（请合并到现有配置，不要用它覆盖整份配置）

```yaml
rule-providers:
  domestic-direct:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/kamioj/domestic-direct-rules/release/rules/domestic-direct.yaml
    path: ./ruleset/domestic-direct.yaml
    interval: 3600
    proxy: Proxy

rules:
  # 现有 Claude、验证、登录等强制代理规则放在这里，优先匹配。
  # 必要的局域网例外另行保留。
  - RULE-SET,domestic-direct,DIRECT
  - MATCH,Proxy
```

`Proxy` 必须替换为客户端实际存在的代理组名称。若仍保留 ChinaMax 或 GEOIP,CN,DIRECT 等宽泛规则，本白名单不能阻止它们继续直连。尚未在实际手机或电脑导入验收。

## 增加国内服务

1. 在 GitHub 的 main 分支编辑 `rules/domestic-direct.yaml`。
2. 精确主机写 `  - DOMAIN,www.example.com`；确认整个域名体系可直连时写 `  - DOMAIN-SUFFIX,example.com`。不要填 URL、路径、IP 或通配符。
3. 在 `docs/audit.md` 补充归属、用途和依据，再提交。
4. 查看 Actions：校验成功后自动更新 release 分支；失败不更新正式订阅。
5. 客户端在成功定时更新（示例为一小时）或手动更新规则集后使用新版。不是 GitHub 提交后立即推送；缓存和已建立的连接可能需要刷新/重连。

没有匹配的请求应由客户端 MATCH,Proxy 接管。网站慢不等于应直连；先确认实际请求域名、服务归属和当前命中规则。

## 收录边界

- 国内服务按产品和运营归属判断，不保证每个 IP 位于中国大陆，也不表示只有国内用户使用。
- `qq.com`、`163.com` 等按整域服务体系收录；同一后缀下的新子域也会匹配，需接受该范围。
- 不使用进程、关键词、IP、ASN、GEOIP、整个顶级域名作为直连条件。
- 不整包放行共享云、共享 CDN、CF、国外验证码、国外支付或 AI 服务。
- 不自动同步上游新增条目；主分支的新增内容需要人工审核。自动校验只检查结构和已知禁止范围，不能自动证明国内归属。
- 首版不是国内服务大全，也不保证所列 App 全部依赖均直连。遗漏的依赖继续代理。
- DNS 出站和代理断线后不直连必须在客户端/系统层另外配置，规则集不能提供此保证。

## 发布与回滚

main 是编辑分支；release 是已校验订阅分支。工作流以快进方式发布，不强推历史。
回滚时在 main 使用 `git revert <commit>` 并推送，校验后 release 自动跟进；不要手动移动 release 到未校验版本。
可用 `git show <commit>:rules/domestic-direct.yaml` 查看历史内容。正式地址会随审核发布更新。

## 验证

Python 3.12+，无需第三方包：

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
```

来源和筛选记录见 [docs/audit.md](docs/audit.md)。本项目不承诺账号“防封”。
