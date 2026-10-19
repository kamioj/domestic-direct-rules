import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('validator', Path(__file__).resolve().parents[1] / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class RuleValidationTests(unittest.TestCase):
    def test_valid_owned_service(self):
        self.assertEqual(len(validator.validate('payload:\n  - DOMAIN-SUFFIX,qq.com\n')), 1)

    def test_reject_broad_and_sensitive_rules(self):
        for rule in ['DOMAIN-SUFFIX,cn', 'DOMAIN-SUFFIX,com.cn',
                     'DOMAIN-KEYWORD,stripe', 'PROCESS-NAME,Thunder.exe',
                     'IP-CIDR,17.0.0.0/8', 'MATCH,DIRECT',
                     'DOMAIN,challenges.cloudflare.com', 'DOMAIN-SUFFIX,claude.ai',
                     'DOMAIN-SUFFIX,aliyuncs.com', 'DOMAIN,223.5.5.5']:
            with self.subTest(rule=rule), self.assertRaises(ValueError):
                validator.validate('payload:\n  - ' + rule + '\n')

    def test_reject_bad_yaml_and_duplicates(self):
        for text in ['payload: []', 'payload:\n  - DOMAIN,qq.com\n  - DOMAIN,qq.com',
                     'payload:\n  - DOMAIN-SUFFIX,qq.com\n  - DOMAIN,mail.qq.com',
                     'payload:\n  - DOMAIN,x..com', 'payload:\nsecret: abc']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                validator.validate(text)


if __name__ == '__main__':
    unittest.main()
