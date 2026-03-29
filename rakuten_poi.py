import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def run_smuggle_search():
    USER_ID = os.environ.get('RAKUTEN_USER_ID')
    PASSWORD = os.environ.get('RAKUTEN_PASSWORD')
    
    options = Options()
    # 最新のHeadlessモードは拡張機能の読み込みに対応しています
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    # 🚨 ここが最大のハッキングポイント：拡張機能（CRX）の強制マウント
    extension_path = os.path.join(os.getcwd(), 'rakuten.crx')
    if os.path.exists(extension_path):
        options.add_extension(extension_path)
        print("📦 密輸品（rakuten.crx）の装備に成功しました！ツールバーありで起動します。")
    else:
        print("⚠️ 警告：密輸品（rakuten.crx）が見つかりません！素手（拡張機能なし）で突撃します。")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    search_words = [
        "量子力学", "シュレーディンガーの猫", "相対性理論", "ブラックホール", "エントロピー",
        "素粒子", "クォーク", "ダークマター", "ダークエネルギー", "超ひも理論",
        "ハイゼンベルクの不確定性原理", "パウリの排他律", "フェルミ粒子", "ボース粒子", "超伝導"
    ]
    random.shuffle(search_words)
    targets = search_words[:10] # テスト用に10回に減らしておきます

    try:
        print("1. 共通ログインゲートから侵入し、拡張機能にCookie（身分証）を吸わせます...")
        driver.get("https://grp02.id.rakuten.co.jp/rms/nid/vc")
        time.sleep(3)
        
        try:
            wait.until(EC.presence_of_element_located((By.ID, "loginInner_u"))).send_keys(USER_ID)
            driver.find_element(By.ID, "loginInner_p").send_keys(PASSWORD)
        except:
            wait.until(EC.presence_of_element_located((By.ID, "u"))).send_keys(USER_ID)
            driver.find_element(By.ID, "p").send_keys(PASSWORD)
            
        driver.find_element(By.NAME, "submit").click()
        print("ログイン成功！拡張機能が同期するのを10秒待ちます...")
        time.sleep(10) # 拡張機能がログイン状態を認識するまでの待機時間

        print("2. 正門（トップページ）からの検索を開始します...")
        for i, word in enumerate(targets):
            driver.get("https://websearch.rakuten.co.jp/")
            time.sleep(3)
            
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "qt")))
            search_box.clear()
            search_box.send_keys(word)
            search_box.send_keys(Keys.RETURN)
            
            print(f"[{i+1}/10] 検索完了: {word}")
            time.sleep(random.uniform(5, 8)) 

        print("🎉 テスト検索（10回）完了！画面のポイントが増えているか確認してください！")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_smuggle_search()
