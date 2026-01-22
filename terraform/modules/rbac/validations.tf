locals {
  allowed_roles = ["vm-reader-dev", "storage-reader", "app-contributor"]
}

# Example safeguard
resource "null_resource" "validate_role_key" {
  count = contains(local.allowed_roles, var.role_key) ? 0 : 1

  provisioner "local-exec" {
    command = "echo 'Invalid role_key!' && exit 1"
  }
}
