Command to build docker image:
docker build -t flask_customer_app_image .


to run image:
docker run -it -p 5000:5000 flask_customer_app_image
