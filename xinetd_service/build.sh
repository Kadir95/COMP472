# build container and run
sudo docker build -t unicornfts -f Dockerfile .
sudo docker run -p 8181:8181 unicornfts &