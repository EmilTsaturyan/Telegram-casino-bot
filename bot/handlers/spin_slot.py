from contextlib import suppress
import random

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import DiceEmoji

from texts import wining_texts, loosing_texts

from motor.core import AgnosticDatabase as MDB


router = Router()


def get_cef(value):
    if value in (1, 22, 43):
        cef = 5
    elif value in (16, 32, 48):
        cef = 2
    elif value == 64:
        cef = 10
    else:
        cef = -1
    return cef 


@router.message(Command('spin'))
async def spin(message: Message, db: MDB, command: CommandObject):
    args = command.args
    user = await db.users.find_one({'_id': message.from_user.id})
    pattern = {'text': ''}

    if args:
        amount = args.split(' ')[-1]
        if amount.isdigit():
            amount = int(amount)

            if amount <= user['balance']:
                await db.users.update_one({'_id': user['_id']}, {'$set': {'balance': user['balance'] - amount}})
                value = await message.answer_dice(DiceEmoji.SLOT_MACHINE)

                cef = get_cef(value.dice.value)
                if cef != -1:
                    new_balance = user['balance'] - amount + amount * cef
                    await db.users.update_one({'_id': user['_id']}, {'$set': {'balance': new_balance}})
                    pattern['text'] = random.choice(wining_texts).format(amount * cef)
                else:
                    new_balance = user['balance'] - amount
                    pattern['text'] = random.choice(loosing_texts).format(amount)
            else:
                pattern['text'] = '❗️ Недостаточно средств для ставки. Пополни свой баланс командой /fill и попробуй снова. 💰'
        else:
            pattern['text'] = '⚠️ Неверное значение для ставки. Пожалуйста, введи положительное число больше нуля. 📏'
    else:
        pattern['text'] = '❗️ Пожалуйста, укажи сумму для ставки, например, /spin 100. 🎡'

    await message.answer(**pattern)