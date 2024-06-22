from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from filters.is_admin import IsAdmin
from config_reader import config

from motor.core import AgnosticDatabase as MDB



router = Router()

@router.message(Command('admin_fill'), IsAdmin(config.admin_id.get_secret_value()))
async def admin_fill(message: Message, db: MDB, command: CommandObject):
    amount = command.args.split(' ')[0]

    user = await db.users.find_one({'_id': message.from_user.id})
    await db.users.update_one({'_id': user['_id']}, {'$set': {'balance': user['balance'] + int(amount)}})
