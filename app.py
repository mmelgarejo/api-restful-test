from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
import hashlib
import hmac
from flask_swagger_ui import get_swaggerui_blueprint
from src.Models.Article import Article
from src.helpers.helper import *
from src.database.database import get_connection

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API RESTFUL TEST"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

def api_required(func):
    def wrapper(*args, **kwargs):
        try:
            api_key = request.headers.get('api-key')
            if api_key is None or api_key == '':
                error = get_error('g268')
                return error, 400
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM api_key WHERE key = ?", (api_key,))
            data = cursor.fetchone()
            if data is None:
                error = get_error('g103')
                return error, 403
            return func(*args, **kwargs)
        except Exception as e:
            error = get_error('g100')
            error['error']+= str(e)
            return error, 500
    return wrapper

@app.route('/consulta')
#@api_required  # Descomentar si se quiere validar la API KEY
def get_data():
    try:
        api_key = request.headers.get('api-key')
        search = request.args.get('q')
        return_base_photo = request.args.get('f')
        if search is None or search == '':
            error = get_error('g268')
            return error, 400
        articles = get_articles(search, api_key)
        if len(articles) == 0:
            error = get_error('g267')
            error['error'] += search
            return error, 404
        list_articles = []
        for article in articles:
            article_object = get_article_data(article, return_base_photo)
            list_articles.append(article_object.__dict__)
        return jsonify(list_articles), 200
    except Exception as e:
        error = get_error('g100')
        error['error'] += str(e)
        return error, 500
    
def get_articles(search, api_key=None):
    try:
        url = "https://npy.com.py/?s=" + search
        if api_key:
            signing = hmac.new(api_key.encode('utf-8'), url.encode('utf-8'), hashlib.sha256).hexdigest()
        else:
            signing = ''
        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'application/xml,application/json,text/plain,text/html',
            'Connection': 'keep-alive',
            'X-API-KEY': signing
        }
        data = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(data.text, 'html.parser')
        articles = soup.find_all("article", class_="post")
        return articles
    except Exception as e:
        raise e
    
def get_article_data(article, return_base_photo):
    try:
        articule_details = article.find("div", class_="article-details")
        articule_photo = article.find("div", class_="entry-image")
        fecha = articule_details.find("time").get("datetime")
        enlace = articule_details.find("h2", class_="entry-title").a.get("href")
        titulo = articule_details.find("h2", class_="entry-title").a.get_text()
        enlace_foto = articule_photo.img.get("src")
        resumen = articule_details.find("div", class_="entry-summary").p.get_text()
        if  return_base_photo is not None and return_base_photo != '' and return_base_photo:
            contenido_foto = get_photo_base64(enlace_foto)
            content_type_foto = get_content_type(enlace_foto)
            article_object = Article(fecha, enlace, enlace_foto, titulo, resumen, contenido_foto, content_type_foto)
        else:
            article_object = Article(fecha, enlace, enlace_foto, titulo, resumen)
        return article_object
    except Exception as e:
        raise e

if __name__ == '__main__':
    app.run()