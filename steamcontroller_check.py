import time
import winsound  # Standard-Windows-Bibliothek für Sounds
from datetime import datetime
from playwright.sync_api import sync_playwright

# --- KONFIGURATION ---
URL = "https://store.steampowered.com/hardware/steamcontroller"
CHECK_INTERVAL = 60  # Sekunden zwischen den Prüfungen

def play_alarm():
    """Spielt einen System-Sound ab (Sternchen/Asterisk-Sound von Windows)."""
    # Alternativ kannst du winsound.Beep(Frequenz, Dauer) nutzen
    # Hier nutzen wir den Standard-Hinweiston
    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
    print("🔔 SOUND ABGESPIELT!")

def check_steam_stock():
    """Prüft die Steam-Seite auf die Verfügbarkeit."""
    with sync_playwright() as p:
        # Browser im Hintergrund starten
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        try:
            # Seite laden und warten, bis JavaScript fertig ist
            page.goto(URL, wait_until="networkidle")
            
            # Prüfung: Existiert die Klasse, die "nicht verfügbar" anzeigt?
            is_unavailable = page.locator(".ReservationUnavailable").is_visible()

            if is_unavailable:
                print(f"[{timestamp}] Status: Immer noch nicht vorrätig.")
                return False
            else:
                # DIE KLASSE FEHLT -> ERFOLG!
                print(f"[{timestamp}] 🚀 ALARM! Der Controller scheint verfügbar zu sein!")
                print(f"Hier prüfen: {URL}")
                
                # Wir spielen den Ton 3 Mal ab, um sicherzugehen
                for _ in range(3):
                    play_alarm()
                    time.sleep(1)
                
                return True # Signalisiert der main-Schleife, dass wir fertig sind

        except Exception as e:
            print(f"[{timestamp}] Ein Fehler ist aufgetreten: {e}")
            return False
        finally:
            browser.close()

def main():
    print("--- Steam Controller Stock Checker ---")
    print(f"Intervall: {CHECK_INTERVAL} Sekunden")
    print("Beenden mit: Strg + C\n")
    
    try:
        while True:
            if check_steam_stock():
                print("Prüfung beendet. Viel Erfolg beim Kauf!")
                break
            
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nMonitoring manuell beendet.")

if __name__ == "__main__":
    main()
