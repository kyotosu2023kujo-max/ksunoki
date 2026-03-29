import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- ロボットだとバレにくくするための強力な設定 ---
options = Options()
options.add_argument('--headless=new') # 最新の画面なしモード
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-blink-features=AutomationControlled') # ロボット判定を回避
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

def run_debug():
    driver = webdriver.Chrome(options=options)
    try:
        print("楽天ログインページにアクセス中...")
        driver.get("https://point.rakuten.co.jp/guidance/login/")
        
        # 画面が完全に表示されるまで少し長めに待つ
        time.sleep(5) 
        
        # --- 観測装置：サーバーが見ている画面の情報を出力 ---
        print("========================================")
        print(f"★現在のURL: {driver.current_url}")
        print(f"★ページのタイトル: {driver.title}")
        print("★ページの中身（最初の500文字）:")
        print(driver.page_source[:500])
        print("========================================")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_debug()
