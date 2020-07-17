from telegram.ext import CommandHandler, MessageHandler, Filters, PicklePersistence
from bot_token import token
TOKEN = token

### logging to see errors
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


########## start function ##########
def start(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "TEST MODE! \nType '/help' to know the commands!")
    # store data
start_handler = CommandHandler('start', start)


######### list letter names function #########
def list_letters(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = str(context.bot_data['vol 1']) )
    context.bot.send_message(chat_id = update.effective_chat.id, text = str(context.bot_data['vol 2']) )

list_handler = CommandHandler('list', list_letters)


####### read a letter function #########
def read(update, context):
    key = update.message.text.partition(' ')[2]

    try:
        letter_to_read = context.bot_data['letters'][key]
        for l in letter_to_read:
            update.message.reply_text(l)

    except KeyError:
        update.message.reply_text("no such letter found")

read_handler = CommandHandler('read',read)


####### help: lists commands #######
def help(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "/list : list all the letters \n/read <letter_number>: fetches selected letter")
help_handler = CommandHandler('help', help)



####### MAIN FUNCTION ie setup ######
def main():
    ### creating the updater and dispatcher
    from telegram.ext import Updater
    updater = Updater(token = token, persistence=my_persistence, use_context=True)
    dispatcher = updater.dispatcher
    
    ## storing list of letters and dictionary into the bot_data
    fn = 'meta_letters/Volume 1.txt'
    with open(fn, 'r') as fo:
        vol1 = fo.read()
    fn = 'meta_letters/Volume 2.txt'
    with open(fn, 'r') as fo:
        vol2 = fo.read()
    # fn = 'all_letters/dict_0to10.json'
    fn = 'all_letters/dict_all_letters.json'
    with open(fn, 'r') as fo:
        import json
        letters = json.load(fo)
    
    #### storing into bot_data
    dispatcher.bot_data['vol 1'] = vol1
    dispatcher.bot_data['vol 2'] = vol2
    dispatcher.bot_data['letters'] = letters

    #### adding handlers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(read_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(list_handler)

    ### HEROKU PORTS
    import os
    PORT = int(os.environ.get('PORT', '8443'))
    # add handlers
    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)
    updater.bot.set_webhook("https://senecabot-01.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()