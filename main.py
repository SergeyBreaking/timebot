import datetime
import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

BOT_TOKEN = '6193880932:AAGkFX9mBiNqlKpxj8LCdPPrmqFONeN90eU'

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Определение состояний
class TimeStates(StatesGroup):
    waiting_for_timezone = State()

# Обработчик команды /start
@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Отправь мне команду /time и узнай который час.")

# Обработчик команды /time
@dp.message_handler(Command("time"))
async def cmd_time(message: types.Message):
    # Запрос часового пояса
    await message.answer("Введите часовой пояс (например, Europe/Moscow):")

    # Установка состояния для получаения часового пояса
    await TimeStates.waiting_for_timezone.set()

# Обработчик сообщений, получаемых в состоянии waiting_for_timezone
@dp.message_handler(state=TimeStates.waiting_for_timezone)
async def process_timezone(message: types.Message, state: FSMContext):
    # Получаем часовой пояс, введенный пользователем
    timezone = message.text

    # Попытка получения текущего времени
    try:
        tz = pytz.timezone(timezone)
        now = datetime.datetime.now(tz)
        time_str = now.strftime("Текущее время: %H:%M:%S")
        await message.answer(time_str, parse_mode=ParseMode.HTML)

    # Ошибка, если пояс не найден
    except pytz.exceptions.UnknownTimeZoneError:
        await message.answer("Часовой пояс не найден.")

    # Сбрасываем состояние
    await state.finish()

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)