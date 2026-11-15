
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv ci-venv
                    . ci-venv/bin/activate

                    python -m pip install --upgrade pip

                    python -m pip install \
                        -i https://mirrors.aliyun.com/pypi/simple/ \
                        -r requirements.txt

                    python -m pip install \
                        -i https://mirrors.aliyun.com/pypi/simple/ \
                        pytest httpx build
                '''
            }
        }

        stage('Automated Tests') {
            steps {
                sh '''
                    . ci-venv/bin/activate
                    python -m pytest -v
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    . ci-venv/bin/activate
                    python -m build
                '''
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'dist/*',
                                 fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Jenkins CI Pipeline completed!'
        }

        failure {
            echo 'FAILURE: Check Console Output for errors.'
        }

        always {
            echo 'Jenkins Pipeline execution finished.'
        }
    }
}
