
pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh "PATH=\"\${PATH}:/usr/local/bin\"; \
        python3 --version"
            }
        }


        stage('deploy') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'mohammad', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                                    sh "PATH=\"\${PATH}:/usr/local/bin\"; \
        python3 usercreate.py"
                    }

            }
        }
    }
}

