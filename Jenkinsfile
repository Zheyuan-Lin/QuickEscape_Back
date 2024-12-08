pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh './mvnw clean package'
            }
        }
        stage('Test') {
            steps {
                sh './mvnw test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'scp target/QuickEscapes-0.0.1-SNAPSHOT.jar root@155.138.237.5:~
                sh 'ssh root@155.138.237.5 "java -jar QuickEscapes-0.0.1-SNAPSHOT.jar"'
            }
        }
    }
}
