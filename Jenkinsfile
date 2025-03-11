pipeline {
    agent {
        docker {
            image 'python:3.9-slim'  # Use a Python Docker image
            args '-u root:root'       # Grant permissions (adjust as needed)
        }
    }
    stages {
        // Stage 1: Fetch code from GitHub
        stage('Checkout') {
            steps {
                git(
                    url: 'https://github.com/mm0177/mlops-mmtg123.git',
                    branch: 'main',
                    credentialsId: 'your-github-credentials-id'  # Setup in Jenkins
                )
            }
        }

        // Stage 2: Install Python dependencies
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        // Stage 3: Run data ingestion
        stage('Data Ingestion') {
            steps {
                sh 'python src/components/data_ingestion.py'
            }
        }

        // Stage 4: Run data transformation
        stage('Data Transformation') {
            steps {
                sh 'python src/components/data_transformation.py'
            }
        }

        // Stage 5: Train model
        stage('Model Training') {
            steps {
                sh 'python src/components/model_trainer.py'
            }
        }

        // (Optional) Stage 6: Tests
        stage('Run Tests') {
            steps {
                sh 'python -m pytest tests/'  # If you have tests
            }
        }
    }
    post {
        always {
            // Cleanup or notifications
            echo 'Pipeline completed'
        }
        failure {
            // Send failure alerts (e.g., email/Slack)
            echo 'Pipeline failed!'
        }
    }
}