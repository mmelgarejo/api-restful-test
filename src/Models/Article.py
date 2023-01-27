class Article:
    def __init__(self, fecha, enlace, enlace_foto, titulo, resumen, contenido_foto=None, content_type_foto=None):
        self.fecha = fecha
        self.enlace = enlace
        self.enlace_foto = enlace_foto
        self.titulo = titulo
        self.resumen = resumen
        self.contenido_foto = contenido_foto
        self.content_type_foto = content_type_foto