import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
from datetime import datetime
from config import token

rec = requests.get('https://yobit.net/api/3/ticker/btc_usd')

response = rec.json()
prise = response['btc_usd']['sell']
prise_high = response['btc_usd']['high']
prise_low = response['btc_usd']['low']

r = requests.get('https://myfin.by/currency/minsk')

soup = BeautifulSoup(r.text, "html.parser")
s = []
def get_kurs():
    item_usd = soup.find('tbody').find('tr')
    item_eur = soup.find('tbody').find('tr').next_sibling
    item_rub = soup.find('tbody').find('tr').next_sibling.next_sibling

    for i in item_usd:
        s.append(i.text)

    for i in item_eur:
        s.append(i.text)

    for i in item_rub:
        s.append(i.text)

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    def create_keyboard():
        keyboard = types.InlineKeyboardMarkup()
        usd_btn = types.InlineKeyboardButton(text="Доллар", callback_data='1')
        eur_btn = types.InlineKeyboardButton(text="Евро", callback_data='2')
        rub_btn = types.InlineKeyboardButton(text="Российский рубль", callback_data='3')
        bitcoin_btn = types.InlineKeyboardButton(text="Bitcoin", callback_data='4')
        bank_btn = types.InlineKeyboardButton(text="Банки", callback_data='5')

        keyboard.add(usd_btn, eur_btn)
        keyboard.row(rub_btn, bitcoin_btn)
        keyboard.add(bank_btn)
        return keyboard

    @bot.message_handler(commands=['start'])
    def start_message(message):
        mass = f'Привет, <b>{message.from_user.first_name}</b>!\nЗдесь ты можешь узнать лучший курс валют в Минске на: {soup.sup.text[:5]} и еще что-нибудь...\n Выбирай,что ты хочешь узнать :-)'
        keyboard = create_keyboard()
        bot.send_message(message.chat.id, mass, parse_mode='html', reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        if call.message:
            keyboard = create_keyboard()
            if call.data == "1":
                    bot.send_message(call.message.chat.id, f'{s[0]}\nпокупка {s[1]}   продажа {s[2]}   НБРБ {s[3]}', reply_markup=keyboard)
            if call.data == "2":
                    bot.send_message(call.message.chat.id, f'{s[5]}\nпокупка {s[6]}   продажа {s[7]}   НБРБ {s[8]}', reply_markup=keyboard)
            if call.data == "3":
                    bot.send_message(call.message.chat.id, f'{s[10]}\nпокупка {s[11]}   продажа {s[12]}   НБРБ {s[13]}', reply_markup=keyboard)
            if call.data == "4":
                    bot.send_message(call.message.chat.id, f'{datetime.now().strftime("%Y-%m-%d %H:%M")}\nSELL: btc_usd {prise}\nHIGH: {prise_high}\nLOW: {prise_low}',reply_markup=keyboard)
            if call.data == "5":
                    bot.send_message(call.message.chat.id, f'https://myfin.by/currency/minsk?working=1', reply_markup=keyboard)
    bot.polling()

if __name__ == '__main__':
    get_kurs()
    telegram_bot(token)
