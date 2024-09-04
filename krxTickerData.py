from pykrx.website import krx
import datetime
from pandas import DataFrame
import re

yymmdd = re.compile(r"\d{4}[-/]?\d{2}[-/]?\d{2}")


def get_future_ticker_list() -> list:
    """티커 목록 조회

    Args: None

    Returns:
        list: 티커가 담긴 리스트

        > get_future_ticker_list()

        ['KRDRVFUK2I', 'KRDRVFUMKI', 'KRDRVOPK2I', 'KRDRVOPWKI', 'KRDRVOPMKI', 'KRDRVFUKQI', 'KRDRVOPKQI', 'KRDRVFUXI3', 'KRDRVFUVKI', 'KRDRVFUXAT', 'KRDRVFUBM3', 'KRDRVFUBM5', 'KRDRVFUBMA', 'KRDRVFURFR', 'KRDRVFUUSD', 'KRDRVFXUSD', 'KRDRVFUJPY', 'KRDRVFUEUR', 'KRDRVFUCNH', 'KRDRVFUKGD', 'KRDRVFUEQU', 'KRDRVOPEQU', 'KRDRVFUEST']
    """  # pylint: disable=line-too-long # noqa: E501

    return krx.get_future_ticker_list()


def get_future_ticker_name(ticker: str) -> str:
    """티커에 대응되는 종목 이름 반환

    Args:
        ticker (str): 티커

    Returns:
        str: 종목명

        > get_future_ticker_name('KRDRVFUEST')

        EURO STOXX50 Futures
    """
    return krx.get_future_ticker_and_name()

tickers = get_future_ticker_list()
print(tickers)

names = get_future_ticker_name(tickers)
print(names)
