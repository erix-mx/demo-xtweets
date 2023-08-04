# Xtweets API

Pequeña API para la creación de Post, va orientado al curso de [iOS de Platzi](https://platzi.com/cursos/apps-ios/), ya que la API original no se encuentra disponible, el código lo puedes encontrar [aquí](https://github.com/erix-mx/platzi-xtweets).

### API URL

```kotlin
[**https://xtweets-api-dev.webfamous.mx/**](https://xtweets-api-dev.webfamous.mx/)
```

### Register [POST]

```kotlin
https://xtweets-api-dev.webfamous.mx/v1/register/
```

Enviamos información por Body:

```
{
    "username": "Demo",
    "email": "demo@email.com",
    "password":"passwordDemo"    
}
```

Por cada registro tenemos como respuesta:

```json
{
    "user": {
        "username": "Demo",
        "email": "demo@email.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxMTg3ODI1LCJpYXQiOjE2OTExODc1MjUsImp0aSI6IjMwMTIzMjVhNGIwYjQ0ODQ4YjA5ODQ4Njg2ZDY2MTY5IiwidXNlcl9pZCI6Mn0.8_dWOyT3qGF0DIoVBs6wIlqnCXbEprRFcy-u2ds5onA"
}
```

Posibles respuestas de error [Status code 400]: 

```kotlin
//Cuando el usuario ya existe
{
    "username": [
        "A user with that username already exists."
    ]
}

//Faltan credenciales
{
    "error": "Missing credentials in JSON data"
}
```

### Consulta de Post [GET]

Se obtienes los post desde la ruta: 

```kotlin
https://xtweets-api-dev.webfamous.mx/v1/post/?page=1
```

Recuerda incluir el token para obtener el listado, si no se envían los accesos tenemos un error como el siguiente:

```kotlin
{
    "detail": "Authentication credentials were not provided."
}
```

Cuando enviamos el token correctamente obtenemos:

```kotlin
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "content": "Mi second post",
            "location": null,
            "imageUri": null,
            "videoUri": null,
            "author": {
                "username": "Erix",
                "email": "eric@webfamous.mx",
                "first_name": ""
            },
            "uuid": "4195f0d2-7a60-4af7-986b-e38eb3d829f2",
            "created": "2023-08-04T22:24:50.686768Z",
            "updated": "2023-08-04T22:24:50.686790Z"
        },
        {
            "content": "Mi first post",
            "location": null,
            "imageUri": null,
            "videoUri": null,
            "author": {
                "username": "Erix",
                "email": "eric@webfamous.mx",
                "first_name": ""
            },
            "uuid": "7bb27f3b-4173-44af-a14c-4d45606118e6",
            "created": "2023-08-04T22:24:33.085583Z",
            "updated": "2023-08-04T22:24:33.085603Z"
        }
    ]
}
```

A diferencia de la API original, se agrega paginado para hacerlo mas parecido a casos reales.

### Crear Registro [POST]

Para crear un registro es necesario el campo “**content**”, los campos opcionales son “**location**”, “**imageUri**” y “**videoUri**”.

```kotlin
https://xtweets-api-dev.webfamous.mx/v1/post/
```

Información en body:

```kotlin
//Case simple post
{
    "content": "Mi second post"
}

//Case with image
{
    "content": "Hola mundo!",
    "imageUri": "https://images.unsplash.com/photo-1542596594-649edbc13630?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80,"
}

//Case with location
{
    "content": "Hola mundo!",
    "imageUri": "https://images.unsplash.com/photo-1542596594-649edbc13630?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80,",
    "location": {
        "latitude": "0.000",
        "longitude": "0.000"
    }
}

```

Respuesta de registro:

```kotlin
//Simple post with image
{
    "content": "Hola mundo!",
    "location": null,
    "imageUri": "https://images.unsplash.com/photo-1542596594-649edbc13630?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80,",
    "videoUri": null,
    "author": {
        "username": "Demo",
        "email": "demo@demo.mx"
    },
    "uuid": "5d19afae-16fb-4733-baaa-9cd0238d0c0f",
    "created": "2023-08-04T22:32:40.802960Z",
    "updated": "2023-08-04T22:32:40.802983Z"
}

//Post with location
{
    "content": "Hola mundo!",
    "location": {
        "latitude": "0.000000",
        "longitude": "0.000000"
    },
    "imageUri": "https://images.unsplash.com/photo-1542596594-649edbc13630?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=987&q=80,",
    "videoUri": null,
    "author": {
        "username": "Erix",
        "email": "eric@webfamous.mx",
        "first_name": ""
    },
    "uuid": "a4524ccb-e30e-47e0-a5a1-67f44029383d",
    "created": "2023-08-04T22:34:52.889318Z",
    "updated": "2023-08-04T22:34:53.026451Z"
}
```

### Borrar Registros [DELETE]

Importante usando método delete podemos eliminar un elemento de nuestra autoría haciendo un request como el siguiente ejemplo:

```kotlin
//Format 
https://xtweets-api-dev.webfamous.mx/v1/post/{uuid}/

//Sample
https://xtweets-api-dev.webfamous.mx/v1/post/a4524ccb-e30e-47e0-a5a1-67f44029383d/
```

Espero les pueda ayudar para realizar su practica, cualquier duda o comentario quedo a sus ordenes [Twitter](https://twitter.com/erixeer), [Linkedin](https://www.linkedin.com/feed/).

Si gustan agregar cosas, seria increíble. 🔥

Mucho éxito, saludos cordiales. ☺️