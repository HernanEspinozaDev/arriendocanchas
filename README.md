# Arriendocanchas

Proyecto de arriendo de canchas.

## Tabla de Contenidos

- [Clonar el Proyecto](#clonar-el-proyecto)
- [Crear Entorno Virtual](#crear-entorno-virtual)
- [Activar el Entorno Virtual](#activar-el-entorno-virtual)
  - [Windows](#windows)
  - [macOS/Linux](#macoslinux)
- [Desactivar el Entorno Virtual](#desactivar-el-entorno-virtual)
- [Instalar las Librerías Necesarias](#instalar-las-librerías-necesarias)
- [Dirigirse al Proyecto](#dirigirse-al-proyecto)
- [Iniciar el Proyecto](#iniciar-el-proyecto)

## Clonar el Proyecto

Primero, clona el repositorio desde GitHub y navega al directorio del proyecto:

```bash
git clone https://github.com/HernanEspinozaDev/arriendocanchas.git
cd arriendocanchas

Crear Entorno Virtual
Crea un entorno virtual para gestionar las dependencias del proyecto. Puedes usar uno de los siguientes comandos:

python -m venv venv
o
python3 -m venv venv

Activar el Entorno Virtual

Windows
Activa el entorno virtual ejecutando:
venv\Scripts\activate

macOS/Linux
Activa el entorno virtual ejecutando:

source venv/bin/activate

Desactivar el Entorno Virtual
Para desactivar el entorno virtual, simplemente ejecuta:

deactivate

Instalar las Librerías Necesarias
Con el entorno virtual activado, instala las dependencias del proyecto usando:

pip install -r requirements.txt

Dirigirse al Proyecto
Navega al directorio principal del proyecto:

cd arriendo_canchas

Iniciar el Proyecto
Finalmente, inicia el proyecto ejecutando:

python main.py