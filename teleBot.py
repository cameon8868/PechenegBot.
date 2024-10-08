import datetime
import itertools
import random
import sqlite3
import telebot
import time
from telebot import types

way = 'C:/Users/User/PycharmProjects/'

conn = sqlite3.connect("telegramBot/db/database", check_same_thread=False)
cursor = conn.cursor()
output = []

def db_table_val(user_id_sql: int, user_name_sql: str, pts_sql: int, last_time: time, card_coll: int):
        cursor.execute('INSERT INTO User (user_id_sql, user_name_sql, pts_sql, last_time, card_coll) VALUES (?, ?, ?, ?, ?)',
                       (user_id_sql, user_name_sql, pts_sql,last_time, card_coll))

def db_table_Card(name_card: str, rarity: str, avatar_card: str, pts_card: int):
    cursor.execute('INSERT INTO Cards (name_card, rarity, avatar_card, pts_card) VALUES (?, ?, ?,?)',
                   (name_card, rarity, avatar_card, pts_card))

def db_table_Collection(user_id_ss: int, card_id: str, rarity: str):
    cursor.execute('INSERT INTO collection (user_id_ss, card_id, rarity) VALUES (?, ?, ?)',
                   (user_id_ss, card_id, rarity))

def db_table_promo(user_id: int, UseOrNeuse: int):
    cursor.execute('INSERT INTO promo (user_id, UseOrNeuse) VALUES (?, ?)', (user_id, UseOrNeuse))
conn.commit()


Card_list = 'SELECT name_card, rarity, avatar_card FROM Cards'
cursor.execute(Card_list)
rec_Card_list = cursor.fetchall()


time.sleep(5)
bot = telebot.TeleBot('TOKEN')




itembtn1 = types.KeyboardButton('💅' + 'получить карту')
itembtn2 = types.KeyboardButton( '🃏'+ 'мои карты')
itembtn3 = types.KeyboardButton( '⚙️' + 'настройки')
itembtn4 = types.KeyboardButton( '🥇'+ 'рейтинг')

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    mess = (f'<b>{message.from_user.first_name}</b>, добро пожаловать в \n'
            f'Card Pecheneg Bot! \n<a href="https://t.me/Cameon_projects">канал с новостями</a>\n'
            f'\n'
            f'\n'
            f'по всем вопросам писать:\n '
            f'@cammeon \n '
            f'@slepaa')

    markup = types.ReplyKeyboardMarkup(row_width=1)

    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    bot.send_message(message.chat.id, mess, parse_mode='html')

    info_user_to = cursor.execute("SELECT * FROM User WHERE user_id_sql = " + str(user_id)).fetchall()

    if len(info_user_to) > 0:
                bot.send_message(message.chat.id, 'вы уже зарегистрированы', parse_mode='html', reply_markup=markup)

    else:

                bot.send_message(message.chat.id, 'Добро Пожаловать!', parse_mode='html', reply_markup=markup)

                us_id_sql = message.from_user.id
                us_name_sql = message.from_user.first_name
                pts_sq = 100
                last_time = datetime.datetime.now()
                db_table_val(user_id_sql=us_id_sql, user_name_sql=us_name_sql, pts_sql=pts_sq, last_time=last_time, card_coll=2)
                db_table_promo(user_id=user_id, UseOrNeuse=2)




    conn.commit()


@bot.message_handler()
def get_user_text(message):
    user_id = message.from_user.id
    current_time = datetime.datetime.now()

    '''поинты игроков'''
    point = 'SELECT user_id_sql, pts_sql FROM User'
    cursor.execute(point)
    rec = cursor.fetchall()
    rec_list = list(sum(rec, ()))
    d = dict(itertools.zip_longest(*[iter(rec_list)] * 2, fillvalue=""))
    cash = d.get(user_id, None)





    cursor.execute('SELECT last_time FROM User WHERE user_id_sql = ?', (user_id,))
    conn.commit()
    last_time = cursor.fetchone()
    cursor.execute('SELECT card_coll FROM User WHERE user_id_sql = ?', (user_id,))
    conn.commit()
    card_coll = cursor.fetchone()

    if message.text.lower() == 'получить карту' or message.text == '💅' +'получить карту':
            try:
                TimeCard = 7200
                time = (current_time - datetime.datetime.fromisoformat(last_time[0])).seconds
                card_kd = card_coll[0]


                if time >= TimeCard or card_kd > 1:
                        cursor.execute('UPDATE User SET last_time = ? WHERE user_id_sql = ?', (current_time, user_id))
                        cursor.execute("UPDATE User SET card_coll = card_coll - 1 WHERE user_id_sql = ?",(user_id,))
                        randomcard = random.randint( 0, 107)

                        if randomcard in range(1, 2):
                            randPlayerCharacter = rec_Card_list[0]
                            if randPlayerCharacter[0] in rec_list:
                                pts_sql = 750
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[
                                    2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'💎<b>{randPlayerCharacter[0]}</b> \n♻️Попалась  повторка, тебе будут начислены только очки за карту\n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')

                            else:
                                pts_sql = 1500
                                db_table_Collection(user_id_ss=user_id, card_id=randPlayerCharacter[0],
                                                    rarity=randPlayerCharacter[1])
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[
                                    2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'💎<b>{randPlayerCharacter[0]}</b>\n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')



                        elif randomcard in range(3, 12):
                            randIndex = random.randrange(1, 15)
                            randPlayerCharacter = rec_Card_list[randIndex]
                            if randPlayerCharacter[0] in rec_list:
                                pts_sql = 250
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[
                                    2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'⭐️<b>{randPlayerCharacter[0]}</b> \n♻️Попалась  повторка, тебе будут начислены только очки за карту\n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')

                            else:
                                pts_sql = 500
                                db_table_Collection(user_id_ss=user_id, card_id=randPlayerCharacter[0],
                                                    rarity=randPlayerCharacter[1])
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[
                                    2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'⭐️<b>{randPlayerCharacter[0]}</b>\n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')




                        elif randomcard in range(12, 33):
                            randIndex = random.randrange(16, 22)
                            randPlayerCharacter = rec_Card_list[randIndex]
                            a = cursor.execute("SELECT card_id FROM collection WHERE user_id_ss = ?", (user_id,))
                            rec = a.fetchall()
                            rec_list = [row[0] for row in rec]

                            if randPlayerCharacter[0] in rec_list:
                                pts_sql = 125
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[
                                    2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'🔥<b>{randPlayerCharacter[0]}</b> \n♻️Попалась  повторка, тебе будут начислены только очки за карту\n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')

                            else:
                                pts_sql = 250
                                db_table_Collection(user_id_ss=user_id, card_id=randPlayerCharacter[0],
                                                    rarity=randPlayerCharacter[1])
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[
                                    2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'🔥<b>{randPlayerCharacter[0]}</b>\n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')





                        elif randomcard in range(33, 64):
                            randIndex = random.randrange(23, 26)
                            randPlayerCharacter = rec_Card_list[randIndex]

                            a = cursor.execute("SELECT card_id FROM collection WHERE user_id_ss = ?", (user_id,))
                            rec = a.fetchall()
                            rec_list = [row[0] for row in rec]

                            if randPlayerCharacter[0] in rec_list:
                                pts_sql = 50
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[
                                    2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'⚡️<b>{randPlayerCharacter[0]}</b>\n♻️Попалась  повторка, тебе будут начислены только очки за карту\n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')

                            else:
                                pts_sql = 100
                                db_table_Collection(user_id_ss=user_id, card_id=randPlayerCharacter[0],
                                                    rarity=randPlayerCharacter[1])
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'⚡️<b>{randPlayerCharacter[0]}</b>\n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')






                        elif randomcard in range(64, 106):
                            randIndex = random.randrange(26, 40)
                            randPlayerCharacter = rec_Card_list[randIndex]

                            a = cursor.execute("SELECT card_id FROM collection WHERE user_id_ss = ?",(user_id,))
                            rec =a.fetchall()
                            rec_list = [row[0] for row in rec]


                            if randPlayerCharacter[0] in rec_list:
                                pts_sql = 25
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'💫<b>{randPlayerCharacter[0]}</b> \n♻️Попалась  повторка, тебе будут начислены только очки за карту\n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')

                            else:
                                pts_sql = 50
                                db_table_Collection(user_id_ss = user_id, card_id=randPlayerCharacter[0], rarity=randPlayerCharacter[1])
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'💫<b>{randPlayerCharacter[0]}</b>\n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')








                        elif randomcard in range(106, 107):
                            randIndex = random.randrange(41, 44)
                            randPlayerCharacter = rec_Card_list[randIndex]

                            a = cursor.execute("SELECT card_id FROM collection WHERE user_id_ss = ?", (user_id,))
                            rec = a.fetchall()
                            rec_list = [row[0] for row in rec]

                            if randPlayerCharacter[0] in rec_list:
                                pts_sql = 2500
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[
                                    2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'🧩<b>{randPlayerCharacter[0]}</b> \n♻️Попалась  повторка, тебе будут начислены только очки за карту \n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')

                            else:
                                pts_sql = 5000
                                db_table_Collection(user_id_ss=user_id, card_id=randPlayerCharacter[0],
                                                    rarity=randPlayerCharacter[1])
                                cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?",
                                               (pts_sql, user_id))
                                card_avatar = "telegramBot/avatar/" + randPlayerCharacter[
                                    2]
                                bot.send_photo(message.chat.id, open(card_avatar, 'rb'),
                                               caption=f'🧩<b>{randPlayerCharacter[0]}</b>\n\n'
                                                       f'🎰Редкость: {randPlayerCharacter[1]}\n'
                                                       f'💰Количество pts: {cash - 100 + pts_sql}', parse_mode='html')
                else:
                        convert = str(datetime.timedelta(seconds = TimeCard - time))
                        bot.send_message(message.chat.id,
                                                 f'❌<b>СЛИШКОМ РАНО</b> \n'
                                                 f'🕓Карту можно получить через:<b> {convert}</b>',
                                                 parse_mode='html')

            except:
                        bot.send_message(message.chat.id, 'eror 404', parse_mode='html')



    elif message.text.lower() == 'мои карты' or message.text == '🃏' +'мои карты':
        # try:
        cursor.execute("SELECT DISTINCT user_id_ss, card_id, rarity FROM collection WHERE user_id_ss = ?", (user_id,))
        a = cursor.fetchall()
        indexPressF = 0
        indexCardMif = 0
        indexCardLeg = 0
        indexCardEpic = 0
        indexCardRary = 0
        indexCardDefolt = 0
        for row in a:
                if row[0] == user_id:
                    if row[2] == 'Мифическая':
                        indexCardMif += 1
                    elif row[2] == 'Легендарная':
                        indexCardLeg += 1
                    elif row[2] == 'Эпическая':
                        indexCardEpic += 1
                    elif row[2] == 'Редкая':
                        indexCardRary += 1
                    elif row[2] == 'Обычная':
                        indexCardDefolt += 1
                    elif row[2] == 'Мертвая легенда':
                        indexPressF += 1

                elif row[0] != user_id:
                    break


        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        pressF = types.InlineKeyboardButton(text=f'🧩Мёртвые легенды - {indexPressF}/4', callback_data='PressF')
        mif = types.InlineKeyboardButton(text=f'💎Мифические - {indexCardMif}/1', callback_data='mif')
        Leg = types.InlineKeyboardButton(text=f'⭐️Легендарные - {indexCardLeg}/14', callback_data='Leg')
        epic = types.InlineKeyboardButton(text=f'️🔥Эпические - {indexCardEpic}/7', callback_data='epic')
        rary = types.InlineKeyboardButton(text=f'️⚡️Редкие - {indexCardRary}/4', callback_data='rary')
        defolt = types.InlineKeyboardButton(text=f'💫Обычные - {indexCardDefolt}/14', callback_data='defolt')
        full = types.InlineKeyboardButton(text=f'🃏все карты - {indexCardMif+indexCardDefolt+indexCardRary+indexCardLeg+indexCardEpic+indexPressF}/44', callback_data='full')
        markup_inline.add(pressF, mif, Leg, epic, rary, defolt, full)


        bot.send_message(message.chat.id, f'💬 {message.from_user.first_name}, какие карты хочешь просмотреть?:\n' , parse_mode='html', reply_markup=markup_inline)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            if call.data == 'PressF':
                user_name = call.from_user.first_name
                user_id_ss = call.from_user.id
                cursor.execute("SELECT DISTINCT user_id_ss, card_id, rarity FROM collection WHERE user_id_ss = ?",
                               (user_id_ss,))
                a = cursor.fetchall()
                list_card = ''
                for row in a:
                    if row[0] == user_id_ss and row[2] == 'Мертвая легенда':
                        list_card += f'🧩{row[1]}\n'
                    elif row[0] != user_id_ss:
                        break
                if list_card == '':
                    bot.edit_message_text("Нет карт такой редкости", call.message.chat.id, call.message.message_id)
                else:
                    bot.edit_message_text(f'Мертвые легенды карты {user_name}:\n{list_card}', call.message.chat.id, call.message.message_id)
            elif call.data == 'mif':
                user_name = call.from_user.first_name
                user_id_ss = call.from_user.id

                cursor.execute("SELECT DISTINCT user_id_ss, card_id, rarity FROM collection WHERE user_id_ss = ?",
                               (user_id_ss,))
                a = cursor.fetchall()
                list_card = ''
                for row in a:
                    if row[0] == user_id_ss and row[2] == 'Мифическая':
                        list_card += f'💎{row[1]}\n'
                    elif row[0] != user_id_ss:
                        break
                if list_card == '':
                    bot.edit_message_text("Нет карт такой редкости", call.message.chat.id, call.message.message_id)
                else:
                    bot.edit_message_text(f'Мифические карты {user_name}:\n{list_card}', call.message.chat.id, call.message.message_id)
            elif call.data == 'Leg':
                user_name = call.from_user.first_name
                user_id_ss = call.from_user.id
                cursor.execute("SELECT DISTINCT user_id_ss, card_id, rarity FROM collection WHERE user_id_ss = ?",
                               (user_id_ss,))
                a = cursor.fetchall()
                list_card = ''
                for row in a:
                    if row[0] == user_id_ss and row[2] == 'Легендарная':
                        list_card += f'⭐️{row[1]}\n'
                    elif row[0] != user_id_ss:
                        break
                if list_card == '':
                    bot.edit_message_text("Нет карт такой редкости", call.message.chat.id, call.message.message_id)
                else:
                    bot.edit_message_text(f'Легендарные карты {user_name}:\n{list_card}', call.message.chat.id, call.message.message_id)
            elif call.data == 'epic':
                user_name = call.from_user.first_name
                user_id_ss = call.from_user.id
                cursor.execute("SELECT DISTINCT user_id_ss, card_id, rarity FROM collection WHERE user_id_ss = ?",
                               (user_id_ss,))
                a = cursor.fetchall()
                list_card = ''
                for row in a:
                    if row[0] == user_id_ss and row[2] == 'Эпическая':

                        list_card += f'🔥{row[1]}\n'
                    elif row[0] != user_id_ss:
                        break
                if list_card == '':
                    bot.edit_message_text("Нет карт такой редкости", call.message.chat.id, call.message.message_id)
                else:
                    bot.edit_message_text(f'Эпические карты {user_name}:\n{list_card}', call.message.chat.id, call.message.message_id)

            elif call.data == 'rary':
                user_name = call.from_user.first_name
                user_id_ss = call.from_user.id
                cursor.execute("SELECT DISTINCT user_id_ss, card_id, rarity FROM collection WHERE user_id_ss = ?",
                               (user_id_ss,))
                a = cursor.fetchall()
                list_card = ''
                for row in a:
                    if row[0] == user_id_ss and row[2] == 'Редкая':
                        list_card += f'⚡️{row[1]}\n'
                    elif row[0] != user_id_ss:
                        break
                if list_card == '':
                    bot.edit_message_text("Нет карт такой редкости", call.message.chat.id, call.message.message_id)
                else:
                    bot.edit_message_text(f'Редкие карты {user_name}:\n{list_card}', call.message.chat.id, call.message.message_id)

            elif call.data == 'defolt':
                user_id_ss = call.from_user.id
                user_name = call.from_user.first_name
                cursor.execute("SELECT DISTINCT user_id_ss, card_id, rarity FROM collection WHERE user_id_ss = ?", (user_id_ss,))
                a = cursor.fetchall()
                list_card = ''
                for row in a:

                    if row[0] == user_id_ss and row[2] == 'Обычная':
                        list_card += f'💫{row[1]}\n'
                    elif row[0] != user_id_ss:
                        break
                if list_card == '':
                    bot.edit_message_text("Нет карт такой редкости", call.message.chat.id, call.message.message_id)
                else:
                    bot.edit_message_text(f'Обычные карты {user_name}:\n{list_card}', call.message.chat.id, call.message.message_id)

            elif call.data == 'full':
                pass



                markup_inline = types.InlineKeyboardMarkup(row_width=1)
                pressF = types.InlineKeyboardButton(text=f'🧩Мёртвые легенды - {indexPressF}/4', callback_data='PressF')
                mif = types.InlineKeyboardButton(text=f'💎Мифические - {indexCardMif}/1', callback_data='mif')
                Leg = types.InlineKeyboardButton(text=f'⭐️Легендарные - {indexCardLeg}/14', callback_data='Leg')
                epic = types.InlineKeyboardButton(text=f'️🔥Эпические - {indexCardEpic}/7', callback_data='epic')
                rary = types.InlineKeyboardButton(text=f'️⚡️Редкие - {indexCardRary}/4', callback_data='rary')
                defolt = types.InlineKeyboardButton(text=f'💫Обычные - {indexCardDefolt}/14', callback_data='defolt')
                full = types.InlineKeyboardButton(
                    text=f'🃏все карты - {indexCardMif + indexCardDefolt + indexCardRary + indexCardLeg + indexCardEpic + indexPressF}/44',
                    callback_data='full')
                markup_inline.add(pressF, mif, Leg, epic, rary, defolt, full)

                bot.edit_message_text(f'💬 {message.from_user.first_name}, какие карты хочешь просмотреть?:\n', call.message.chat.id, call.message.message_id,
                                      reply_markup=markup_inline, parse_mode='html')







    elif message.text.lower() == 'настройки' or message.text == '⚙️' +'настройки':
        try:
            bot.send_message(message.chat.id, f'🎮 Твой ник: {message.from_user.first_name} \n'
                                          f'🌐 Твой aйди: {message.from_user.id}\n'
                                          f'🗓 Дата регистрации: {datetime.datetime.fromisoformat(last_time[0]).strftime("%d.%m.20%yг в %H:%M")}\n'
                                          f'💰Количество pts: {cash-100}\n'
                                          f'🌀Количество круток: {card_coll[0] - 1}\n'
                                          f'❓Помощь\n⚡️  @cammeon\n👨‍🦯  @slepaa', parse_mode='html')
        except:
            bot.send_message(message.chat.id, 'eror 404', parse_mode='html')



    elif message.text.lower() == 'рейтинг' or message.text == '🥇' +'рейтинг':
        # try:
            top = 'SELECT user_id_sql, pts_sql, user_name_sql FROM User'
            cursor.execute(top)
            rec_top = cursor.fetchall()
            rec_top.sort(key=lambda x: x[1], reverse=True)
            msg = ''
            count = 9
            id = 0

            for i in rec_top:
                if id <= count:
                    id += 1
                    msg += f'{id}. <a href="tg://user?id={i[0]}">{i[2]}</a> - {i[1]-100} pts\n'
                else:
                    break
            bot.send_message(message.chat.id,f'🎯Таблица лидеров:\n{msg}', parse_mode='html')

        # except:
        #     bot.send_message(message.chat.id, 'вы не зарегистрированы', parse_mode='html')

    elif message.text.lower() == '!промокод slepapitar' or message.text.lower() == '.промокод slepapitar':
        try:
            cursor.execute('SELECT user_id, UseOrNeuse FROM promo WHERE user_id = ?', (user_id,))
            promo = cursor.fetchall()
            for i in promo:
                if i[1] > 1:
                    bot.send_message(message.chat.id, '🎁успешно введен промокод!', parse_mode='html')
                    cursor.execute("UPDATE User SET card_coll = card_coll + 3 WHERE user_id_sql = ?", (user_id,))
                    cursor.execute("UPDATE promo SET UseOrNeuse = UseOrNeuse - 1 WHERE user_id = ?", (user_id,))
                else:
                    bot.send_message(message.chat.id, '❌вы уже использовали промокод, извиняй.', parse_mode='html')

        except:
            bot.send_message(message.chat.id, 'eror 404', parse_mode='html')

    elif message.text.lower() == '.state':
        '''всего игроков'''
        top = 'SELECT * FROM User'
        cursor.execute(top)
        rec_top = cursor.fetchall()
        rec_top.sort(key=lambda x: x[0], reverse=True)
        a = ''
        for i in rec_top:
            a += str(i[0])
            break

        '''активных игроков: больше 500 птс'''
        active = 'SELECT user_id_sql FROM User WHERE pts_sql >= 2000'
        cursor.execute(active)
        rec_active = cursor.fetchall()
        h = 0
        for e in rec_active:
            h += 1



        bot.send_message(message.chat.id, f'Статистика бота:\nвсего игроков: {a}\n,=больше 2000 pts: {h}')



# bot.polling(none_stop=True)
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(20)