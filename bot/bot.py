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
    print(message.text)
    title, title_id = scripts.get_title(message.text)
    link = scripts.get_link(title_id)
    bot.send_message(chat_id, 'Here it is: ' + title + '\n' + 'https://www.imdb.com/title/tt' + link)


def main():
    scripts.pre_actions()
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
