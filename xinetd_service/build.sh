# build container and run
sudo docker build -t unicornfts -f Dockerfile .
sudo docker run --net=host unicornfts &