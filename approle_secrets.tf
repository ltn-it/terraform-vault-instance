# AppRole Backend-Rollen
resource "vault_approle_auth_backend_role" "cluster" {
  for_each = var.bootstrap_phase >= 3 ? local.active.approles : {}

  backend            = vault_auth_backend.approle[each.value.backend].path
  role_name          = each.value.role_name
  namespace          = each.value.namespace
  token_ttl          = each.value.token_ttl
  token_max_ttl      = each.value.token_max_ttl
  token_policies     = each.value.token_policy
  token_type         = lookup(each.value, "token_type", "default")
  token_period       = each.value.token_period
  secret_id_ttl      = each.value.secret_id_ttl
  secret_id_num_uses = each.value.secret_id_num_uses
  depends_on = [
    vault_policy.policy,
    vault_mount.secret
  ]
}

# Ansible owns the complete KV v2 credential entry, including the Secret ID.
# Forget every legacy instance without deleting the live credentials.
removed {
  from = vault_kv_secret_v2.approle_credentials

  lifecycle {
    destroy = false
  }
}
