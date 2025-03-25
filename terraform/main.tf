provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "flask_sg" {
  name        = "flask-app-sg"
  description = "Allow HTTP and SSH access"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "flask_app" {
  ami             = "ami-0013d898808600c4a"  # Ubuntu 20.04 LTS
  instance_type   = var.instance_type
  key_name        = var.key_pair
  security_groups = [aws_security_group.flask_sg.name]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update -y
              sudo apt-get install -y python3 python3-pip git
              sudo pip3 install ansible
              git clone https://github.com/mm0177/mlops-mmtg123.git /home/ec2-user/ansible-playbooks
              ansible-playbook -i "localhost," -c local /home/ec2-user/ansible-playbooks/deploy_flask_app.yml
              EOF

  tags = {
    Name = "FlaskApp"
  }
}

