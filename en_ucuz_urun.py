from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sqlite3
from urllib.parse import urlsplit
from selenium.webdriver.chrome.options import Options

def trendyol_urun():

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get("http://www.trendyol.com")
    time.sleep(1)
    driver.find_element(By.ID,"Combined-Shape").click()
    time.sleep(1)
    arama_kutusu=driver.find_element(By.CSS_SELECTOR,".N4M8bfaJ input")
    arama_kutusu.send_keys(urun)
    arama_kutusu.send_keys(Keys.ENTER)
    time.sleep(1)
    fiyatlar=driver.find_elements(By.CSS_SELECTOR,".prc-box-dscntd")
    #fiyatlar=fiyatlar[:10]
    basliklar=driver.find_elements(By.CSS_SELECTOR,"span.prdct-desc-cntnr-name")
    #basliklar=basliklar[:10]
    linkler=driver.find_elements(By.CSS_SELECTOR,"div.p-card-chldrn-cntnr a")
    #linkler=linkler[:10]


    vt=sqlite3.connect("en_ucuz_urun.db")
    im=vt.cursor()
    im.execute("CREATE TABLE IF NOT EXISTS urunler (urun_adi TEXT,urun_fiyati TEXT,site_adi TEXT,urun_linki TEXT)")
    for i in range(len(fiyatlar)):
        im.execute("INSERT INTO urunler VALUES (?,?,?,?)",(basliklar[i].text,fiyatlar[i].text,"trendyol",linkler[i].get_attribute("href")))
    vt.commit()
    print("bulundu!!!")



def hepsiburada_urun(urun):
    urun=urun.replace(" ","+")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    link="https://www.hepsiburada.com/ara?q="+urun
    driver.get(link)
    selector = '[data-test-id="price-current-price"]:not(.hepsiads-sponsored-brand-widget-bInaCk)'
    selector_title = '[data-test-id="product-card-name"]:not(.hepsiads-sponsored-brand-widget-kGaKfx)'
    fiyatlar=driver.find_elements(By.CSS_SELECTOR,selector)
    basliklar=driver.find_elements(By.CSS_SELECTOR,selector_title)
    #basliklar=basliklar[:10]
    #fiyatlar=fiyatlar[:10]
    time.sleep(1)
    selector_link=driver.find_elements(By.CSS_SELECTOR,".moria-ProductCard-joawUM a")
    link_list = []
    for a in selector_link:
        link = a.get_attribute("href")
        link_list.append(link)
    linkler=link_list
    
    vt=sqlite3.connect("en_ucuz_urun.db")
    im=vt.cursor()
    im.execute("CREATE TABLE IF NOT EXISTS urunler (urun_adi TEXT,urun_fiyati TEXT,site_adi TEXT,urun_linki TEXT)")
    
    for i in range(len(fiyatlar)):
        im.execute("INSERT INTO urunler VALUES (?,?,?,?)",(basliklar[i].text,fiyatlar[i].text,"hepsiburada",linkler[i]))
    vt.commit()
    print("en ucuz ürünler bulunuyor...")

while True:
    urun=input("istediğiniz ürün:")
    hepsiburada_urun(urun)
    trendyol_urun()
    vt=sqlite3.connect("en_ucuz_urun.db")
    im=vt.cursor()
    im.execute("SELECT COUNT(*) FROM urunler")
    sayi=im.fetchone()
    print(sayi[0],"tane ürün bulundu.")
    a=input("Kaç tane ürün görmek istersiniz?")
    
    im.execute("SELECT DISTINCT urun_adi, urun_fiyati, urun_linki FROM urunler WHERE urun_fiyati > (SELECT AVG(urun_fiyati) * 0.75 FROM urunler) ORDER BY urun_fiyati ASC LIMIT ?", (a,))
    sonuclar=im.fetchall()
    for sonuc in sonuclar:
        print(sonuc)
    secim=input("Devam etmek istiyor musunuz? (e/h)")
    if secim=="h":
        
        im.execute("DELETE FROM urunler")
        vt.commit()
        vt.close()
        print("beni kullandığın için teşekkürler...")
        time.sleep(2)
        break
    else:
        im.execute("DELETE FROM urunler")
        vt.commit()
        vt.close()
        continue
