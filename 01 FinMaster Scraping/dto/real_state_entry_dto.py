from datetime import datetime
import hashlib

class RealStateEntryDTO:

    def __init__(self, id, tipo, estVenta, lat, lng, tipoinv,  titulo, precio, ambientes, dormitorios, banios, superficie, url_scrapped,url_element,url_first_page):
        self.id = id
        self.tipo= tipo
        self.estVenta =estVenta
        self.lat = lat
        self.lng = lng
        self.tipoinv =tipoinv
        self.titulo = titulo
        self.prize = precio
        self.ambientes = ambientes
        self.dormitorios = dormitorios
        self.meters = superficie
        self.banios = banios
        self.url_scraped=url_scrapped
        self.url_element=url_element
        self.url_first_page=url_first_page
        self.date = str(datetime.now())

        self.construct_id_and_clean()

    def construct_id_and_clean(self):
        hashed_url = self.get_hash_from_url_first()
        if(self.titulo=="" or self.titulo==None):
            self._id = hashed_url + "---"+ str(self.meters)+"---" + str(self.dormitorios)+"---"+str(self.prize)
            self.titulo = hashed_url
        else:
            self._id = hashed_url + "---" + self.titulo + "---" + str(self.meters)+"---" + str(self.dormitorios)+"---"+str(self.prize)

    def get_hash_from_url_first(self):
        hash_object = hashlib.sha1(self.url_first_page.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig