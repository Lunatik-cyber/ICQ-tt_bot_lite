# Developer: https://github.com/Lunatik-cyber
# Telegram: @Lunatik_cyber
# Donate:
#   BTC: bc1q9qtm3vlq6kwz0lu29d9hn3yph9l900wq6hkwhr
#   ETH: 0xD1Ed6545257dC6D7B84211Aa4ffaDD52F271ce1F
#   TRX: TCCCaKnky8gu7XXZpvtLQsTqwLkDv3cNbb
#   USDT (TRC20): TCCCaKnky8gu7XXZpvtLQsTqwLkDv3cNbb
#   USDT (ERC20): 0xD1Ed6545257dC6D7B84211Aa4ffaDD52F271ce1F

import os
import random

import requests
from bot.bot import Bot
from bot.handler import MessageHandler

TOKEN = ""  # bot token

bot = Bot(token=TOKEN)


def get_download_links(video_url, event):
    r = requests.get(f'https://api.douyin.wtf/api?url={video_url}').json()
    if r["status"] == "success":
        filename = f'tt-{random.randint(1, 9999999999)}.mp4'
        file = open(filename, 'wb')
        video_url = r["nwm_video_url"]
        video_r = requests.get(video_url, stream=True)
        file.write(video_r.content)  # записываем содержимое в файл
        file.close()
        file = open(filename, 'rb')
        response = bot.send_file(chat_id=event.from_chat, file=file.read())
        file.close()
        file_id = response.json()['fileId']
        print(file_id)
        os.remove(filename)
        return filename
    return None, None


def message_cb(bot, event):
    print(event.text, event.from_chat)
    if event.text.startswith(
            ('/tt https://www.tiktok.com', '/tt http://www.tiktok.com', '/tt https://vm.tiktok.com',
             '/tt http://vm.tiktok.com', '/tt https://vt.tiktok.com', '/tt http://vt.tiktok.com')):
        bot.send_text(chat_id=event.from_chat, text='Скачиваю...')
        video_url = f'{event.text}'.replace('/tt ', '')
        get_download_links(video_url, event)


def message_start(bot, event):
    print(event.text, event.from_chat)
    if event.text.startswith('/start'):
        bot.send_text(chat_id=event.from_chat, text='Бот для скачивания видео с платформы TikTok.\n\n'
                                                    'Доступные команды:\n'
                                                    '   /tt <ссылка на видео>\n')


if __name__ == '__main__':
    bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
    bot.dispatcher.add_handler(MessageHandler(callback=message_start))
    bot.start_polling()
    bot.idle()
