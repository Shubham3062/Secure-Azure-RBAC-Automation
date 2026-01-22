variable "subscription_id" {
  type        = string
  description = "Azure subscription ID"
  default     = ""
}

variable "tenant_id" {
  type        = string
  description = "Azure tenant ID"
  default     = ""
}

variable "group_object_id" {
  type        = string
  description = "Azure AD Group object ID to assign role to"
}

variable "role_key" {
  type        = string
  description = "Role key from role catalog"
}

variable "scope_id" {
  type        = string
  description = "Azure scope (resource group or subscription ID)"
}

variable "role_definition_name" {
  type        = string
  description = "Role name from role catalog"
}

variable "expires_at" {
  type        = string
  description = "Optional expiry timestamp for role assignment"
  default     = null
}
