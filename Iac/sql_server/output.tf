output "sqlserver_001" {
  description = "Nome do SQL Server"
  value       = azurerm_mssql_server.sql.name
}

output "database_001" {
  description = "Nome do Banco de Dados"
  value       = azurerm_mssql_database.sql.name
}

output "username" {
  description = "Usuário SQL Server"
  value       = var.usuario_admin
}

output "password" {
  description = "Senha SQL Server"
  value       = var.password
}

output "public_ip" {
  description = "Meu IP Público"
  value       = data.ipify_ip.public.ip_cidr
}
