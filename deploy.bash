sudo docker build -t image-api . 
sudo docker stop image
sudo docker rm image
sudo docker run -d -p 5000:5000 -it --name image image-api

