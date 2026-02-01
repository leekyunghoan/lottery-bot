import os
import sys
from dotenv import load_dotenv

import auth
import lotto645
import notification
import time

def _setup_and_login():
    load_dotenv(override=True)
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')
    
    # 알림 설정 확인
    slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    if slack_webhook_url and slack_webhook_url.startswith("YOUR_"):
        slack_webhook_url = None

    discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    if discord_webhook_url and discord_webhook_url.startswith("YOUR_"):
        discord_webhook_url = None

    # 슬랙 우선, 없으면 디스코드 사용
    webhook_url = slack_webhook_url if slack_webhook_url else discord_webhook_url

    auth_ctrl = auth.AuthController()
    auth_ctrl.login(username, password)

    return auth_ctrl, username, webhook_url

def buy_lotto645(authCtrl: auth.AuthController, cnt: int, mode: str):
    lotto = lotto645.Lotto645()
    _mode = lotto645.Lotto645Mode[mode.upper()]
    response = lotto.buy_lotto645(authCtrl, cnt, _mode)
    response['balance'] = authCtrl.get_user_balance()
    return response

def check_winning_lotto645(authCtrl: auth.AuthController) -> dict:
    lotto = lotto645.Lotto645()
    item = lotto.check_winning(authCtrl)
    item['balance'] = authCtrl.get_user_balance()
    return item

def send_message(mode: int, response: dict, webhook_url: str):
    notify = notification.Notification()
    # mode 0: 당첨 확인, mode 1: 구매 결과
    if mode == 0:
        notify.send_lotto_winning_message(response, webhook_url)
    elif mode == 1: 
        notify.send_lotto_buying_message(response, webhook_url)

def check():
    auth_ctrl, _, webhook_url = _setup_and_login()
    response = check_winning_lotto645(auth_ctrl)
    send_message(0, response=response, webhook_url=webhook_url)

def buy(): 
    load_dotenv(override=True) 
    count = int(os.environ.get('COUNT'))
    mode = "AUTO"

    auth_ctrl, _, webhook_url = _setup_and_login()
    response = buy_lotto645(auth_ctrl, count, mode) 
    send_message(1, response=response, webhook_url=webhook_url)

def run():
    if len(sys.argv) < 2:
        print("Usage: python controller.py [buy|check]")
        return

    cmd = sys.argv[1]
    if cmd in ["buy", "buy_lotto"]:
        buy()
    elif cmd in ["check", "check_lotto"]:
        check()

if __name__ == "__main__":
    run()
