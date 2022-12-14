<div align="center">
 

  <h3 align="center">MyFlashCards</h3>  <p align="center">
    Aplicación web de Flashcards    
  </p>

 </div>
 
 <details>
  <summary>Tabla de contenido</summary>
  <ol>
    <li>
      <a href="#sobre-el-proyecto">Sobre el proyecto</a>
      <ul>
         <li><a href="#herramientas">Herramientas</a></li>
      </ul>
    </li>
    
   <li>
      <a href="#instrucciones">Instrucciones</a>
      <ul>
        <li><a href="#instalación">Instalación</a></li>
       <li><a href="#aplicación-desplegada">Aplicación desplegada</a></li>
      </ul>
    </li>
    
   <li>
    <a href="#contacto">Contacto</a>
   </li>
    
  </ol>
</details>


## Sobre el proyecto

Aplicación web de flashcards construida con el Framework Flask y  SQLAlchemy para el backend y Bootstrap para el frontend. La aplicación permite el registro y login de usuarios los cuales pueden crear, editar y eliminar tanto tarjetas como mazos los cuales pueden decidir si hacerlos públicos para que otros usuarios puedan verlos y adquirirlos o mantenerlos en privado. La aplicación también permite crear tarjetas buscando palabras en https://dictionary.cambridge.org mediante web scraping tanto de inglés a español como de español a inglés. 
Para facilitar el proceso de memorización la aplicación se basa en técnicas de repaso espaciado que tienen en cuenta el funcionamiento de la memoria, en concreto el sistema Leitner. Cada tarjeta tiene asignado un grado de dificultad que va del 1 al 5 según la facilidad con la que el usuario recuerda la respuesta. Al momento de estudiar un mazo la aplicación muestra en orden las tarjetas en base a su grado de dificultad lo que permite repasar primero las más difíciles.

<p align="right">(<a href="#readme">back to top</a>)</p>


### Herramientas


* ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
* ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

<p align="right">(<a href="#readme">back to top</a>)</p>

## Instrucciones





### Instalación
Para funcionar la aplicación requiere estar conectada a una base de datos SQL por ejemplo MySQL o PostgreSQL. Para conectar a la base de datos se debe establecer el url de la base de datos en el archivo config.py. Por ejemplo


   ```sh
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/flashcards"
   ```
Que corresponde a una base de datos MySQL local de nombre flashcards con nombre de usuario root y contraseña root en el puerto 3306. Una vez conectada ala base de datos la aplicación creara las tablas necesarias usando SQLAlchemy.

Con la base de datos conectada escribir en consola dentro de un espacio virtual de preferencia

   ```sh
   pip install -r requirements.txt
   set FLASK_APP=app.py
   flask run
   ```
   
### Aplicación desplegada

La aplicación está disponible en  [https://uane-flashcards-production.up.railway.app/](https://uane-flashcards-production.up.railway.app/). Tiene tres usuarios Osmar, Maria y Miguel todos con contraseña 123 con sus respectivos mazos públicos y privados.

<p align="right">(<a href="#readme">back to top</a>)</p>



## Contacto



Link del proyecto : [https://uane-flashcards-production.up.railway.app/](https://uane-flashcards-production.up.railway.app/)

Link del código del proyecto : [https://github.com/YOrHaS/UANE-flashcards](https://github.com/YOrHaS/UANE-flashcards)

<p align="right">(<a href="#readme">back to top</a>)</p>


[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
