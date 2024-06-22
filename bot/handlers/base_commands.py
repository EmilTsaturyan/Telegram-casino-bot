from contextlib import suppress

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from texts import start_text, help_text

from motor.core import AgnosticDatabase as MDB

from pymongo.errors import DuplicateKeyError


router = Router()


@router.message(CommandStart())
async def start(message: Message, db: MDB):
    pattern = {
        '_id': message.from_user.id,
        'balance': 2000
    }

    with suppress(DuplicateKeyError):
        await db.users.insert_one(pattern)

    await message.answer(start_text)
    

@router.message(Command('help'))
async def help(message: Message):
    await message.answer(help_text)