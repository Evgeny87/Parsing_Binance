import requests
import pandas as pd
import time


def zapros():
    data = {
      "asset": "USDT",
      "fiat": "RUB",
      "merchantCheck": False,
      "page": 1,
      "payTypes": [],
      "publisherType": None,
      "rows": 5,
      "tradeType": "SELL"
    }

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "123",
        "content-type": "application/json",
        "Host": "p2p.binance.com",
        "Origin": "https://p2p.binance.com",
        "Pragma": "no-cache",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    return data, headers


def url_to_parse(url_site=""):
    while True:
        data, headers = zapros()
        try:
            response = requests.post(url_site,
                                     headers=headers, json=data)
            response.raise_for_status()
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            print("Ошибка timeout, url:", url_site)
        except requests.exceptions.URLRequired as errur:
            print("URLRequired Error:", errur)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            code = errh.response.status_code
            print("Ошибка url: %url_site, code: %code", url_site, code)
            print("Connection Error: ", code)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            print("Ошибка скачивания url: ", url_site)
        else:
            json_response = response.json()
            break
    return json_response, response.status_code


def new_dict():
    data = {}
    price = "price"
    key, value = price, []
    data[key] = value
    surplusAmount = "surplusAmount"
    key, value = surplusAmount, []
    data[key] = value
    maxSingleTransAmount = "maxSingleTransAmount"
    key, value = maxSingleTransAmount, []
    data[key] = value
    minSingleTransAmount = "minSingleTransAmount"
    key, value = minSingleTransAmount, []
    data[key] = value
    nickName = "nickName"
    key, value = nickName, []
    data[key] = value
    monthOrderCount = "monthOrderCount"
    key, value = monthOrderCount, []
    data[key] = value
    monthFinishRate = "monthFinishRate"
    key, value = monthFinishRate, []
    data[key] = value
    return data


def sborka(url=""):
    json_response, status_code = url_to_parse(url)
    data = new_dict()

    len_json_response_data = len(json_response["data"])
    for i in range(len_json_response_data):
        price = json_response["data"][i]["adv"]["price"]
        data["price"].append(price)
        surplusAmount = json_response["data"][i]["adv"]["surplusAmount"]
        data["surplusAmount"].append(surplusAmount)
        maxSingleTransAmount = json_response["data"][i]["adv"]["maxSingleTransAmount"]
        data["maxSingleTransAmount"].append(maxSingleTransAmount)
        minSingleTransAmount = json_response["data"][i]["adv"]["minSingleTransAmount"]
        data["minSingleTransAmount"].append(minSingleTransAmount)
        nickName = json_response["data"][i]["advertiser"]["nickName"]
        data["nickName"].append(nickName)
        monthOrderCount = json_response["data"][i]["advertiser"]["monthOrderCount"]
        data["monthOrderCount"].append(monthOrderCount)
        monthFinishRate = json_response["data"][i]["advertiser"]["monthFinishRate"]
        data["monthFinishRate"].append(monthFinishRate * 100)

    df = pd.DataFrame(data)
    df.to_csv("pandas0001.csv", sep=';', encoding='utf-8-sig', index=False)
    df.to_json("pandas0001.json", orient='index')
    
    del df


def main():
    url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
    print("Для остановки нажмите CTRL+C")
    while True:
        sborka(url)
        time.sleep(10)


if __name__ == "__main__":
        main()
