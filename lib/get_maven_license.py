from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

def get_license_info(group_id, artifact_id):
    url = f"https://mvnrepository.com/artifact/{group_id}/{artifact_id}"
    
    options = Options()
    options.headless = True  # Esegui in modalità headless (senza GUI)
    service = FirefoxService(executable_path="data/driver/geckodriver")  # Aggiorna questo percorso

    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)
    time.sleep(3)  # Attendi che la pagina si carichi
    
    try:
        license_section = driver.find_element(By.CSS_SELECTOR, 'section.b.lic')
        licenses = license_section.find_elements(By.TAG_NAME, 'p')
        license_names = [license.text for license in licenses]
        return license_names
    except Exception as e:
        print(f"Errore durante il recupero delle licenze: {e}")
        return None
    finally:
        driver.quit()

# Esempio di utilizzo
group_id = "com.fasterxml.jackson.core"
artifact_id = "jackson-annotations"

license_info = get_license_info(group_id, artifact_id)
if license_info:
    print(f"Licenze per {group_id}:{artifact_id}: {', '.join(license_info)}")
else:
    print(f"Licenza per {group_id}:{artifact_id} non trovata.")
