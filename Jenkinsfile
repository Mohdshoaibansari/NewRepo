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
                sh "PATH=\"\${PATH}:/usr/local/bin\"; \
        python3 test.py"
            }
        }
    }
}
