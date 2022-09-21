## Docker build process

* build `docker build .`
* list `docker image ls`
* run with your image id `docker run -it 5aef9b0af70f /bin/bash repeat.sh 4 hello`

### Push to DockerHub

* Create docker account, then access token, then place token in GitHub Secrets as DOCKER_HUB
* docker login: `docker login -u <hub-user -p $DOCKER_HUB`
* build and tag locally: `docker build . -t <hub-user>/<repo-name>`
* docker push <hub-user>/<repo-name>
* Verify you can run it by pulling from Docker Hub:  https://hub.docker.com/r/noahgift/tiny-container-demo/tags
