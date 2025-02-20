# Use Nginx as the base image
FROM nginx:alpine

# Set a directory to serve the web files
WORKDIR /usr/share/nginx/html

# Copy website files into Nginx's serving directory
COPY src /usr/share/nginx/html

# Replace placeholder in flag.html with the actual flag
RUN sed -i 's/FLAG_TEMPLATE_STRING/magpieCTF{k@yl1n3d_1s_w@nt3d}/g' /usr/share/nginx/html/mcdata/flag.html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 for the web server
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
