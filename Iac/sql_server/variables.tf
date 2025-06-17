variable "resource_group_name" {
  description = "Nome do Resource Group onde o SQL Server será criado"
  type        = string
}

variable "location" {
  description = "Região da Azure onde os recursos serão provisionados"
  type        = string
  default     = "westus"
}

variable "subscription_id" {
  description = "ID da Subscription da Azure"
  type        = string
}

variable "usuario_admin" {
  description = "Login do administrador do SQL Server"
  type        = string
}

variable "password" {
  description = "Senha do administrador do SQL Server"
  type        = string
  sensitive   = true
}
