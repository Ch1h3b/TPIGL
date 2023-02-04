import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def sign_in(email, password):
    google_btn = driver.find_element(By.CSS_SELECTOR,
                                     "#root > div.flex.justify-center.mt-16.md\:mt-20.flex-col.gap-10.items-center.h-\[calc\(100vh-64px\)\].md\:h-\[calc\(100vh-80px\)\] > div.flex.flex-col.shadow-xl.rounded-3xl.h-2\/5.w-3\/5.md\:w-2\/5 > div.relative.text-\[\#7A7474\].h-3\/4.flex.flex-col.justify-start.md\:justify-center.mb-5.gap-5.items-center > a", )
    google_btn.click()
    google_form_mail_address = driver.find_element(By.CSS_SELECTOR, "#identifierId")
    google_form_mail_address.send_keys(email)
    next_btn = driver.find_element(By.CSS_SELECTOR, "#identifierNext")
    next_btn.click()
    google_form_password = driver.find_element(By.CSS_SELECTOR,
                                               "#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", )
    google_form_password.send_keys(password)
    next_btn2 = driver.find_element(By.CSS_SELECTOR, "#passwordNext")
    next_btn2.click()
    time.sleep(7)


def publier_annonce_btn_click():
    publier_annonce_btn = driver.find_element(By.CSS_SELECTOR,
                                              "#root > div.flex.gap-10.flex-col > div > div.hidden.md\:flex.gap-2.lg\:gap-4 > a:nth-child(3)")
    publier_annonce_btn.click()


def ajouter_titre_annonce(titre):
    titre_annonce = driver.find_element(By.CSS_SELECTOR, "#titre")
    titre_annonce.send_keys(titre)


def ajouter_desc_annonce(desc):
    desc_annonce = driver.find_element(By.CSS_SELECTOR, "#description")
    desc_annonce.send_keys(desc)


def ajouter_surface_annonce(surface):
    surface_annonce = driver.find_element(By.CSS_SELECTOR, "#surface")
    surface_annonce.send_keys(surface)


def ajouter_prix_annonce(prix):
    prix_annonce = driver.find_element(By.CSS_SELECTOR, "#prix")
    prix_annonce.send_keys(prix)


def ajouter_type_annonce(type):
    type_annonce = Select(driver.find_element(By.CSS_SELECTOR,
                                              "#annonceForm > div:nth-child(1) > div.flex.justify-center.gap-3.items-center > select"))
    type_annonce.select_by_index(type)


def ajouter_wilaya_annonce(wilaya):
    wilaya_annonce = Select(driver.find_element(By.CSS_SELECTOR,
                                                "#annonceForm > div:nth-child(1) > div.flex.justify-center.gap-2.items-center > select:nth-child(1)"))
    wilaya_annonce.select_by_index(wilaya)


def ajouter_commune_annonce(commune):
    commune_annonce = Select(driver.find_element(By.CSS_SELECTOR,
                                                 "#annonceForm > div:nth-child(1) > div.flex.justify-center.gap-2.items-center > select:nth-child(2)"))
    commune_annonce.select_by_index(commune)


def ajouter_categorie_annonce(categorie):
    categorie_annonce = driver.find_element(By.CSS_SELECTOR, "#categorie")
    categorie_annonce.send_keys(categorie)


service = Service('C:\selenium drivers\chromedriver.exe')
driver = webdriver.Chrome(service=service)
url = 'http://localhost:3000/'
driver.get(url)
driver.maximize_window()
driver.implicitly_wait(30)

sign_in(email="", password="") # email & password of Gmail account

publier_annonce_btn_click()

ajouter_titre_annonce("Vente Appartement Alger Cheraga")

ajouter_desc_annonce(
    "Résidence Sérénité, un accord parfait entre modernité, sécurité, emplacement privilégié et architecture réfléchie. Situé au cœur du quartier huppé de Dar Diaf, Sérénité est une résidence ultra privative de 10 logements, allant du F3 au F5, en simplex ou duplex")

ajouter_surface_annonce("60 M²")

ajouter_prix_annonce("8000000")

ajouter_type_annonce(3)

ajouter_wilaya_annonce(4)

ajouter_commune_annonce(29)

ajouter_categorie_annonce("Vente")

adresse_annonce = driver.find_element(By.CSS_SELECTOR, "#addresse")
adresse_annonce.send_keys("Alger - Cheraga")

adresse_annoncer = driver.find_element(By.CSS_SELECTOR, "#myaddresse")
adresse_annoncer.send_keys("Alger - Cheraga")

teleph_annoncer = driver.find_element(By.CSS_SELECTOR, "#telephone")
teleph_annoncer.send_keys("34701057")

importer_btn = driver.find_element(By.CSS_SELECTOR,
                                   "#annonceForm > div.annonce-form.mb-9.flex.flex-col.gap-8.lg\:w-\[48\%\].justify-start.items-center > label")
importer_btn.click()

element = WebDriverWait(driver, 100).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR,
     "#annonceForm > div.annonce-form.mb-9.flex.flex-col.gap-8.lg\:w-\[48\%\].justify-start.items-center > div.image-Wrapper.flex.flex-wrap.flex-row.justify-center.md\:justify-start.gap-5.max-w-\[550px\] > div > img")))

#publier_btn = driver.find_element(By.CSS_SELECTOR, "#annonceForm > button")

#publier_btn.click()
print("Test Completed !")
while True:
    time.sleep(1)
