import telebot, random, time, itertools,sqlite3, datetime, emoji
from telebot import types

conn = sqlite3.connect('C:/Users/User/PycharmProjects/telegramBot/db/database', check_same_thread=False)
cursor = conn.cursor()
output = []

def db_table_val(user_id_sql: int, user_name_sql: str, pts_sql: int, last_time: time):
        cursor.execute('REPLACE INTO User (user_id_sql, user_name_sql, pts_sql, last_time) VALUES (?, ?, ?,?)', (user_id_sql, user_name_sql, pts_sql,last_time))
        conn.commit()




class card():
    instances = []

    def __init__(self, name, rarily, avatar):
        '''данные карт'''
        self.name = name
        self.rarily = rarily
        self.avatar = "C:/Users/User/PycharmProjects/telegramBot/avatar/" + avatar
        __class__.instances.append(self)


card1 = card('Yana', 'мифический', 'avatar1.jpg')
card2 = card('Дашя?', 'легендарный', 'avatar2.jpg')
card3 = card('Cameon.', 'легендарный', 'avatar3.jpg')
card4 = card('slepa', 'легендарный', 'avatar4.jpg')
card5 = card('Коки', 'легендарный', 'avatar5.jpg')
card6 = card('YakamoZzz', 'легендарный', 'avatar6.jpg')
card7 = card('гробоеб', 'легендарный', 'avatar7.jpg')
card8 = card('Clum', 'легендарный', 'avatar8.jpg')
card9 = card('duduka', 'легендарный', 'avatar9.jpg')
card10 = card('Амина', 'легендарный', 'avatar10.jpg')
card11 = card('killrht', 'легендарный', 'avatar11.jpg')
card12 = card('Пепся', 'легендарный', 'avatar12.jpg')
card13 = card('Таша насос', 'легендарный', 'avatar13.jpg')
card14 = card('Варвара', 'легендарный', 'avatar14.jpg')
card15 = card('Вова', 'легендарный', 'avatar15.jpg')
card16 = card('Sashi_ia', 'эпические', 'avatar16.jpg')
card17 = card('ISLA', 'эпические', 'avatar17.jpg')
card18 = card('Макс', 'эпические', 'avatar18.jpg')
card19 = card('Леша', 'эпические', 'avatar19.jpg')
card20 = card('Баха', 'эпические', 'avatar20.jpg')
card21 = card('Лисенок', 'эпические', 'avatar21.jpg')
card22 = card('qupper', 'эпические', 'avatar22.jpg')
card23 = card('Эдик', 'редкие', 'avatar23.jpg')
card24 = card('Goddess', 'редкие', 'avatar24.jpg')
card25 = card('Гречка', 'редкие', 'avatar25.jpg')
card26 = card('Спермобак', 'редкие', 'avatar26.jpg')
card27 = card('Майор', 'обычные', 'avatar27.jpg')
card28 = card('Feliks ks ks', 'обычные', 'avatar28.jpg')
card29 = card('Тимур', 'обычные', 'avatar29.jpg')
card30 = card('Yukito', 'обычные', 'avatar30.jpg')
card31 = card('Никто', 'обычные', 'avatar31.jpg')
card32 = card('Bro', 'обычные', 'avatar32.jpg')
card33 = card('fuguto', 'обычные', 'avatar33.jpg')
card34 = card('Эля', 'обычные', 'avatar34.jpg')
card35 = card('BERTLR', 'обычные', 'avatar35.jpg')
card36 = card('Алексей', 'обычные', 'avatar36.jpg')
card37 = card('Леся', 'обычные', 'avatar37.jpg')
card38 = card('pou', 'обычные', 'avatar38.jpg')
card39 = card('Лера', 'обычные', 'avatar39.jpg')
card40 = card('nervapfcrn', 'обычные', 'avatar40.jpg')


bot = telebot.TeleBot('7337494301:AAHxZaJGuha7dpmnTJv_AnCA-DvrQK_0hTs')

itembtn1 = types.KeyboardButton(emoji.emojize('\ud83d\udc85') + 'получить карту')
itembtn2 = types.KeyboardButton(emoji.emojize('\ud83c\udccf') + 'мои карты')
itembtn3 = types.KeyboardButton(emoji.emojize('\u2699\ufe0f') + 'настройки')
itembtn4 = types.KeyboardButton(emoji.emojize('\ud83e\udd47') + 'рейтинг')

@bot.message_handler(commands=['start'])
def start(message):

    mess = (f'<b>{message.from_user.first_name}</b>, добро пожаловать в \n'
            f'Card Pecheneg Bot! \n<a href="tg://resolve?domain=Pecheneg_card">канал с новостями</a>\n'
            f'<a href="https://telegra.ph/Kak-polzovatsya-pecheneg-botom-08-19">обязательно к прочтению</a> \n'
            f'\n'
            f' по всем вопросам писать:\n '
            f'@cammeon \n '
            f'@sabersolovers')

    markup_InLane = types.InlineKeyboardMarkup()




    markup = types.ReplyKeyboardMarkup(row_width=1)

    button1 = types.InlineKeyboardButton('создать новый аккаунт', callback_data='reset')



    markup_InLane.add(button1)
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup_InLane)

    @bot.callback_query_handler(func= lambda call: True)
    def answer(call):

        user_id = call.from_user.id

        if call.data == 'reset':

            info_user_to = cursor.execute("SELECT * FROM User WHERE user_id_sql = " +
                                          str(user_id)).fetchall()

            if len(info_user_to) > 0:
                bot.send_message(message.chat.id, 'вы уже зарегистрированы', parse_mode='html')

            else:

                bot.send_message(message.chat.id, 'Добро Пожаловать!', parse_mode='html', reply_markup=markup)

                us_id_sql = message.from_user.id
                us_name_sql = message.from_user.first_name

                last_time = datetime.datetime.now()

                db_table_val(user_id_sql=us_id_sql, user_name_sql=us_name_sql, pts_sql=100, last_time=last_time)

@bot.message_handler()
def get_user_text(message):

    user_id = message.from_user.id
    current_time = datetime.datetime.now()

    point = 'SELECT user_id_sql, pts_sql FROM User'
    cursor.execute(point)
    rec = cursor.fetchall()
    rec_list = list(sum(rec, ()))


    d = dict(itertools.zip_longest(*[iter(rec_list)] * 2, fillvalue=""))


    cash = d.get(user_id, None)

    cursor.execute('SELECT last_time FROM User WHERE user_id_sql = ?', (user_id,))
    conn.commit()
    last_time = cursor.fetchone()

    if message.text.lower() == 'получить карту' or message.text == '💅' +'получить карту':
            # try:
                pts_sql = 100
                time = (current_time - datetime.datetime.fromisoformat(last_time[0])).seconds
                if time >= 14400:

                    cursor.execute('UPDATE User SET last_time = ? WHERE user_id_sql = ?', (current_time, user_id))

                    cursor.execute("UPDATE User SET pts_sql = pts_sql + ? WHERE user_id_sql = ?", (pts_sql, user_id))
                    conn.commit()


                    randIndex = random.randrange(len(card.instances))
                    randPlayerCharacter = card.instances[randIndex]

                    bot.send_photo(message.from_user.id, open(randPlayerCharacter.avatar, 'rb'),   caption=f'Поздравляю! Вам выпал(а): \n {randPlayerCharacter.name}\n'
                                                                                               f'\n Количество pts: {cash+100}' )
                else:
                    convert = str(datetime.timedelta(seconds = 14400 - time))

                    bot.send_message(message.chat.id,
                                             f'❌<b>СЛИШКОМ РАНО</b> \n'
                                             f'🕓Карту можно получить через:<b> {convert}</b>',
                                             parse_mode='html')
            # except:
            #         bot.send_message(message.chat.id, 'вы не зарегистрированы', parse_mode='html')





    elif message.text.lower() == 'настройки' or message.text == '⚙️' +'настройки':
        try:
            bot.send_message(message.chat.id, f'🎮 Твой ник: {message.from_user.first_name} \n'
                                          f'🌐 Твой aйди: {message.from_user.id}\n'
                                          f'🗓 Дата регистрации: {datetime.datetime.fromisoformat(last_time[0]).strftime("%d.%m.20%yг в %H:%M")}\n'
                                          f'💰Количество pts: {cash}\n\n'
                                          f'❓ Помощь\n⚡️  @cammeon\n👨‍🦯  @sabersolovers', parse_mode='html')
        except:
            bot.send_message(message.chat.id, 'вы не зарегистрированы', parse_mode='html')

    elif message.text.lower() == 'мои карты' or message.text == '🃏' +'мои карты':
        try:
            bot.send_message(message.chat.id, 'тут будет твоя коллекция карт', parse_mode='html')
        except:
            bot.send_message(message.chat.id, 'вы не зарегистрированы', parse_mode='html')


    elif message.text.lower() == 'рейтинг' or message.text == '🥇' +'рейтинг':
        try:
            top = 'SELECT user_id_sql, pts_sql, user_name_sql FROM User'
            cursor.execute(top)
            rec_top = cursor.fetchall()
            rec_top.sort(key=lambda x: x[1], reverse=True)
            msg = ''
            count = 10
            id = 0

            for i in rec_top:
                if id <= count:
                    id += 1
                    msg += f'{id}. <a href="tg://user?id={i[0]}">{i[2]}</a> - {i[1]} pts\n'
                else:
                    break
            bot.send_message(message.chat.id,f'Таблица лидеров:\n{msg}', parse_mode='html')
        except:
            bot.send_message(message.chat.id, 'вы не зарегистрированы', parse_mode='html')


# bot.polling(none_stop=True)
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(5)