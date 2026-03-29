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
# ここがミソ！iPhoneからアクセスしているように見せかける偽装設定
options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1')

def run_mobile_poi():
    USER_ID = os.environ.get('RAKUTEN_USER_ID')
    PASSWORD = os.environ.get('RAKUTEN_PASSWORD')
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        print("1. 【スマホ偽装モード】ログイン画面を強制呼び出し...")
        driver.get("https://point.rakuten.co.jp/history/")
        time.sleep(5)
        
        print(f"★現在のURL: {driver.current_url}")

        if "id.rakuten.co.jp" in driver.current_url:
            print("2. ログイン画面を検知。入力欄を探査します...")
            
            # --- ハイブリッド入力システム ---
            # まずスマホ版のID欄を探す
            mobile_user_input = driver.find_elements(By.ID, "loginInner_u")
            
            if mobile_user_input:
                print("→ スマホ版の画面を確認！")
                mobile_user_input[0].send_keys(USER_ID)
                driver.find_element(By.ID, "loginInner_p").send_keys(PASSWORD)
            else:
                print("→ PC版の画面を確認！")
                wait.until(EC.presence_of_element_located((By.ID, "u"))).send_keys(USER_ID)
                driver.find_element(By.ID, "p").send_keys(PASSWORD)
            
            driver.find_element(By.NAME, "submit").click()
            print("ログインボタンを押しました！")
            time.sleep(5)
        else:
            print("既にログイン状態です。")

        print("3. スマホ版ミッションページへ移動します...")
        driver.get("https://point.rakuten.co.jp/mission/")
        time.sleep(5)
        
        print("4. ポチポチ用のバナーをスキャンします...")
        missions = driver.find_elements(By.CLASS_NAME, "mission-click-target")
        
        if not missions:
            print("結果: 未達成のミッションは見つかりませんでした。")
        else:
            print(f"結果: {len(missions)}個のミッションを発見！順次ポチポチします...")
            for i, mission in enumerate(missions):
                try:
                    mission.click()
                    print(f"[{i+1}] クリック完了！ポイント獲得！")
                    time.sleep(5)
                except Exception as e:
                    print(f"[{i+1}] クリック失敗: {e}")

        print("実験終了！無事に完走しました。")

    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_mobile_poi()
