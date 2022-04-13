locals {
  tags = {
    Owner       = "mlops-tabular"
    Project     = "mlops-tabular"
    Environment = "${var.environment}"
    Toolkit     = "Terraform"
    Name        = "${var.prefix}"
  }
}