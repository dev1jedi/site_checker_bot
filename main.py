from create_bot import dp
from aiogram.utils import executor
from telega_bot import main_register
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="log_files/main_log.log", filemode="a")

    print("Бот в сети!")
    main_register(dp)
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logging.info(f"ПРОИЗОШЛА ОШИБКА В ОСНОВНОМ БОТЕ: {e}")

