import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- クラウド実行用のブラウザ設定 ---
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1') # スマホに見せかける

def run_rakuten_poi():
    # 金庫(Secrets)からID/PASSを読み込む
    USER_ID = os.environ.get('RAKUTEN_USER_ID')
    PASSWORD = os.environ.get('RAKUTEN_PASSWORD')
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        print("楽天ログインページにアクセス中...")
        driver.get("https://point.rakuten.co.jp/guidance/login/")
        
        # ログイン処理
        wait.until(EC.presence_of_element_id("loginInner_u")).send_keys(USER_ID)
        driver.find_element(By.ID, "loginInner_p").send_keys(PASSWORD)
        driver.find_element(By.NAME, "submit").click()
        print("ログインに成功しました。")
        
        time.sleep(5) # ログイン後の安定待ち

        # ポイントミッション（ポチポチページ）へ
        print("ポイントミッションページへ移動します...")
        driver.get("https://pointi.rakuten.co.jp/mission/")
        time.sleep(5)

        # 「℗1」のマークがついた未達成のミッションを探す
        # ※クラス名は楽天の仕様変更で変わることがありますが、現在はこれが一般的です
        missions = driver.find_elements(By.CLASS_NAME, "mission-click-target")
        
        if not missions:
            print("現在、未達成のミッションは見つかりませんでした。")
        else:
            print(f"{len(missions)}個のミッションを発見！順次ポチポチします...")
            for i, mission in enumerate(missions):
                try:
                    mission.click()
                    print(f"[{i+1}] クリック完了！ポイント獲得処理中...")
                    time.sleep(7) # 楽天側に怪しまれないための「人間らしいタメ」
                except Exception as e:
                    print(f"[{i+1}] クリックに失敗しました: {e}")

        print("本日の全自動ポイ活ルーティンを終了します。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_rakuten_poi()
