data "azurerm_role_definition" "selected_role" {
  name  = var.role_definition_name
  scope = var.scope_id
}

resource "azurerm_role_assignment" "rbac" {
  scope              = var.scope_id
  role_definition_id = data.azurerm_role_definition.selected_role.id
  principal_id       = var.group_object_id
}