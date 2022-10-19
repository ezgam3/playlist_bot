import argparse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--test", type=bool, default=False)

args = parser.parse_args()
if args.test:
    from dotenv import load_dotenv

    load_dotenv(".env")


from aiogram import executor

from app.entrypoint import dp, on_starup, scheduler
import app.handlers  # noqa: F401 # This is needed to register handlers


scheduler.start()

executor.start_polling(dp, on_startup=on_starup)
