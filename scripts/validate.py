"""Validate an intentionally restricted classical YAML rule list; stdlib only."""
import ipaddress
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BLOCKED = {
    'claude.ai', 'claude.com', 'anthropic.com', 'claudeusercontent.com',
    'claudemcpclient.com', 'claudemcpcontent.com', 'clau.de',
    'openai.com', 'chatgpt.com', 'oaistatic.com', 'oaiusercontent.com',
    'cloudflare.com', 'cloudflare.net', 'cloudflareinsights.com', 'workers.dev',
    'pages.dev', 'recaptcha.net', 'hcaptcha.com', 'arkoselabs.com',
    'stripe.com', 'stripe.network', 'stripecdn.com', 'auth0.com',
    'workos.com', 'workoscdn.com', 'google.com', 'gstatic.com',
    'googleapis.com', 'github.com', 'githubusercontent.com',
    'amazonaws.com', 'cloudfront.net', 'azurewebsites.net', 'akamaized.net',
    'akamaihd.net', 'aliyuncs.com', 'myqcloud.com', 'qcloud.com',
    'alicdn.com', 'doh.pub', 'alidns.com',
}
# Client profile AI-Only/Proxy domains (synced 2026-10-19). nameserver-policy binds this
# ruleset to domestic DNS regardless of rule order, so these must never appear here.
CLIENT_FORCED_PROXY = {
    'openaimerge.com', 'ai.com', 'sora.com', 'anthropic.com.cdn.cloudflare.net',
    'servd-anthropic-website.b-cdn.net', 'anthropic-com.ghost.io',
    'challenges.cloudflare.com', 'humb.apple.com', 'openaicom.imgix.net',
    'workos.imgix.net', 'statsig.com', 'statsigapi.net', 'featuregates.org',
    'featureassets.org', 'prodregistryv2.org', 'livekit.cloud', 'intercom.io',
    'intercomcdn.com', 'sendgrid.net', 'usefathom.com',
    'browser-intake-us5-datadoghq.com', 'siftscience.com', 'sift.com',
    'ghproxy.com', 'githubassets.com', 'npmjs.org', 'npmjs.com', 'pypi.org',
    'pythonhosted.org', 'okex.com', 'oklink.com', 'okx.com',
    'self.events.data.microsoft.com', 'mp.microsoft.com',
    'storeedge.microsoft.com', 'graph.microsoft.com', 'edge.microsoft.com',
    'www.microsoft.com', 'dns.google', 'cloudflare-dns.com', 'dns.quad9.net',
}
# Cloudflare / Claude / OpenAI / Google: never direct, never domestic DNS. Keywords
# catch new names; this set covers their domains that lack those keywords.
NEVER_DIRECT = {
    # Cloudflare
    'cf-ipfs.com', 'argotunnel.com', 'cfargotunnel.com', 'one.one.one.one',
    'cfl.re', 'r2.dev',
    # OpenAI
    'chat.com',
    # Google
    'ggpht.com', 'ytimg.com', 'youtu.be', 'gvt1.com', 'gvt2.com', 'gvt3.com',
    '1e100.net', 'appspot.com', 'firebaseio.com', 'firebaseapp.com', 'web.app',
    'doubleclick.net', 'gmail.com', 'android.com', 'chrome.com', 'chromium.org',
    'g.co', 'goo.gl', 'g.page', 'blogspot.com', 'blogger.com', 'admob.com',
    'gstatic.cn', 'gkecnapps.cn',
}
BLOCKED |= CLIENT_FORCED_PROXY | NEVER_DIRECT
# Client DOMAIN-KEYWORD,*,Proxy rules plus never-direct brands: reject any domain
# containing these.
BLOCKED_KEYWORDS = (
    'datadog', 'sentry', 'linkedin',
    'cloudflare', 'claude', 'anthropic', 'openai', 'chatgpt', 'google', 'youtube',
)
PUBLIC_SUFFIXES = {'com.cn', 'net.cn', 'org.cn', 'gov.cn', 'edu.cn', 'co.uk', 'com.hk'}


def overlaps(a, b):
    return a == b or a.endswith('.' + b) or b.endswith('.' + a)


def validate(text):
    if '\ufffd' in text or '\x00' in text:
        raise ValueError('Invalid text encoding')
    records = []
    header = False
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line == 'payload:' and not header and not records:
            header = True
            continue
        match = re.fullmatch(r'  - (DOMAIN|DOMAIN-SUFFIX),([a-z0-9.-]+)', raw)
        if not header or not match:
            raise ValueError(f'Line {number}: only DOMAIN / DOMAIN-SUFFIX entries allowed')
        kind, domain = match.groups()
        labels = domain.split('.')
        if len(labels) < 2 or domain in PUBLIC_SUFFIXES or len(domain) > 253:
            raise ValueError(f'Line {number}: overly broad or invalid domain {domain}')
        if any(not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', label) for label in labels):
            raise ValueError(f'Line {number}: invalid domain {domain}')
        try:
            ipaddress.ip_address(domain)
        except ValueError:
            pass
        else:
            raise ValueError(f'Line {number}: IP literals forbidden')
        if any(overlaps(domain, blocked) for blocked in BLOCKED):
            raise ValueError(f'Line {number}: protected/shared domain {domain}')
        if any(keyword in domain for keyword in BLOCKED_KEYWORDS):
            raise ValueError(f'Line {number}: protected keyword in {domain}')
        record = (kind, domain)
        if record in records:
            raise ValueError(f'Line {number}: duplicate {domain}')
        records.append(record)
    if not records:
        raise ValueError('Empty ruleset')
    for kind, domain in records:
        for parent_kind, parent in records:
            if parent_kind == 'DOMAIN-SUFFIX' and (kind, domain) != (parent_kind, parent):
                if domain == parent or domain.endswith('.' + parent):
                    raise ValueError(f'Redundant rule: {domain} already covered by {parent}')
    return records


if __name__ == '__main__':
    rules = validate((ROOT / 'rules/domestic-direct.yaml').read_text(encoding='utf-8'))
    print(f'PASS: {len(rules)} domain rules; no broad selectors or known protected domains')
