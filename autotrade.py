import time
import pyupbit
import datetime

access = "your-access"
secret = "your-secret"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 매수 정보 초기화
buy_price = None
sell_price = None

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        target_price = get_target_price("KRW-BTC", 0.5)
        current_price = get_current_price("KRW-BTC")

        # 매수 시도
        if buy_price is None and target_price < current_price:
            krw = get_balance("KRW")
            if krw > 5000:
                buy_price = current_price
                upbit.buy_market_order("KRW-BTC", krw*0.9995)
        # 매도 시도
        else:
            if buy_price is not None:
                current_price = get_current_price("KRW-BTC")
                if current_price >= buy_price * 1.1 and sell_price is None:
                    sell_price = current_price
                if current_price <= buy_price * 0.95:
                    sell_price = current_price
                if sell_price is None and (current_price >= buy_price * 1.1 or current_price <= buy_price * 0.95):
                    btc = get_balance("BTC")
                    if btc > 0.00008:
                        sell_price = current_price
                        buy_price = None
                        upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)