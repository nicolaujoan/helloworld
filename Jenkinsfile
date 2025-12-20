pipeline {
    agent any

    stages {
        stage('Get Code') {
            steps {
                // Traer todo el código fuente del repositorio
                git 'https://github.com/anieto-unir/helloworld.git'

                // Verificar que el código se ha descargado
                sh 'ls -la'

                // Verificar cuál es el espacio de trabajo
                sh 'echo "Workspace: ${WORKSPACE}"'
            }
        }

        stage('Build') {
            steps {
                echo 'Eyyy, esto es Python. No hay que compilar nada!!!'
            }
        }
    }
}
