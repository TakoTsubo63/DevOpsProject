terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.13.5"
}

provider "aws" {
  profile = "default"
  region  = "us-west-2"
}

resource "aws_instance" "tomcatserver" {
  ami           = "ami-03d5c68bab01f3496"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.awssg.id]
  key_name = "key_pair_linux_main"

  tags = {
    Name = "TomCat_server"
  }
}

resource "aws_instance" "apacheserver" {
  ami           = "ami-03d5c68bab01f3496"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.awssg.id]
  key_name = "key_pair_linux_main"  

  tags = {
    Name = "Apache_server"
  }
}

resource "aws_instance" "sqlserver" {
  ami           = "ami-03d5c68bab01f3496"
  instance_type = "t2.micro"
  vpc_security_group_ids = [aws_security_group.awssg.id]
  key_name = "key_pair_linux_main"

  tags = {
    Name = "PostgreSQL_server"
  }
}


resource "aws_security_group" "awssg" {
  name        = "SecurityGroup"

  ingress {
      from_port        = 22
      to_port          = 22
      protocol         = "tcp"
      cidr_blocks      = ["0.0.0.0/0"]
    }
  
  ingress {
      from_port        = 80
      to_port          = 80
      protocol         = "tcp"
      cidr_blocks      = ["0.0.0.0/0"]
    }

 ingress {
      from_port        = 8080
      to_port          = 8080
      protocol         = "tcp"
      cidr_blocks      = ["0.0.0.0/0"]
    }

 ingress {
      from_port        = 5432
      to_port          = 5432
      protocol         = "tcp"
      cidr_blocks      = ["0.0.0.0/0"]
    }

  egress {
      from_port        = 0
      to_port          = 0
      protocol         = "-1"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }

  tags = {
    Name = "SecurityGroup"
  }
}

output "instance_public_ip_apache" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.apacheserver.public_ip
}
output "instance_public_ip_postgres" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.sqlserver.public_ip
}
output "instance_public_ip_jenkins" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.tomcatserver.public_ip
}
