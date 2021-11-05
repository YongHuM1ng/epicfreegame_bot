from hoshino import Service
from PIL import Image
from io import BytesIO
import requests
import time
import os
import base64

sv = Service('epic喜加一')

FILE_PATH = os.path.dirname(__file__)


def imgtobase64(url: str):
    r = requests.get(url)
    open(FILE_PATH + '/temp.jpg', 'wb').write(r.content)
    image = Image.open(os.path.join(FILE_PATH, 'temp.jpg'))
    bio = BytesIO()
    image.save(bio, format='JPEG')
    base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()
    return f"[CQ:image,file={base64_str}]"


def datetranslate(date):
    return time.strftime('%m{m}%d{d}%H:%M', time.localtime(time.mktime(time.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')) + 28800)).format(m='月', d='日')


@sv.on_rex('epic免费游戏')
async def epic(bot, ev):
    url = 'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=zh-CN&country=CN&allowCountries=CN'
    r = requests.get(url, verify=False)
    r.raise_for_status()
    r.encoding = 'utf-8'
    data = r.json()['data']['Catalog']['searchStore']['elements']
    for i in range(len(data)):
        if data[i]['promotions'] is not None and len(data[i]['promotions']['promotionalOffers']) != 0:
            endDate = datetranslate(data[i]['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'])
            img = imgtobase64(data[i]['keyImages'][2]['url'])
            msg = data[i]['title'] + '\n截止时间：' + endDate + '\n─────────────\n' + img + '\n' + data[i]['description'] + '\n─────────────\nhttps://www.epicgames.com/store/zh-CN/p/' + data[i]['urlSlug']
            await bot.send(ev, msg)
            # elif len(data[i]['promotions']['upcomingPromotionalOffers']) != 0:
            #     startDate = data[i]['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['startDate']
            #     endDate = data[i]['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['endDate']
            #     startDate = time.localtime(time.mktime(time.strptime(startDate, '%Y-%m-%dT%H:%M:%S.000Z')) + 28800)
            #     endDate = time.localtime(time.mktime(time.strptime(endDate, '%Y-%m-%dT%H:%M:%S.000Z')) + 28800)
            #     startDate = time.strftime('%m{m}%d{d}', startDate).format(m='月', d='日')
            #     endDate = time.strftime('%m{m}%d{d}', endDate).format(m='月', d='日')
            #     msg = msg + data[i]['title'] + '\n免费 ' + startDate + ' - ' + endDate + '\n'
