
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        VENV = 'ci-venv'
    }

    // Check GitHub for changes approximately every 2 minutes
    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {

        // Stage 1: Download source code from GitHub
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Source code downloaded successfully.'
            }
        }

        // Stage 2: Create Python environment and install dependencies
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv ${VENV}

                    ${VENV}/bin/python -m pip install --upgrade pip

                    ${VENV}/bin/python -m pip install \
                        -r requirements.txt \
                        pytest \
                        httpx \
                        build \
                        setuptools \
                        wheel
                '''
            }
        }

        // Stage 3: Run automated tests
        stage('Automated Tests') {
            steps {
                sh '''
                    export PYTHONPATH="${WORKSPACE}/src"

                    ${VENV}/bin/python -m pytest tests/ -v
                '''
            }
        }

        // Stage 4: Build Python wheel and source distribution
        stage('Build') {
            steps {
                sh '''
                    rm -rf dist
                    mkdir -p dist

                    ${VENV}/bin/python -m build --no-isolation

                    echo "Build files created successfully:"
                    ls -lh dist/
                '''
            }
        }

        // Stage 5: Archive generated artifacts in Jenkins
        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'dist/*',
                                 fingerprint: true

                echo 'Python build artifacts archived successfully.'
            }
        }
    }

    // Display final pipeline status
    post {
        success {
            echo 'SUCCESS: Tests passed, build completed and artifacts archived.'
        }

        failure {
            echo 'FAILURE: Check Jenkins Console Output for errors.'
        }

        always {
            echo 'Jenkins Pipeline execution finished.'
        }
    }
}

