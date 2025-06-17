variable "resource_group_name" {
  description = "Nome do Resource Group onde o Data Factory será criado"
  type        = string
}

variable "location" {
  description = "Região da Azure onde o Data Factory será provisionado"
  type        = string
  default     = "westus"
}

variable "data_factory_name" {
  description = "Nome do Azure Data Factory"
  type        = string
}

variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}
