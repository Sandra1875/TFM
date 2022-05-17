from datetime import datetime
import hashlib

class DetalleDTO:

    def __init__(self, id, estado, direccion, atributos, caracteristicas, url_first_page, id1):
        self.id = str(id)
        self.id1 = str(id1)
        self.estado= str(estado)
        self.direccion =str(direccion)
        self.atributos = str(atributos)
        self.caracteristicas = str(caracteristicas)
        self.url_first_page = str(url_first_page)
        self.date = str(datetime.now())
        self.construct_id_and_clean()

    def construct_id_and_clean(self):
        hashed_url = self.get_hash_from_url_first()
        self._id = hashed_url+ "---" + str(self.estado)+"---" + str(self.direccion)
        #print("_id: "+str(self._id))
        #print("id: "+str(self.id))
        #print("estado: "+str(self.estado))

    def get_hash_from_url_first(self):
        hash_object = hashlib.sha1(self.url_first_page.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig