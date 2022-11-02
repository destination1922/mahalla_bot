from bot import MahallaBot
from web import MahallaWeb

if __name__ == '__main__':
    bot = MahallaBot()
    web = MahallaWeb()

    bot.start()
    web.start()

    bot.join()