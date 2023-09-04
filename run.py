from create_bot import dp
from aiogram.utils import executor
from handlers import clients,admin

clients.register_handlers_clients(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
