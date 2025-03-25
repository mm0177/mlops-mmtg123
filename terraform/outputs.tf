output "public_ip" {
  value = aws_instance.flask_app.public_ip
}

output "app_url" {
  value = "http://${aws_instance.flask_app.public_ip}"
}