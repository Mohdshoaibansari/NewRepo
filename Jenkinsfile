pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh "PATH=\"\${PATH}:/usr/local/bin\"; \
        python3 --version"
            }
        }

        stage('build') {
            steps {
                sh "PATH=\"\${PATH}:/usr/local/bin\"; \
        python3 test1.py"
            }
        }
    }
}
