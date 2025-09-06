# reimagining-celery-canvas

pip install -r requirements.txt 
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
docker stop rabbitmq
docker rm rabbitmq