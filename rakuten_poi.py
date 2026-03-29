import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

def run_rakuten_poi():
    USER_ID = os.environ.get('RAKUTEN_USER_ID')
    PASSWORD = os.environ.get('RAKUTEN_PASSWORD')
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        print("1. ポイントミッションページへ直接アクセスします...")
        # ミッションページにアクセス（未ログインなら勝手にログイン画面に飛ばされる）
        driver.get("https://point.rakuten.co.jp/mission/")
        time.sleep(5)
        
        print(f"★現在のURL: {driver.current_url}")

        # もしURLに「id.rakuten.co.jp」が含まれていたら、そこは本物のログイン画面！
        if "id.rakuten.co.jp" in driver.current_url:
            print("2. 本物のログイン画面を検知しました。IDとパスワードを入力します...")
            wait.until(EC.presence_of_element_located((By.ID, "u"))).send_keys(USER_ID)
            driver.find_element(By.ID, "p").send_keys(PASSWORD)
            driver.find_element(By.NAME, "submit").click()
            print("ログインボタンを押しました！")
            time.sleep(5)
            
            # ログイン後、念のためもう一度ミッションページを開き直す
            driver.get("https://point.rakuten.co.jp/mission/")
            time.sleep(5)
        
        print("3. ミッションページでポチポチを開始します...")
        missions = driver.find_elements(By.CLASS_NAME, "mission-click-target")
        
        if not missions:
            print("現在、未達成のミッションは見つかりませんでした。（または既に完了しています）")
        else:
            print(f"{len(missions)}個のミッションを発見！順次ポチポチします...")
            for i, mission in enumerate(missions):
                try:
                    mission.click()
                    print(f"[{i+1}] クリック完了！ポイント獲得！")
                    time.sleep(5) # 人間らしいタメ
                except Exception as e:
                    print(f"[{i+1}] クリック失敗: {e}")

        print("本日の全自動ポイ活ルーティンを正常に終了しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_rakuten_poi()
