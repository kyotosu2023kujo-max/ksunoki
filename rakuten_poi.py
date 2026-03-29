import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys # エンターキーを押すための部品

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
        driver.get("https://grp02.id.rakuten.co.jp/rms/nid/vc")
        time.sleep(3)
        
        print("2. IDとパスワードを入力します...")
        try:
            wait.until(EC.presence_of_element_located((By.ID, "loginInner_u"))).send_keys(USER_ID)
            driver.find_element(By.ID, "loginInner_p").send_keys(PASSWORD)
        except:
            wait.until(EC.presence_of_element_located((By.ID, "u"))).send_keys(USER_ID)
            driver.find_element(By.ID, "p").send_keys(PASSWORD)
            
        driver.find_element(By.NAME, "submit").click()
        print("ログイン成功！")
        time.sleep(5)

        print("3. 正門（トップページ）からの人間らしい検索を開始します...")
        
        for i, word in enumerate(targets):
            # 毎回ちゃんとトップページを開く
            driver.get("https://websearch.rakuten.co.jp/")
            time.sleep(3)
            
            # 検索窓（name="qt"）を見つけて、文字を入れてエンターキーを押す
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "qt")))
            search_box.clear()
            search_box.send_keys(word)
            search_box.send_keys(Keys.RETURN) # エンターキーをターン！
            
            print(f"[{i+1}/30] 正門から検索完了: {word}")
            time.sleep(random.uniform(5, 8)) 

        print("🎉 本日のウェブ検索ミッション（30回）を完了しました！")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_rakuten_search()
