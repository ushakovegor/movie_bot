import telebot
import config
import scripts

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    chat_id = message.chat.id
    title = scripts.get_title(message.text)

    bot.send_message(chat_id, 'Here it is: ' + title)


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()