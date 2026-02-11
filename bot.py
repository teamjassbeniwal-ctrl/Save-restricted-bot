# Don't Remove Credit Tg - @TeamJB
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@jassbeniwaltech
# Ask Doubt on telegram @TeamJB_bot

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION, LOGIN_SYSTEM

if STRING_SESSION is not None and LOGIN_SYSTEM == False:
    TeamJBUser = Client("TeamJB", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
    TeamJBUser.start()
else:
    TeamJBUser = None

class Bot(Client):

    def __init__(self):
        super().__init__(
            "teamjb login",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="TeamJB"),
            workers=150,
            sleep_threshold=5
        )

    async def start(self):
        await super().start()
        print('Bot Started Powered By @TeamJB')

    async def stop(self, *args):
        await super().stop()
        print('Bot Stopped Bye')

if __name__ == "__main__":
    bot = Bot()
    bot.run()

# Don't Remove Credit Tg - @TeamJB
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@jassbeniwaltech
# Ask Doubt on telegram @TeamJB_bot
