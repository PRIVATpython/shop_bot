from handlers import bot
import logging

logging.basicConfig(filename="sample.log", level=logging.INFO)


if __name__ == '__main__':
#     while True:
#         try:
        bot.polling(none_stop=True)
        # except Exception as ex:
        #     logging.error(ex)
