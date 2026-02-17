provider "aws" {
  region = "us-east-2"
}

resource "random_id" "id" {
  byte_length = 4
}

resource "aws_cognito_user_pool" "financial_agent_pool" {
  name = "amazon-financial-agent-pool"

  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  username_attributes      = ["email"]
  auto_verified_attributes = ["email"]
}

resource "aws_cognito_user_pool_domain" "main" {
  domain       = "amazon-financial-agent-${random_id.id.hex}"
  user_pool_id = aws_cognito_user_pool.financial_agent_pool.id
}

resource "aws_cognito_user_pool_client" "agent_client" {
  name         = "financial-agent-client"
  user_pool_id = aws_cognito_user_pool.financial_agent_pool.id

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH"
  ]

  # CAMBIO CLAVE: Activamos el secreto para que coincida con tu código Python
  generate_secret = true 
}

# --- OUTPUTS PARA TU ARCHIVO .ENV ---
output "user_pool_id" {
  value = aws_cognito_user_pool.financial_agent_pool.id
}

output "client_id" {
  value = aws_cognito_user_pool_client.agent_client.id
}

output "client_secret" {
  value     = aws_cognito_user_pool_client.agent_client.client_secret
  sensitive = true
}