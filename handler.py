import json
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List


BASE_URL = 'https://api.clashroyale.com/v1'
ACCESS_KEY = os.environ['CR_ACCESS_KEY']


def init_headers() -> Dict[str, str]:
    """
    初期化されたヘッダー情報の辞書を返す

    Returns
    -------
    dict
        header情報
    """
    return {
        'content-type': 'application/json; charset=utf-8',
        'cache-control': 'max-age=60',
        'authorization': f'Bearer {ACCESS_KEY}',
    }


def get_member(clan_tag: str) -> Dict[str, str]:
    """
    クラロワAPIからclan_tagのメンバー情報をGETする

    Parameters
    ----------
    clan_tag : str
        クランタグ (ex. #228UCY92)

    Returns
    -------
    dict
        APIのレスポンス
    """
    url = BASE_URL + f'/clans/{clan_tag}/members'
    headers = init_headers()

    res = requests.get(url, headers=headers)

    return res.json()


def filter_by_last_seen(items: List[dict], dead_line: datatime) -> List[dict]:
    """
    最終ログインがdead_lineのクラメンの情報を抽出する

    Parameters
    ----------
    items : List[dict]
        クランメンバーの情報のリスト

    dead_line : datetime
        最終ログインのデッドライン

    Returns
    -------
    List[dict]
        dead_lineを超えてしまったクラメンの情報のリスト
    """
    before_last_seen = lambda i: datetime.strptime(i['lastSeen'], '%Y%m%dT%H%M%S.000Z') < dead_line

    return [item for item in items if before_last_seen(item)]


def lambda_function(event, context) -> Dict[str, str]:
    """
    実行用の関数

    Parameters
    ----------
    event : list
        入力パラメータ
    context : list
        よくわからん

    Returns
    -------
    data : dict
        結果
    """
    data = get_member('#228UCY92')
    dead_line = datetime.now() - timedelta(days=7)
    filtered_data = filter_by_last_seen(data, dead_line)

    return dead_line
