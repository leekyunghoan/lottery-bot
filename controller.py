import os
import sys
from dotenv import load_dotenv

import auth
import lotto645
# import win720  <- 연금복권 모듈은 더 이상 필요 없으므로 주석 처리하거나 삭제합니다.
import notification
import time


def buy_lotto645(authCtrl: auth.AuthController, cnt: int, mode: str):
    lotto = lotto645.Lotto645()
    _mode = lotto645.Lotto645Mode[mode.upper()]
    response = lotto.buy_lotto645(authCtrl, cnt, _mode)
    response['balance'] = lotto.get_balance(auth_ctrl=authCtrl)
    return response

def check_winning_lotto645(authCtrl: auth.AuthController) -> dict:
    lotto = lotto645.Lotto645()
    item = lotto.check_winning(authCtrl)
    return item

# 연금복권 구매 및 당첨 확인 함수는 더 이상 사용되지 않으므로 주석 처리하거나 삭제합니다.
# def buy_win720(authCtrl: auth.AuthController, username: str):
#     pension = win720.Win720()
#     response = pension.buy_Win720(authCtrl, username)
#     response['balance'] = pension.get_balance(auth_ctrl=authCtrl)
#     return response

# def check_winning_win720(authCtrl: auth.AuthController) -> dict:
#     pension = win720.Win720()
#     item = pension.check_winning(authCtrl)
#     return item

def send_message(mode: int, lottery_type: int, response: dict, webhook_url: str):
    notify = notification.Notification()

    if mode == 0: # 당첨 확인 모드
        if lottery_type == 0: # 로또 6/45
            notify.send_lotto_winning_message(response, webhook_url)
        # else: # 연금복권 알림은 삭제
        #     notify.send_win720_winning_message(response, webhook_url)
    elif mode == 1: # 구매 모드
        if lottery_type == 0: # 로또 6/45
            notify.send_lotto_buying_message(response, webhook_url)
        # else: # 연금복권 알림은 삭제
        #     notify.send_win720_buying_message(response, webhook_url)

def check():
    load_dotenv()

    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')

    globalAuthCtrl = auth.AuthController()
    globalAuthCtrl.login(username, password)
    
    response = check_winning_lotto645(globalAuthCtrl)
    send_message(0, 0, response=response, webhook_url=discord_webhook_url)

    # 연금복권 당첨 확인 로직 삭제
    # time.sleep(10)
    # response = check_winning_win720(globalAuthCtrl)
    # send_message(0, 1, response=response, webhook_url=discord_webhook_url)

def buy(): 
    
    load_dotenv() 

    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    # count = int(os.environ.get('COUNT')) # 환경변수에서 구매 수량을 가져오는 대신 1로 고정합니다.
    count = 1 # 매일 1장씩만 구매하도록 설정
    discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    mode = "AUTO"

    globalAuthCtrl = auth.AuthController()
    globalAuthCtrl.login(username, password)

    response = buy_lotto645(globalAuthCtrl, count, mode) 
    send_message(1, 0, response=response, webhook_url=discord_webhook_url)

    # 연금복권 구매 로직 삭제
    # time.sleep(10)
    # response = buy_win720(globalAuthCtrl, username) 
    # send_message(1, 1, response=response, webhook_url=discord_webhook_url)

def run():
    if len(sys.argv) < 2:
        print("Usage: python controller.py [buy|check]")
        return

    if sys.argv[1] == "buy":
        buy()
    elif sys.argv[1] == "check":
        check()
  
if __name__ == "__main__":
    run()
