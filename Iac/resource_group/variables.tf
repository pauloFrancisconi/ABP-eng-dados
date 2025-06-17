variable "resource_group_name" {
  description = "Nome do Resource Group"
  type        = string
}

variable "location" {
  description = "Localização do Resource Group"
  type        = string
  default     = "westus"
}
