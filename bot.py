import telebot
import config
import createdb

bot = telebot.TeleBot(config.TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Это бот для сохранения и напоминания \n"
                     "вашего качества на текущий год.")

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/start', '/save', '/quality')
    bot.send_message(message.chat.id,
                     "Команды-кнопки для бота:\n"
                     "«<b>start</b>» - возврат в начало\n"
                     "«<b>save</b>» - ввод вашего качества на год\n"
                     "«<b>quality</b>» - напомнить ваше качество",
                     reply_markup=keyboard)


@bot.message_handler(commands=['save'])
def save(message):
    user_quality = createdb.get_user_quality(message.chat.id)

    if user_quality is None:
        msg_input = bot.send_message(message.chat.id, "Введите качество на текущий год:")
        bot.register_next_step_handler(msg_input, set_quality)
    else:
        bot.send_message(message.chat.id, f"Ваше качество на текущий год - <b>{user_quality[0]}</b>")

        markup = telebot.types.InlineKeyboardMarkup()
        markup.row(telebot.types.InlineKeyboardButton(text="Да", callback_data="yes"),
                   telebot.types.InlineKeyboardButton(text="Нет", callback_data="no"))
        bot.send_message(message.chat.id, text="Желаете записать новое качество?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'yes':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        msg_input = bot.send_message(call.message.chat.id, "Введите новое качество на год:")
        bot.register_next_step_handler(msg_input, set_quality)
    else:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Удачи!")


def set_quality(message):

    if is_correct_quality(message.text):
        user_quality = message.text.upper()
        bot.send_message(message.chat.id, f"Ваше качество на текущий год - <b>{user_quality}</b>")

        is_check_user = createdb.check_user_id(message.chat.id)
        if is_check_user is None:
            createdb.insert_user_quality(message.chat.id, user_quality)
        else:
            createdb.update_user_quality(message.chat.id, user_quality)

    else:
        msg_try = bot.send_message(message.chat.id, "Некорректные символы. Попробуйте еще раз:")
        bot.register_next_step_handler(msg_try, set_quality)


def is_correct_quality(text):
    for letter in text:
        code = ord(letter)
        if all([(not(1040 < code < 1103)),
                (code != 1025),
                (code != 1105),
                (code != 32),
                (code != 44),
                (code != 45)]):
            return False
    return True


@bot.message_handler(commands=['quality'])
def quality(message):
    is_check_user = createdb.check_user_id(message.chat.id)
    if is_check_user is None:
        bot.send_message(message.chat.id, "Качество ранее не было сохранено.")
    else:
        saved_user_quality = createdb.get_user_quality(message.chat.id)
        bot.send_message(message.chat.id, f"Ваше качество на текущий год - <b>{saved_user_quality[0]}</b>")


@bot.message_handler(commands=['fv'])
def force_vita(message):
    with open("user_values.txt", encoding="utf-8") as f:
        result = f.read()
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['all'])
def get_all(message):
    rows = createdb.get_all()
    result = "id telegram - value\n"
    for line in rows:
        result += f"{line[0]} - {line[1]}\n"
    bot.send_message(message.chat.id, f"{result}")


@bot.message_handler(content_types=["text"])
def answers(message):
    bot.send_message(message.chat.id, "А ведь еще подумать надо над качеством!")


if __name__ == '__main__':
    bot.infinity_polling()
