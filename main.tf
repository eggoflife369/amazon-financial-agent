provider "aws" {
  region = "us-east-2"
}

resource "random_id" "id" {
  byte_length = 4
}

# --- 1. COGNITO (IDENTIDAD FRONTEND) ---
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

  generate_secret = true 
}

# --- 2. INFRAESTRUCTURA DE DATOS E IA (BACKEND) ---
resource "aws_s3_bucket" "financial_reports" {
  bucket = "amazon-financial-reports-${random_id.id.hex}"
  tags = {
    Environment = "Production"
    Project     = "Amazon Financial Agent"
  }
}

resource "aws_iam_role" "agent_execution_role" {
  name = "amazon-financial-agent-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = ["ecs-tasks.amazonaws.com", "lambda.amazonaws.com"]
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bedrock_access" {
  role       = aws_iam_role.agent_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
}

# --- 3. OUTPUTS ---
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

output "s3_bucket_name" {
  value = aws_s3_bucket.financial_reports.bucket
}

output "agent_role_arn" {
  value = aws_iam_role.agent_execution_role.arn
}
