import math
import csv
from datetime import datetime
import os
from colorama import init, Fore, Style

# カラー表示の初期化
init()

def is_prime(number):
    """与えられた数字が素数かどうかを判断する関数"""
    # 2未満の数は素数ではない
    if number <= 1:
        return False
    # 2と3は素数
    if number <= 3:
        return True
    # 2と3の倍数を除外
    if number % 2 == 0 or number % 3 == 0:
        return False
    
    # 6の倍数±1の形で割り切れるかチェック
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    
    return True

def save_score(score):
    """スコアをCSVファイルに保存する"""
    file_path = "ranking.csv"
    time_id = datetime.now().strftime('%m%d_%H%M')
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([time_id, score, datetime.now().strftime('%Y-%m-%d')])

def show_ranking():
    """ランキングを表示する"""
    try:
        with open('ranking.csv', 'r', encoding='utf-8') as f:
            scores = list(csv.reader(f))
            if not scores:  # ファイルが空の場合
                print("まだ記録がありません")
                return
            
            # スコアでソート
            scores.sort(key=lambda x: int(x[1]), reverse=True)
            
            print("\n-------------------")
            print(f"{Fore.CYAN}ランキング TOP10{Style.RESET_ALL}")
            print("-------------------")
            for i, (time_id, score, date) in enumerate(scores[:10], 1):
                print(f"{i}位: ID:{time_id} - {Fore.YELLOW}{score}点{Style.RESET_ALL} ({date})")

    except FileNotFoundError:
        print("まだ記録がありません")

def play_game():
    """ゲームの実行"""
    previous_number = 0
    score = 0
    while True:
        if previous_number == 0:
            number = int(input("最初の素数を入力してください: "))
        else:
            print("-------------------")
            number = int(input(f"前回の数字 [{previous_number}] より大きい素数を入力してください: "))
        
        if number <= previous_number:
            print("\nゲームオーバー")
            print(f"{number} は {previous_number} より大きくありません。")
            break
        if is_prime(number):
            print(f"\n{number} は素数です!")
            previous_number = number
            score += number
        else:
            print("\nゲームオーバー")
            print(f"{number} は素数ではありません。")
            break

    print("\n-------------------")
    print(f"最終スコア: {Fore.GREEN}{score}{Style.RESET_ALL}")
    print("-------------------")

    if score > 0:
        save_score(score)
    
    show_ranking()
    return score

# メインループ
while True:
    # ゲームのルール説明
    print("-------------------")
    print("素数チェイスゲーム")
    print("-------------------")
    print("ルール：")
    print("1. 前回の数字より大きい素数を入力してください")
    print("2. 素数でない数字を入力するとゲームオーバー")
    print("3. 小さい数字を入力するとゲームオーバー\n")

    try:
        play_game()
    except ValueError:
        print(f"\n{Fore.RED}エラー: 正しい数値を入力してください{Style.RESET_ALL}")

    # リトライの確認
    print(f"\n{Fore.CYAN}もう一度プレイしますか？ (y/n):{Style.RESET_ALL}", end=" ")
    retry = input().lower()
    if retry != 'y':
        print("\nゲームを終了します。また遊んでね！")
        break
    print("\n" + "="*30 + "\n")  # ゲーム間の区切り