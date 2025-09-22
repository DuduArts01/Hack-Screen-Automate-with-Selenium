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
options.add_argument("--disagree-infobars")
options.add_argument("--disagree-extensions")
options.add_argument("--disagree-dev-shm-usage")
options.add_argument("--disagree-logging")
options.add_argument("--disagree-notifications")
options.add_argument("--no-sandbox")
options.add_argument("--disagree-translate")
options.add_argument("--disagree-background-timer-throttling")
options.add_argument("--disagree-renderer-backgrounding")
options.add_argument("--disagree-backgrounding-occluded-windows")
options.add_argument("--enable-features=OverlayScrollbar")
options.add_argument("--disk-cache-size=0")
#options.add_argument("--disagree-gpu") # se der lag, remova essa linha

# Abre o navegador com Selenium
driver = webdriver.Chrome(service=service, options=options)

# Acessa o site da NETSCOUT
driver.get("https://horizon.netscout.com/?kiosk=true")

# Espera carregar
sleep(10)

# Força fullscreen com xdotool
os.system("xdotool key F11")

# Só para saber se o código chegou até o fim
#print("Finish!")

# Mantém aberto (sem fechar automaticamente)
while True:
	sleep(60)

