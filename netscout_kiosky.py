import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep

# Caminho do ChromeDriver
service = Service("/usr/bin/chromedriver")

# Configurações do Chromium
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") # iniciando maximizado
options.add_argument("--kiosk") # modo kiosk (sem barras, mais limpo)

# Remove a mensagem "controlado por software de teste"
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# ---- Otimizações ----
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-logging")
options.add_argument("--disable-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disable-translate")
options.add_argument("--disable-background-timer-throttling")
options.add_argument("--disable-renderer-backgrounding")
options.add_argument("--disable-backgrounding-occluded-windows")
options.add_argument("--enable-features=OverlayScrollbar")
options.add_argument("--disk-cache-size=0")
#options.add_argument("--disable-gpu") # se der lag, remova essa linha

# Abre o navegador com Selenium
driver = webdriver.Chrome(service=service, options=options)

# Acessa o site da NETSCOUT
driver.get("https://horizon.netscout.com/?kiosk=true")

# Espera carregar
sleep(10)

# Força fullscreen com xdotool
os.system("xdotool key F11")

# Mantém aberto (sem fechar automaticamente)
while True:
	sleep(60)

# Só para saber se o código chegou até o fim
print("Finish!")
