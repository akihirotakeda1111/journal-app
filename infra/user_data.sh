#!/bin/bash
# install:Docker, Git
yum update -y
yum install -y docker git
systemctl start docker
systemctl enable docker
curl -SL https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
sudo usermod -aG docker ec2-user

# git clone
cd /home/ec2-user
git clone https://github.com/akihirotakeda1111/journal-app.git
sudo chown -R ec2-user:ec2-user journal-app
cd journal-app
echo "ALLOWED_HOSTS=api.journal-app.a-t-dev.com" >> .env
echo "CORS_ALLOWED_ORIGINS=https://journal-app.a-t-dev.com" >> .env

# output .env
echo "DB_HOST=${db_host}" >> .env
echo "DB_NAME=${db_name}" >> .env
echo "DB_USER=${db_user}" >> .env
echo "DB_PASSWORD=${db_password}" >> .env
echo "POSTGRES_DB=${db_name}" >> .env
echo "POSTGRES_USER=${db_user}" >> .env
echo "POSTGRES_PASSWORD=${db_password}" >> .env
echo "AWS_S3_UPLOAD_BUCKET=${s3_upload_bucket}" >> .env

# setup nginx
bash setup_nginx.sh