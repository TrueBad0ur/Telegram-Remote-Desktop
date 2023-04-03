from telegram.ext import *
from telegram import KeyboardButton, ReplyKeyboardMarkup
import ctypes
import json
import psutil

class TelegramBot:

    def __init__(self):
        f = open('auth.json')
        auth = json.load(f)
        self.TOKEN = auth["token"]
        self.CHAT_ID = auth["chat_id"]

    def start_command(self, update, context):
        buttons = [[KeyboardButton("⚠ Screen status")], [KeyboardButton("🔒 Lock screen")]]
        if update.message.chat["username"] != "USERNAME":
            print("[!] " + update.message.chat["username"] + ' started bot')
        else:
            context.bot.send_message(chat_id=self.CHAT_ID, text="I will do what you command.", reply_markup=ReplyKeyboardMarkup(buttons))

    def error(self, update, context):
        print(f"Update {update} caused error {context.error}")

    def handle_message(self, update, input_text):
        usr_msg = input_text.split()

        if input_text == 'screen status':
            for proc in psutil.process_iter():
                if (proc.name() == "LogonUI.exe"):
                    return '✅ Screen is Locked'
            return '❌ Screen is Unlocked'

        if input_text == 'lock screen':
            try:
                ctypes.windll.user32.LockWorkStation()
                return "✅ Screen locked successfully"
            except:
                return "❌ Error while locking screen"

    def send_response(self, update, context):
        user_message = update.message.text

        if update.message.chat["username"] != "USERNAME":
            print("[!] " + update.message.chat["username"] + ' tried to use this bot')
        else:
            user_message = user_message.encode('ascii', 'ignore').decode('ascii').strip(' ')
            user_message = user_message[0].lower() + user_message[1:]
            response = self.handle_message(update, user_message)
            if response:
                if (len(response) > 4096):
                    for i in range(0, len(response), 4096):
                        context.bot.send_message(chat_id=self.CHAT_ID, text=response[i:4096+i])
                else:
                    context.bot.send_message(chat_id=self.CHAT_ID, text=response)

    def start_bot(self):
        updater = Updater(self.TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", self.start_command))
        dp.add_handler(MessageHandler(Filters.text, self.send_response))
        dp.add_error_handler(self.error)
        updater.start_polling()
        print("[+] BOT has started")
        updater.idle()
