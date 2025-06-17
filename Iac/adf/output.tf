output "data_factory_name" {
  description = "Nome do Azure Data Factory criado"
  value       = azurerm_data_factory.adf.name
}

output "data_factory_id" {
  description = "ID do Azure Data Factory"
  value       = azurerm_data_factory.adf.id
}
