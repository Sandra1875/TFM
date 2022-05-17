from selenium import webdriver
import sys

from utils_app.util_summary_builder import UtilsSummaryBuilder
from dto.detalle_dto import DetalleDTO
from dto.summary_scrapped_dto import SummaryScrappedDTO

import time 
import random

#https://www.seleniumhq.org/download/
#14393
#https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

class ScraperSeleniumRemax:

    def __init__(self, urls):
        self.urls = urls
        self.contador=0
        #self.driver = webdriver.Edge()
        self.driver = webdriver.Chrome(executable_path=r"F:\UIV\09 Fin Master\chromedriver_win32\chromedriver.exe")        
        #self.driver = webdriver.Firefox()
        self.data ={}
        self.summaries = {}
        self.address = ""
        self.estado = ""
        self.id_datos = ""
        self.atributos = {}
        self.caracteristicas = {}
    
    def get_data(self, id1):
        for url_from_db in self.urls:
            driver = self.driver
            driver.get(url_from_db) 
            self.get_data_from_page(driver, url_from_db, id1) 
        driver.close()
    
    def get_data_from_page(self,driver, url_from_db, id1):
        print("obtaining data from " + driver.current_url)
        random_int =573 + random.randint(-3, 3)
        driver.execute_script("window.scrollTo(0, "+str(random_int) +");")
        time.sleep(2.5 + random.uniform(0.5,0.9))
        formas = self.driver.find_elements_by_id("ssForm")
        for forma in formas:
            paginas = forma.find_element_by_id("page")
            secciones = paginas.find_element_by_css_selector('div.section-dark')    
            listas = secciones.find_element_by_css_selector("div.container")
            #row = listas.find_element_by_css_selector("div.row") 
            lista_rows = listas.find_element_by_css_selector("div.listfull-details")     
            sig_div= lista_rows.find_element_by_tag_name('div')       
            #datos del bien
            left = sig_div.find_element_by_id("LeftColumn")
            box = left.find_element_by_css_selector("div.box-generic")
            generic = box.find_element_by_css_selector("div.content-generic")
            key_data = generic.find_element_by_css_selector("div.key-data") 
            key_data_row = key_data.find_element_by_css_selector("div.row") 
            columnas = key_data_row.find_elements_by_css_selector("div.col-xs-12")
            for col in columnas:
                clase = col.get_attribute("class")
                if clase=="col-xs-12 key-address fts-mark":
                     self.address = col.text
                if clase=="col-xs-12 key-status fts-mark":
                     self.estado = col.text
                if clase=="col-xs-12 key-id":
                     self.id_datos = col.text
            #print("sourceHtml: " + str(sourceHtml))
            # datos especiales
            atributos = key_data.find_element_by_css_selector("div.attributes-data")        
            atr_data_row = atributos.find_element_by_css_selector("div.attributes-data-row")  
            atr_fila = atr_data_row.find_elements_by_css_selector("div.attributes-icons")

            self.atributos = {}
            contador =0
            for dato in atr_fila:
                #sourceHtml = dato.get_attribute("innerHTML")
                #print("sourceHtml: " + str(sourceHtml))
                #atributo=dato.find_element_by_css_selector('div.attributes-icons')
                item_row=dato.find_element_by_css_selector('div.data-item-row')
                item_label=item_row.find_element_by_css_selector('div.data-item-label')
                label= item_label.find_element_by_tag_name('span')
                #print("label: " + label.text)
                item_label=item_row.find_element_by_css_selector('div.data-item-value')
                valor= item_label.find_element_by_tag_name('span')
                #print("Valor: " + valor.text)
                self.atributos[contador] =(label.text , valor.text)
                contador+=1
            #print("total: -->> " + str(self.atributos))  
            land_data = generic.find_elements_by_css_selector("div.features-container")
                
            self.caracteristicas = {}
            for element in land_data:
                land_data_row = element.find_element_by_css_selector("div.row")
                columnas_l = land_data_row.find_elements_by_css_selector("div.col-xs-6")
                i=0                
                for col_l in columnas_l:
                    #sourceHtml = col_l.get_attribute("innerHTML")
                    #print("sourceHtml: " + str(sourceHtml))
                    caract= col_l.find_element_by_tag_name('span')                
                    clase = caract.get_attribute("title")
                    self.caracteristicas[i] = clase
                    i+=1
                #print("caracteristicas: " + str(self.caracteristicas))      
        dto=DetalleDTO(self.id_datos, self.estado, self.address, self.atributos, self.caracteristicas, url_from_db, id1)
        if(not url_from_db in self.data.keys()): self.data[url_from_db]=[]
        self.data[url_from_db]=self.data[url_from_db] + [dto]



    