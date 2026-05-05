import time
import winsound
from datetime import datetime
from playwright.sync_api import sync_playwright

# --- CONFIGURATION ---
# The URL of the product you want to monitor
URL = "https://store.steampowered.com/hardware/steamcontroller"

# Interval in seconds between checks (60 seconds is recommended to avoid rate limits)
CHECK_INTERVAL = 60 

def play_alarm():
    """
    Triggers the Windows system sound to notify the user.
    Uses 'SystemAsterisk' which is the standard Windows notification sound.
    """
    try:
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
    except Exception as e:
        print(f"Could not play sound: {e}")

def check_steam_stock():
    """
    Launches a headless browser, navigates to the Steam page, 
    and checks for the 'ReservationUnavailable' class.
    """
    with sync_playwright() as p:
        # Launching the browser in headless mode (no visible window)
        browser = p.chromium.launch(headless=True)
        
        # Creating a browser context with a specific User-Agent to mimic a real desktop user
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        page = context.new_page()
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        try:
            # Navigate to the URL and wait until the network has no more activity for 500ms
            page.goto(URL, wait_until="networkidle")
            
            # Locate the specific CSS class that indicates "Out of Stock"
            # .is_visible() returns True if the element exists and is shown on the page
            is_unavailable = page.locator(".ReservationUnavailable").is_visible()

            if is_unavailable:
                print(f"[{timestamp}] Status: Out of stock (Class '.ReservationUnavailable' found).")
                return False
            else:
                # SUCCESS: The indicator class is missing!
                print(f"[{timestamp}] 🚀 ALERT: The product might be available!")
                print(f"Check the page immediately: {URL}")
                
                # Play the alarm sound 3 times to grab attention
                for _ in range(3):
                    play_alarm()
                    time.sleep(1)
                
                return True # Stops the main loop

        except Exception as e:
            print(f"[{timestamp}] Error during page check: {e}")
            return False
        finally:
            # Ensuring the browser is closed even if an error occurs
            browser.close()

def main():
    print("--- Steam Hardware Stock Checker ---")
    print(f"Monitoring URL: {URL}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print("Press Ctrl+C to stop the script.\n")
    
    try:
        while True:
            # If check_steam_stock returns True, we found stock and can stop
            if check_steam_stock():
                print("Monitoring finished. Good luck with your purchase!")
                break
            
            # Wait for the defined interval before checking again
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    main()
