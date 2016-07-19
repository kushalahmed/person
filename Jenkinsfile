node {

    stage "git checkout"
    checkout scm

    stage "build"
    def myImage = docker.build "person:${env.BUILD_TAG}"

    stage "push"
    docker.withRegistry(env.DOCKER_REGISTRY, 'docker-registry-login') {
        // myImage.push()
        myImage.push 'latest'
    }
}