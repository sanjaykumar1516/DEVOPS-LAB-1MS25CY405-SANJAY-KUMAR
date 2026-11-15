

pipeline {
    agent any

    environment {
        VENV = 'ci-venv'
        PYTHONPATH = "${WORKSPACE}/src"
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code checked out successfully.'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv ${VENV}

                    ${VENV}/bin/python -m pip install --upgrade pip

                    ${VENV}/bin/python -m pip install -r requirements.txt pytest httpx build
                '''
            }
        }

        stage('Automated Tests') {
            steps {
                sh '''
                    export PYTHONPATH="${WORKSPACE}/src"

                    ${VENV}/bin/python -m pytest tests/ -v
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    ${VENV}/bin/python -m build
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
            echo 'SUCCESS: Tests passed, build completed and artifacts archived.'
        }

        failure {
            echo 'FAILURE: Check Console Output for errors.'
        }

        always {
            echo 'Jenkins Pipeline execution finished.'
        }
    }
}
