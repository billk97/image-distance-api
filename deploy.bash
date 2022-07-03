sudo docker build -t image-api . 
sudo docker stop image
sudo docker rm image
docker run -p 5000:5000 -it --name image-api image 
