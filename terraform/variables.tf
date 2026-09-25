variable "aws_region" {
  description = "The AWS region to deploy the infrastructure in."
  type        = string
  default     = "ap-south-1" # Changed default to Mumbai as requested
}

variable "cluster_name" {
  description = "The name of the EKS cluster."
  type        = string
  default     = "pixelcraft-ai-eks-cluster"
}
