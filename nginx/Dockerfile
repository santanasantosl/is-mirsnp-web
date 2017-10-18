FROM nginx:stable
MAINTAINER Lucas Santana-Santos "lusasantos@gmail.com"

# Copy a configuration file from the current directory
ADD nginx.conf /etc/nginx/

# Copy standard uwsgi_params to etc directory
ADD uwsgi_params /etc/nginx/

# Define working directory.
WORKDIR /etc/nginx

# Expose ports.
EXPOSE 443

