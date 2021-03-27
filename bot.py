                                  
#libraries
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
#Bot object
bot= Bot(token='1779209869:AAEpQzdYlcn-9Kqx1wVfQ2-tTrAIOAwprCY')
#Bot dispetcher
dp = Dispatcher(bot)
#Function
@dp.message_handler(commands="hello")
async def hello(message : types.Message):
    await message.reply('hello')

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)
