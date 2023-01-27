from PIL import Image
import requests
from io import BytesIO
import base64

def get_photo_base64(url_photo):
    try:
        im = Image.open(requests.get(url_photo, stream=True).raw)
        buf = BytesIO()
        im.save(buf, format='JPEG')
        buf.seek(0)
        image_bytes = buf.read()
        buf.close()
        return base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        raise e
    
def get_content_type(url_photo):
    try:
        im = Image.open(requests.get(url_photo, stream=True).raw)
        return im.format
    except Exception as e:
        raise e
    
def get_error(code):
    try:
        errors = {
            'g100': {'codigo': 'g100', 'error': 'Error interno del servidor '},
            'g267': {'codigo': 'g267', 'error': 'No se encuentran noticias para el texto '},
            'g268': {'codigo': 'g268', 'error': 'Parámetros inválidos'},
            'g103': {'codigo': 'g103', 'error': 'No autorizado'},
        }
        return errors[code]
    except Exception as e:
        raise e
    
        