output "assigned_role" {
  value       = var.role_key
  description = "Role assigned to the group"
}

output "scope" {
  value       = var.scope_id
  description = "Scope where role is assigned"
}
