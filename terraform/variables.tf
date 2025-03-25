variable "aws_region" {
  description = "AWS region"
  default     = "ap-southeast-2"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "key_pair" {
  description = "new-keymmtg"
  default     = "new-keymmtg"
}