"""Keep the KV handoff non-destructive and prevent credential state ownership."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AppRoleHandoffTests(unittest.TestCase):
    def test_all_legacy_instances_are_forgotten_without_destroy(self):
        source = (ROOT / 'approle_secrets.tf').read_text()
        self.assertRegex(source, r'removed\s*\{\s*from\s*=\s*vault_kv_secret_v2\.approle_credentials\s+lifecycle\s*\{\s*destroy\s*=\s*false')

    def test_no_credential_resource_or_data_source_remains(self):
        source = '\n'.join(path.read_text() for path in ROOT.glob('*.tf'))
        self.assertFalse(re.search(r'(?:resource|data)\s+"vault_kv_secret_v2"\s+"approle_credentials"', source))
        self.assertNotIn('vault_approle_auth_backend_role_secret_id', source)
        self.assertIn('resource "vault_approle_auth_backend_role" "cluster"', source)
