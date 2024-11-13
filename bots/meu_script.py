from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

def start_bot():
    # Inicialize o WebDriver (usando Chrome neste exemplo)
    # Certifique-se de substituir o caminho do chromedriver, se necessário
    driver = webdriver.Chrome()
    try:
        # Acesse o YouTube
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")
        driver.maximize_window()
        # Aguarde alguns segundos para garantir que a página carregou completamente
        # time.sleep(2)  # Isso é apenas para ver o YouTube aberto, você pode remover para agilizar o script
       
        # Exemplo: Buscar por um termo no YouTube
        title = driver.title
        driver.implicitly_wait(0.5)
        text_box = driver.find_element(by=By.NAME, value="my-text")
        submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
        driver.implicitly_wait(2)
        text_box.send_keys("Selenium")
        driver.implicitly_wait(2)
        submit_button.click()

        # Espera para observar o resultado (opcional)
        time.sleep(10)

    finally:
        # Fecha o navegador
        driver.quit()

start_bot()