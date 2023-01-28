
# API RESTFUL TEST




## Realizado con

 - [Python 3](https://www.python.org/)
 - [Flask 2.2.2](https://flask.palletsprojects.com/en/2.2.x/)



## Deployment

Para ejecutar el proyecto se debe realizar lo siguiente:

Configurar entorno virtual

```bash
  python3 -m venv env
  
  Activar entorno virtual

  Windows: env\Scripts\activate

  Linux o Mac: source env/bin/activate
```

Instalar Requerimientos

```bash
  pip install -r requirements.txt
```
Ejecutar el archivo app:

```bash
  python app.py
```

## Llamar a la API

- http://localhost:5000/consulta?q=prueba&f=False

    - q (Text a Buscar). Requerido
    - f (Parametro que define si se debe retornar la imagen codificada en base64). Opcional


## API KEY

Para ejecutar el proyecto con el requerimiento de API KEY se debe descomentar la llamada a la función @api_key_required en el archivo app.py (linea 46) y pasar al request una de las siguientes keys:

`API_KEY` = c0a4b28f-c48d-4596-8639-f3f34cff1a8b

`ANOTHER_API_KEY` = b883dff0-daf2-4d48-89f8-88d344c928d8

## Swagger 

- http://localhost:5000/swagger
