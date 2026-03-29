import os
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def download_extension():
    # 楽天ウェブ検索の拡張機能の直接ダウンロードURL（Googleのサーバー）
    ext_id = "iihkglbebihpaflfihhkfmpabjgdpnol"
    url = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=120.0&x=id%3D{ext_id}%26installsource%3Dondemand%26uc"
    
    print("📦 拡張機能（武器）をGoogleサーバーから直接調達中...")
    r = requests.get(url)
    with open("rakuten.crx", "wb") as f:
        f.write(r.content)
    print("✅ 調達完了！rakuten.crx を作成しました。")

def run_ultimate_search():
    USER_ID = os.environ.get('RAKUTEN_USER_ID')
    PASSWORD = os.environ.get('RAKUTEN_PASSWORD')
    
    # 1. まず自分で拡張機能をダウンロードする
    download_extension()

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    # 2. ダウンロードしたばかりのファイルを装備
    options.add_extension('rakuten.crx')

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    search_words = ["量子力学", "相対性理論", "ブラックホール", "シュレーディンガーの猫", "エントロピー", "素粒子", "クォーク", "超ひも理論", "カオス理論", "ビッグバン"]
    random.shuffle(search_words)

    try:
        print("1. ログインゲートに突撃中...")
        driver.get("https://grp02.id.rakuten.co.jp/rms/nid/vc")
        time.sleep(3)
        
        try:
            wait.until(EC.presence_of_element_located((By.ID, "loginInner_u"))).send_keys(USER_ID)
            driver.find_element(By.ID, "loginInner_p").send_keys(PASSWORD)
        except:
            wait.until(EC.presence_of_element_located((By.ID, "u"))).send_keys(USER_ID)
            driver.find_element(By.ID, "p").send_keys(PASSWORD)
            
        driver.find_element(By.NAME, "submit").click()
        print("ログイン成功！拡張機能の同期を待ちます（15秒）...")
        time.sleep(15)

        print("2. 拡張機能を有効化した状態でトップページから検索開始...")
        for i, word in enumerate(search_words):
            driver.get("https://websearch.rakuten.co.jp/")
            time.sleep(5) # ページが完全に落ち着くのを待つ
            
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "qt")))
            search_box.clear()
            search_box.send_keys(word)
            search_box.send_keys(Keys.RETURN)
            
            print(f"[{i+1}/{len(search_words)}] 拡張機能モードで検索完了: {word}")
            time.sleep(random.uniform(7, 12)) 

        print("🎉 すべての工程が完了しました！")

    except Exception as e:
        print(f"エラー発生: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_ultimate_search()
