@echo off

:: Remove existing container
docker rm -f ecs152a-simulator

:: Build Docker image
docker build -t ecs152a/simulator .

:: Start container and expose port 5001
docker run --name ecs152a-simulator ^
    --cap-add=NET_ADMIN ^
    --rm ^
    -p 5001:5001/udp ^
    -v "%cd%\hdd:/hdd" ^
    ecs152a/simulator
