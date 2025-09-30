import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException
from time import sleep

CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
TARGET_URL = "https://horizon.netscout.com/?kiosk=true"
REFRESH_INTERVAL = 180  # segundos -> 3 minutos
RESTART_MAX_TRIES = 3   # quantas vezes tentar recriar o driver em caso de erro

def make_driver():
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--kiosk")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # otimizações
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
    # options.add_argument("--disable-gpu") # descomente se precisar

    driver = webdriver.Chrome(service=service, options=options)
    return driver

def ensure_fullscreen_with_xdotool():
    # chama xdotool para forçar F11 caso chrome saia do fullscreen
    try:
        os.system("xdotool key F11")
    except Exception:
        pass

def open_page(driver):
    driver.get(TARGET_URL)
    # espere um pouco para carregar antes do primeiro refresh
    sleep(8)
    ensure_fullscreen_with_xdotool()

def safe_refresh(driver):
    """Tenta atualizar usando Selenium; levanta WebDriverException se falhar."""
    try:
        driver.refresh()
        # opcional: small wait pra garantir que carregou
        sleep(5)
        ensure_fullscreen_with_xdotool()
    except (WebDriverException, TimeoutException) as e:
        raise

def recreate_driver_and_open():
    """Cria um novo driver e abre a página (usado se o driver travar)."""
    try:
        new_driver = make_driver()
        open_page(new_driver)
        return new_driver
    except Exception as e:
        # se até criar falhar, retorne None para tratamento
        return None

def main_loop():
    driver = make_driver()
    try:
        open_page(driver)
    except Exception:
        # se falhar na primeira vez, tenta recriar algumas vezes
        driver.quit()
        driver = None
        tries = 0
        while tries < RESTART_MAX_TRIES and driver is None:
            tries += 1
            print(f"Tentativa {tries} para criar driver...")
            driver = recreate_driver_and_open()
            if driver is None:
                sleep(3)
        if driver is None:
            raise RuntimeError("Não foi possível iniciar o navegador. Verifique o chromedriver e dependências.")

    print("Página aberta. Entrando no loop de atualização a cada", REFRESH_INTERVAL, "segundos.")
    restart_attempts = 0

    try:
        while True:
            sleep(REFRESH_INTERVAL)
            try:
                print("Tentando dar refresh...")
                safe_refresh(driver)
                restart_attempts = 0  # reset após sucesso
                print("Refresh OK.")
            except Exception as e:
                print("Erro no refresh:", repr(e))
                restart_attempts += 1
                # tenta recriar o driver até RESTART_MAX_TRIES vezes
                try:
                    print("Tentando recriar driver (tentativa", restart_attempts, ")...")
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    driver = recreate_driver_and_open()
                    if driver is None:
                        print("Falha ao recriar driver.")
                    else:
                        print("Driver recriado com sucesso.")
                        restart_attempts = 0
                except Exception as e2:
                    print("Erro ao recriar driver:", repr(e2))

                # se muitas falhas, aguarda mais tempo antes de nova tentativa
                if restart_attempts >= RESTART_MAX_TRIES:
                    print(f"Muitas falhas ({restart_attempts}). Aguardando 60s antes de tentar novamente...")
                    sleep(60)
    except KeyboardInterrupt:
        print("Encerrando por KeyboardInterrupt...")
    finally:
        try:
            driver.quit()
        except Exception:
            pass
        print("Driver finalizado. Saindo.")

if __name__ == "__main__":
    main_loop()
