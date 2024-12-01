# Use the base image php:apache
FROM php:apache

# Copy the web application files
COPY ./index.php /var/www/html/

# Set environment variable for API URL
ENV API_URL=http://api:5000/pozos/api/v1.0/get_student_ages

