locals {
  tags = {
    Owner       = "mlops-tabular"
    Project     = "mlops-tabular"
    Environment = "dev"
    Toolkit     = "Terraform"
    Name        = "${var.prefix}"
  }
}