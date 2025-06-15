variable "resource_group_name" {
  description = "Nome do Resource Group onde o ADLS será criado"
  type        = string
}

variable "location" {
  description = "Região da Azure onde o ADLS será provisionado"
  type        = string
  default     = "westus"
}
