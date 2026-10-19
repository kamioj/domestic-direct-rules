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
