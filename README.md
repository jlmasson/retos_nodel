# Retos Nodel - José Luis Massón

### Reto 1

Para el reto 1, se tiene el siguiente enlace:

https://docs.google.com/spreadsheets/d/18SIxsNHlXLXLPOrmYguEBa0Shz_7ufobEgID1LXrCXI/edit?usp=sharing

La hoja tiene el acceso público. Se modifica la data para las respectivas pruebas

Se debe eliminar el archivo token.pickle para tener tokens limpios, y se debe dar la autorización
a la aplicación Quickstart que se utilizó para este reto

Para correr el script que permite probar la solución se debe ir a la carpeta reto1

```shell
    cd reto1
    python 01_reto_pivote_table.py
```

Para cada ejecución, se crea una hoja nueva con los resultados esperados

### Reto 3

Para el reto 3, se tiene un chromedriver (Windows fue utilizado para esto), que se encuentra
en la carpeta bin de este repositorio.

Se debe ejecutar el siguiente script:


```shell
    cd reto3
    python main.py <user> <password> <link>
```

Donde:
    1. user: Es el correo de facebook
    2. password: Es la contraseña
    3. link: Es el enlace del post

Se debe considerar que el enlace debe ser enviado entre commillas como en el siguiente ejemplo
```shell
    cd reto3
    python main.py prueba@correo.com prueba "https://facebook.com/..."
```

Para cada ejecución, se crea una nueva hoja en el archivo.
