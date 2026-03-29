import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def run_kuji():
    # 1. GitHub Secrets からログイン情報を取得
    USER_ID = os.environ.get('RAKUTEN_USER_ID')
    USER_PASS = os.environ.get('RAKUTEN_PASSWORD')

    if not USER_ID or not USER_PASS:
        print("Error: RAKUTEN_ID or RAKUTEN_PASS is not set in Secrets.")
        return

    # 2. Chromeのヘッドレス設定（GitHub Actions用）
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # ユーザーエージェントを偽装してボット検知を回避しやすくする
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10) # 要素が見つかるまで最大10秒待機

    try:
        # 3. ログイン処理
        print("Logging in...")
        driver.get("https://kuji.rakuten.co.jp/")
        
        # 最初のくじを選択してログイン画面へ飛ばす
        first_kuji = driver.find_element(By.XPATH, "/html/body/div/main/section[2]/ul/li[1]/a")
        first_kuji.click()
        time.sleep(3)

        # ログイン情報の入力
        driver.find_element(By.ID, "loginInner_u").send_keys(USER_ID)
        driver.find_element(By.ID, "loginInner_p").send_keys(USER_PASS)
        driver.find_element(By.XPATH, "//input[@type='submit' or @value='ログイン']").click()
        print("Login successful (probably).")
        time.sleep(5)

        # 4. くじを順番に引くループ
        # サイトの構成が変わっている可能性があるため、多めに回す（例: 1〜30）
        for num in range(1, 31):
            url = "https://kuji.rakuten.co.jp/"
            driver.get(url)
            time.sleep(random.randint(3, 5))
            
            try:
                xpath = f"/html/body/div/main/section[2]/ul/li[{num}]/a"
                target_kuji = driver.find_element(By.XPATH, xpath)
                print(f"Checking Kuji #{num}...")
                target_kuji.click()
                time.sleep(random.randint(5, 8))

                # 「Start」ボタンを探してクリック
                try:
                    start_btn = driver.find_element(By.ID, "entry")
                    start_btn.click()
                    print(f"-> Kuji #{num} started!")
                    # くじのアニメーション待ち
                    time.sleep(random.randint(20, 30)) 
                except NoSuchElementException:
                    print(f"-> Kuji #{num} already played or Start button not found.")

            except NoSuchElementException:
                print(f"-> Kuji #{num} link not found. Ending loop.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    run_kuji()
