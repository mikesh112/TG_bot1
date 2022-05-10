from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

TOKEN = '5389826870:AAHXkptHgOZ-Ohpb81ltkj2eyimgTCWC2jA'

file_to_convert = None
file_type_from, file_type_to = None, None


# a short description of the bot
def help(update, context):
    update.message.reply_text(
        "Привет еще раз!\n\n1)Пришли мне файл, который нужно конвертировать\n2)Затем выбери новый формат "
        "файла из предложенных\n3)Результатом ты получешь присланный мною файл с "
        "нужным расширением\n\nПо всем вопросам и предложениям обращаться @mikesh112")


# conversation 1 start func - greetings; asks to send a file
def start(update, context):
    update.message.reply_text(
        "Привет!\n\n"
        "Я бот, который умеет конвертировать файлы\n"
        "Будут вопросы пиши /help")

    update.message.reply_text(
        "Пришли мне файл, который хочешь конвертировать")
    return 1


# conversation 1 end func - gets file to convert; asks to send file type
def first_response(update, context):
    global file_to_convert
    file_to_convert = context.bot.get_file(update.message.document).download()
    update.message.reply_text("Напиши тип расширение файла без точки с маленькой буквы\n"
                              "Файлы без расширений мы пока не принимам)\n")
    update.message.document(file_to_convert)
    return ConversationHandler.END


# conversation 2 start func - gets type file; asks for converting type
def second_response(update, context):

    type = update.message.text
    logger.info(type)
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return 3  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.


# conversation midl func - gets type to convert; converts file; sends file
def third_response(update, context): pass


# conversation end func - says bye
def stop(update, context):
    update.message.reply_text("Всего доброго!\n"
                              "Для повторного использования пишите /start")
    return ConversationHandler.END


# conversation
# in MessageHandler of each state: Filters.<> - is to accept; ~Filters.<> - is not acceptable to get
conv_handler_1 = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text & Filters.document & ~Filters.command, first_response)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

conv_handler_2 = ConversationHandler(
    entry_points=[MessageHandler(Filters.text, second_response)],
    states={
            1: [MessageHandler(Filters.text & Filters.document & ~Filters.command, first_response)],
            2: [MessageHandler(Filters.text & Filters.document & ~Filters.command, second_response)],
            3: [MessageHandler(Filters.text & ~Filters.command, third_response)]
        },
    fallbacks=[CommandHandler('stop', stop)]
)

def main():
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(conv_handler_1)
    updater.dispatcher.add_handler(MessageHandler(Filters.document, first_response))
    updater.dispatcher.add_handler(conv_handler_2)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
