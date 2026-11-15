
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
                    pip install -r requirements.txt
                    pip install pytest httpx build
                '''
            }
        }

        stage('Automated Tests') {
            steps {
                sh '''
                    . ci-venv/bin/activate
                    PYTHONPATH=src pytest -v
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
}

