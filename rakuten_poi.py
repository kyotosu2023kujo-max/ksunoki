import os
import time
import random
import urllib.parse
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

def run_rakuten_search():
    USER_ID = os.environ.get('RAKUTEN_USER_ID')
    PASSWORD = os.environ.get('RAKUTEN_PASSWORD')
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    search_words = [
        "量子力学", "シュレーディンガーの猫", "相対性理論", "ブラックホール", "エントロピー",
        "素粒子", "クォーク", "ダークマター", "ダークエネルギー", "超ひも理論",
        "ハイゼンベルクの不確定性原理", "パウリの排他律", "フェルミ粒子", "ボース粒子", "超伝導",
        "マクスウェルの方程式", "熱力学第一法則", "プランク定数", "光電効果", "アインシュタイン",
        "ニュートン力学", "ラグランジュ力学", "ハミルトニアン", "波動関数", "スピン",
        "カオス理論", "フラクタル", "統計力学", "ブラウン運動", "宇宙マイクロ波背景放射",
        "重力波", "中性子星", "白色矮星", "事象の地平面", "ビッグバン"
    ]
    random.shuffle(search_words)
    targets = search_words[:30]

    try:
        print("1. 楽天の共通ログインゲートに突入します...")
        # 楽天の最も確実な大元ログインURL
        driver.get("https://grp02.id.rakuten.co.jp/rms/nid/vc")
        time.sleep(3)
        
        print("2. IDとパスワードを入力します...")
        # PC版・スマホ版どちらの画面が出ても対応できるハイブリッド入力
        try:
            wait.until(EC.presence_of_element_located((By.ID, "loginInner_u"))).send_keys(USER_ID)
            driver.find_element(By.ID, "loginInner_p").send_keys(PASSWORD)
            print("→ [スマホ版レイアウト] を検知・入力しました")
        except:
            wait.until(EC.presence_of_element_located((By.ID, "u"))).send_keys(USER_ID)
            driver.find_element(By.ID, "p").send_keys(PASSWORD)
            print("→ [PC版レイアウト] を検知・入力しました")
            
        driver.find_element(By.NAME, "submit").click()
        print("ログイン成功！譲太郎さんのアカウントで入室しました。")
        time.sleep(5)

        print("3. 楽天ウェブ検索での自動検索（30回）を開始します...")
        for i, word in enumerate(targets):
            encoded_word = urllib.parse.quote(word)
            search_url = f"https://websearch.rakuten.co.jp/Web?qt={encoded_word}"
            driver.get(search_url)
            print(f"[{i+1}/30] 検索完了: {word}")
            time.sleep(random.uniform(5, 8)) # 人間らしいランダム待機

        print("🎉 本日のウェブ検索ミッション（30回）を完了しました！")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_rakuten_search()
