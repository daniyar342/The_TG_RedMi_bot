import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

# Replace 'YOUR_BOT_API_TOKEN' with your actual bot's API token
API_TOKEN = '6670475375:AAGC5P4nqeLVdZLzzy9mrzTytBPy0AISmLQ'

# Initialize the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define a handler for the /start command
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Create a keyboard with the "Start" button
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Start")
    keyboard.add(start_button)

    # Send a welcome message with the keyboard
    await message.answer("Welcome to your bot! Press 'Start' to begin.", reply_markup=keyboard)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
