## Docker build process

* build `docker build .`
* list `docker image ls`
* run with your image id `docker run -it 5aef9b0af70f /bin/bash repeat.sh 4 hello`

### Push to DockerHub

* Create docker account, then access token, then place token in GitHub Secrets as DOCKER_HUB
* docker login: `docker login -u <hub-user -p $DOCKER_HUB`
* build and tag locally: `docker build . -t <hub-user>/<repo-name>`
* docker push 
* Verify you can run it by pulling from Docker Hub:  https://hub.docker.com/r/noahgift/tiny-container-demo/tags
* docker run -it <hub-user>/<repo-name>:latest /bin/bash repeat.sh 4 hello

Example would be:
`docker run -it noahgift/tiny-container-demo:latest /bin/bash repeat.sh 4 hello`

### Run in Cloud9

* run locally:  `docker run -it noahgift/tiny-container-demo:latest /bin/bash repeat.sh 4 hello`
* retag and push:  
Example (replace with your info): `docker push 561744971673.dkr.ecr.us-east-1.amazonaws.com/awscli:tiny`
* verify it runs in a new cloud9 instance: `docker run -it 561744971673.dkr.ecr.us-east-1.amazonaws.com/awscli:tiny /bin/bash repeat.sh 4 hello`