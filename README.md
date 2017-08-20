# Docker-Service-Manager
A tool to manage &amp; monitor containerized web applications

# Quickstart
1. Pull the docker-service-manager image from DockerHub,

`docker pull thejanw/docker-service-manager`

2. Pull the automated reverse proxy image from DockerHub,

`docker pull jwilder/nginx-proxy:0.6.0`

3. Run Docker Service Manager,

`docker run -d -p 8765:8765 -v /var/run/docker.sock:/var/run/docker.sock:ro thejanw/docker-service-manager`

4. Head to http://localhost:8765/ and you will see the DSM dashboard,

![alt text](https://raw.githubusercontent.com/ThejanW/Docker-Service-Manager/master/imgs/dsm_services_summary.png)

5. It's time to play!! Pull the images specified in the dsm-config.json by heading to the relevant tab in the 
SERVICES pane and witness their pulling progress in real time. 

![alt text](https://raw.githubusercontent.com/ThejanW/Docker-Service-Manager/master/imgs/dsm_pulling_logs.png)

6. Once pulled, you'll be able to start/stop the services as you wish.

7. Head to the services summary page and see the running services, 
if a particular service is running you can issue cURL commands or create your own client to utilize those services.
Some example cURL commands would look like,

    `curl -H 'Host: recognition-image.tika.dl' 'http://localhost:8765'`
    
    `curl -H 'Host: recognition-image.tika.dl' 'http://localhost:8765/inception/v4/ping'`
    
    `curl -H 'Host: recognition-image.tika.dl' 'http://localhost:8765/inception/v4/classify?topk=2&url=https://upload.wikimedia.org/wikipedia/commons/f/f6/Working_Dogs%2C_Handlers_Share_Special_Bond_DVIDS124942.jpg'`
    
    `curl -H 'Host: caption-image.tika.dl' 'http://localhost:8765'`
    
    `curl -H 'Host: caption-image.tika.dl' 'http://localhost:8765/inception/v3/ping'`
    
    `curl -H 'Host: caption-image.tika.dl' 'http://localhost:8765/inception/v3/captions?beam_size=3&max_caption_length=15&url=https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Marcus_Thames_Tigers_2007.jpg/1200px-Marcus_Thames_Tigers_2007.jpg'`

# TODO

1. Include CPU usage, usage statistics graphs for services.

2. Allow changing the dsm-config.json file through a web form.
