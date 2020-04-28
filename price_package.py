from bs4 import BeautifulSoup
import asyncio
import httpx
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.applications import Starlette


url_btc = 'https://coinmarketcap.com/currencies/bitcoin/'
url_xlm = 'https://coinmarketcap.com/currencies/stellar/'
url_xrp = 'https://coinmarketcap.com/currencies/xrp/'
url_gld = 'https://www.kitco.com/gold-price-today-usa/'
url_usd = 'https://transferwise.com/pl/currency-converter/usd-to-pln-rate'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.117 Safari/537.36'}


async def get_url(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


async def check_price_btc():
    soup = await get_url(url_btc)
    price_btc = soup.find(class_='cmc-details-panel-price__price').get_text()
    price_btc = price_btc.replace(',','')
    converted_price_btc = float(price_btc[1:])
    converted_price_btc = round(converted_price_btc,3)
    print(converted_price_btc)
    return converted_price_btc


async def check_price_xrp():
    soup = await get_url(url_xrp)
    price_xrp = soup.find(class_='cmc-details-panel-price__price').get_text()
    price_xrp = price_xrp.replace(',','')
    converted_price_xrp = float(price_xrp[1:])
    converted_price_xrp = round(converted_price_xrp,3)
    print(converted_price_xrp)
    return converted_price_xrp


async def check_price_xlm():
    soup = await get_url(url_xlm)
    price_xlm = soup.find(class_='cmc-details-panel-price__price').get_text()
    price_xlm = price_xlm.replace(',','')
    converted_price_xlm = float(price_xlm[1:])
    converted_price_xlm = round(converted_price_xlm,3)
    print(converted_price_xlm)
    return converted_price_xlm


async def check_price_gld():
    soup = await get_url(url_gld)
    price_gld = soup.find(class_='table-price--body-table--overview-bid').get_text()
    price_gld = price_gld[5:13].replace(',', '')
    converted_price_gld = float(price_gld[:])
    converted_price_gld = round(converted_price_gld,3)
    print(converted_price_gld)
    return converted_price_gld

async def check_price_usd():
    soup = await get_url(url_usd)
    price_usd = soup.find(class_='text-success').get_text()
    price_usd = price_usd.replace(',','.')
    converted_price_usd = float(price_usd)
    converted_price_usd = round(converted_price_usd,3)
    return converted_price_usd


# def async_prices():
#     many = asyncio.gather(check_price_btc(),check_price_xrp(),check_price_xlm(),check_price_gld())
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(many)


async def check_prices(request):
    prices = await asyncio.gather(check_price_btc(), check_price_xrp(), check_price_xlm(), check_price_gld(),
                                  check_price_usd())
    print(prices)
    return JSONResponse({'BTC':prices[0],'XRP':prices[1],'XLM':prices[2],'GLD':prices[3],'USD':prices[4]})

routes = [Route('/', check_prices)]

app = Starlette(debug=True, routes=routes)