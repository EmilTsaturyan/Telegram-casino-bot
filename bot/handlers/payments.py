from aiogram.types import LabeledPrice, Message, PreCheckoutQuery, ContentType
from config_reader import config
from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject

from motor.core import AgnosticDatabase as MDB


router = Router()


@router.message(Command('fill'))
async def fill(message: Message, bot: Bot, command: CommandObject):
    text = ''
    amount = command.args

    if amount:
        amount = amount.split(' ')[0]
        if amount.isdigit():
            amount = int(amount)
            if amount >= 50:

                PRICE = LabeledPrice(label='Пополнение баланса', amount=amount * 100)

                await bot.send_invoice(
                    message.chat.id,
                    title='Пополнение счета',
                    description='Пополнение счета для продолжения игры в казино. Больше денег — больше шансов на успех! 💰',
                    provider_token=config.paymaster_token.get_secret_value(),
                    currency='rub',
                    prices=[PRICE],
                    payload="test-invoice-payload"
                )
            else:
                text = '⚠️ Сумма пополнения должна быть больше 50 монет. Попробуй еще раз с большей суммой. 💰'
        else:
            text = '⚠️ Неверное значение для пополнения. Пожалуйста, введи положительное число. 📏'
    else:
        text = '❗️ Пожалуйста, укажи сумму для пополнения, например, /fill 100. 💳'

    if text:
        await message.answer(text)


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message, bot: Bot, db: MDB):
    user = await db.users.find_one({'_id': message.from_user.id})

    await bot.send_message(message.chat.id,
                           f'✅ Пополнение прошло успешно! Твой новый баланс: {user["balance"] + message.successful_payment.total_amount // 100} монет. Удачи в игре! 🎉')
    
    await db.users.update_one({'_id': user['_id']}, {'$set': {'balance': user['balance'] + message.successful_payment.total_amount // 100}})
