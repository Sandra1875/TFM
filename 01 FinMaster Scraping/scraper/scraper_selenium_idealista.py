from selenium import webdriver
import sys

from utils_app.util_summary_builder import UtilsSummaryBuilder
from dto.real_state_entry_dto import RealStateEntryDTO
from dto.summary_scrapped_dto import SummaryScrappedDTO

import time 
import random

#https://www.seleniumhq.org/download/
#14393
#https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

class ScraperSeleniumIdealista:

    def __init__(self, urls):
        self.urls = urls
        self.contador=0
        #self.driver = webdriver.Edge()
        self.driver = webdriver.Chrome(executable_path=r"F:\UIV\09 Fin Master\chromedriver_win32\chromedriver.exe")        
        #self.driver = webdriver.Firefox()
        self.data ={}
        self.summaries = {}
    
    def get_data(self):
        for url_from_db in self.urls:
            driver = self.driver
            driver.get(url_from_db) 
            #driver.set_window_position(-4000,0)

            self.get_data_from_page(driver,url_from_db) 
        driver.close()
       

    def get_data_from_page(self,driver,url_from_db):
        print("obtaining data from " + driver.current_url)
        random_int =573 + random.randint(-3, 3)
        driver.execute_script("window.scrollTo(0, "+str(random_int) +");")
        time.sleep(8.5 + random.uniform(0.5,0.9))
        body_containers = self.driver.find_element_by_id("body-content-wrapper")
        formas = body_containers.find_element_by_id("ssForm")
        paginas = formas.find_element_by_id("page")
        secciones = paginas.find_element_by_css_selector('div.section-dark')    
        contenidos = secciones.find_element_by_id("MainContent")
        listas = contenidos.find_element_by_css_selector("div.listinglist-container")
        lista_rows = listas.find_element_by_css_selector("div.listinglist-row")
        conts = lista_rows.find_element_by_css_selector("div.results-container-outer")
        r_rows = conts.find_element_by_css_selector("div.results-row")
        r_contas = r_rows.find_element_by_css_selector("div.results-container")        
        ll_contents = r_contas.find_element_by_id("ll-content-container")
        galerys = ll_contents.find_element_by_css_selector("div.gallery-container")
        rows = galerys.find_element_by_css_selector("div.row")
        gallery_items = rows.find_elements_by_css_selector("div.gallery-item-container")
        for item in gallery_items: 
            id_item = item.get_attribute("id")
            print("id_item : "+str(id_item))           
            #sourceHtml = item.get_attribute("innerHTML")
            self.parse_info_container_and_update_data(item, url_from_db, id_item)
        print("se obtuvo " + str(len(self.data[url_from_db])) + " entradas")
        self.contador+=1
        time.sleep(1 + random.uniform(0.5,1))
        sigPagina =self.is_next_page(ll_contents)
         
        if (sigPagina!=None and self.contador < 20):
            #url=driver.find_elements_by_class_name("icon-arrow-right-after")[0].get_attribute("href")
            driver.get(sigPagina+"&tt=261&cr=2&min=400000&sc=89&fts=Terreno&cur=USD&sb=PriceIncreasing&")
            self.get_data_from_page(driver,url_from_db)
        #else: 
        #    self.get_summary(driver,url_from_db)
            

    def is_next_page(self, contenedor):
        try:
            pagination=contenedor.find_element_by_css_selector("div.pagination")
            sourceHtml = pagination.get_attribute("innerHTML")
            #print("Row: "+ sourceHtml)
            nav= pagination.find_element_by_tag_name('nav')
            ul= nav.find_element_by_tag_name('ul')
            lis = ul.find_elements_by_tag_name('li')
            encontro= False
            for li in lis:
                if encontro ==True:
                    #print("  >> siguiente  ! !")
                    enlace = li.find_elements_by_tag_name('a')
                    sig= enlace[0].get_attribute("href")
                    #print("sig: " + str(sig))
                    break
                clase= li.get_attribute("class").strip()            
                if clase=="active":
                    encontro=True
                    #print("li activa ! !")
        except:
            return None
        return sig

    def parse_info_container_and_update_data(self,info_container_array,url_from_db, id_item ):
        if(self.data==None): self.data = {}
        if(not url_from_db in self.data.keys()): self.data[url_from_db]=[]

        list_gallery_items = info_container_array.find_elements_by_css_selector("div.gallery-item")
        for home in list_gallery_items:                                                                               
            Tipos=home.find_elements_by_class_name('card-trans-type')
            tipo=""
            for t in Tipos:
                tipo= t.text.strip()
            especial=home.find_element_by_class_name('gallery-attribute-position')
            estado= especial.find_elements_by_class_name('status-sold')
            estVenta=""
            for e in estado:
                estVenta= e.text.strip()                
            foto=home.find_element_by_css_selector('div.gallery-photo')
            listgalle=foto.find_element_by_css_selector('div.listgallery-controls-container')
            pull=listgalle.find_element_by_css_selector('div.pull-right')            
            mapas= pull.find_elements_by_class_name('map')
            lat=0
            lng=0
            for m in mapas:
                lat= m.get_attribute("data-lat")
                lng= m.get_attribute("data-lng")
            url_element=foto.find_element_by_tag_name('a').get_attribute("href").strip()
            gal_precio=home.find_element_by_css_selector('div.gallery-price')
            precio_main=gal_precio.find_element_by_css_selector('span.gallery-price-main')
            Precio=precio_main.find_element_by_css_selector('a.proplist_price')
            precio= str(Precio.text.replace("USD","").strip())
            tipo_bien=home.find_element_by_css_selector('div.gallery-transtype')
            tipoinv= str(tipo_bien.text.strip())
            title = home.find_element_by_css_selector('div.gallery-title')                
            titulo =title.find_element_by_tag_name("a").get_attribute('title')
            caracteristicas = home.find_element_by_css_selector('div.gallery-icons') 
            imagenes = caracteristicas.find_elements_by_tag_name("img") 
            ambientes=0
            dormitorios=0
            banios=0
            superficie=0
            for car in imagenes:
                texto =car.get_attribute('data-original-title')
                if  "Ambientes" in texto:
                    ambientes = texto.replace("Total de Ambientes:","").strip()
                if  "Dormitorios" in texto:
                    dormitorios = texto.replace("Num. de Dormitorios:","").strip()
                if  "Baños" in texto:
                    banios = texto.replace("Baños:","").strip()
                if  "Habitable" in texto:
                    superficie = texto.replace("Sup. Habitable(m2)","").strip()
            dto=RealStateEntryDTO(id_item, tipo, estVenta, lat, lng, tipoinv, titulo, precio, ambientes, dormitorios, banios, superficie, self.driver.current_url, url_element,url_from_db)
            self.data[url_from_db]=self.data[url_from_db] + [dto]
                        
                        
    def get_summary(self,driver,url_from_db):
        average_prize=0
        util_summary_builder=UtilsSummaryBuilder(self.data[url_from_db],url_from_db,average_prize)
        util_summary_builder.obtain_summary()
        summary = util_summary_builder.summary
        self.summaries[url_from_db] = summary
        