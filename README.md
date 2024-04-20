# Citizen Security - Proyecto de Django REST con Autenticación Token Bearer

Este es un proyecto de Django REST Framework diseñado para aplicaciones web que requieren autenticación basada en tokens Bearer. Proporciona una solución simple y segura para la autenticación de usuarios y protege las vistas de la API mediante la verificación de la validez de los tokens Bearer.

## Características
- **Autenticación por Token Bearer**: Verifica la autenticidad de los tokens Bearer proporcionados por los clientes.
- **Protección de Vistas de API**: Restringe el acceso a vistas específicas de la API a usuarios autenticados.
- **Fácil Integración**: Se integra sin problemas en proyectos Django REST existentes.
- **Personalizable**: Permite la configuración de opciones como el tiempo de expiración del token y el algoritmo de cifrado.
- **Autenticación de Dos Factores (2FA)**: Proporciona una capa adicional de seguridad al requerir un segundo factor de autenticación, como un código generado en tiempo real o enviado a través de email.
- **Traducción**: Facilita la accesibilidad a usuarios de diferentes idiomas mediante la traducción de textos en la aplicación.
- **Manejo de Sesiones**: Permite almacenar información del usuario de manera segura entre solicitudes HTTP, cumpliendo con los requisitos de privacidad y seguridad.
- **Autenticación con Google**: Permite a los usuarios autenticarse en la aplicación utilizando sus cuentas de Google.
- **Registro con Confirmación de Correo a través de Código OTP**: Facilita el registro de nuevos usuarios mediante la generación de un código OTP enviado por correo electrónico para confirmar la dirección de correo electrónico proporcionada.

## Clonación del Proyecto
Puedes clonar este proyecto desde GitHub utilizando el siguiente enlace:

`git clone https://github.com/Darius20M/citizensecurity.git`

## Configuración
1. **Crea un entorno virtual con Python 3.9:**

   Antes de instalar las dependencias, crea un entorno virtual para este proyecto. Puedes hacerlo utilizando `venv`, así:

   ```bash
   python3.9 -m venv myenv
  
   
  Esto creará un nuevo directorio llamado myenv que contendrá el entorno virtual.

  Activa el entorno virtual:Luego, activa el entorno virtual. En sistemas Linux o macOS, puedes hacerlo con el siguiente comando:
  
  `source myenv/bin/activate`
  
  En Windows, el comando es ligeramente diferente:

  `myenv\Scripts\activate`
  
  Una vez activado el entorno virtual, verás (myenv) en tu terminal, lo que indica que estás trabajando dentro del entorno virtual.
  Instala las dependencias:Navega hasta el directorio del proyecto y asegúrate de tener el entorno virtual activado. Luego, ejecuta el siguiente comando para instalar las dependencias:

  `pip install -r requirements.txt`


## Uso
Una vez que hayas configurado el proyecto, puedes ejecutarlo utilizando el servidor de desarrollo de Django:

python manage.py runserver


Visita `http://localhost:8000/` en tu navegador para acceder a la aplicación.

## Contribución

¡Las contribuciones son bienvenidas! Si tienes sugerencias, problemas o deseas mejorar el proyecto, aquí hay algunas pautas para contribuir:

### Creación de Issues
- Si encuentras un problema en el proyecto o tienes una sugerencia de mejora, por favor crea un issue en este repositorio.
- Asegúrate de describir claramente el problema o la sugerencia, incluyendo pasos para reproducirlo si es un problema.

### Envío de Pull Requests
- Si deseas contribuir con código al proyecto, puedes enviar una pull request desde tu propio fork.
- Antes de enviar una pull request, asegúrate de que tu código cumpla con los estándares de codificación del proyecto y de que esté probado.
- Describe claramente los cambios que estás proponiendo en la pull request.
- Asegúrate de que tu pull request esté dirigida a la rama adecuada del repositorio.

¡Gracias por contribuir al proyecto!

