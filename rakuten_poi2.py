import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def run_kuji():
    # 1. GitHub Secrets からログイン情報を取得
    USER_ID = os.environ.get('RAKUTEN_USER_ID')
    USER_PASS = os.environ.get('RAKUTEN_PASSWORD')

    if not USER_ID or not USER_PASS:
        print("Error: RAKUTEN_ID or RAKUTEN_PASS is not set in Secrets.")
        return

    # 2. Chromeのヘッドレス設定
    options = Options()
    options.add_argument('--headless=new') # 最新のヘッドレスモード
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    # ボット検知回避用のUser-Agent
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15) # 最大15秒待機

    try:
        print("--- Start Rakuten Kuji Automation ---")
        driver.get("https://kuji.rakuten.co.jp/")
        
        # 最初のくじをクリックしてログイン画面へ
        print("Clicking first kuji to trigger login...")
        first_kuji = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "main section ul li a")))
        first_kuji.click()

        # 3. ログイン処理（新旧両対応）
        print("Step 1: Entering ID...")
        # ID入力フィールド（新: login_id, 旧: loginInner_u）
        id_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#login_id, input#loginInner_u")))
        id_field.send_keys(USER_ID)
        
        # 「次へ」ボタンがあればクリック（ステップ式の場合）
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "button.loginButton, input#loginInner_0")
            next_btn.click()
            print("Clicked 'Next' button.")
            time.sleep(2)
        except NoSuchElementException:
            print("No 'Next' button found, proceeding to password.")

        print("Step 2: Entering Password...")
        # パスワード入力フィールド（新: password, 旧: loginInner_p）
        pass_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#password, input#loginInner_p")))
        pass_field.send_keys(USER_PASS)
        
        # ログインボタンをクリック
        login_submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")))
        login_submit.click()
        
        print("Login submit clicked. Waiting for redirection...")
        time.sleep(8)

        # 4. くじ引きループ
        for num in range(1, 40): # 最大40個までチェック
            print(f"\nChecking Kuji #{num}...")
            driver.get("https://kuji.rakuten.co.jp/")
            time.sleep(random.randint(3, 5))
            
            try:
                # くじのリストを取得
                kuji_links = driver.find_elements(By.CSS_SELECTOR, "main section ul li a")
                if num > len(kuji_links):
                    print("No more kuji links found.")
                    break
                
                kuji_links[num-1].click()
                print(f"Opened Kuji #{num} page.")
                time.sleep(random.randint(4, 7))

                # 「Start」ボタンまたは「くじを引く」ボタンを探す
                try:
                    # IDやXPATH、画像ボタンなど複数の可能性を考慮
                    start_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#entry, .btn-entry, a[href*='entry']")))
                    start_btn.click()
                    print(f"Success: Kuji #{num} started!")
                    time.sleep(random.randint(20, 30)) # アニメーション待ち
                except (TimeoutException, NoSuchElementException):
                    print(f"Skip: Start button not found for Kuji #{num} (Maybe already done).")

            except Exception as e:
                print(f"Error at Kuji #{num}: {type(e).__name__}")
                continue

    except Exception as e:
        print(f"Critical Error: {e}")
        # デバッグ用に現在のURLを表示
        print(f"Current URL: {driver.current_url}")
    
    finally:
        print("\n--- Automation Finished ---")
        driver.quit()

if __name__ == "__main__":
    run_kuji()
