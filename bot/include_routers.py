from aiogram import Dispatcher

from handlers import (
    base_commands,
    spin_slot,
    balance,
    fill,
    payments
)


def include_routers(dp: Dispatcher) -> None:
    dp.include_routers(
        base_commands.router,
        spin_slot.router,
        balance.router,
        fill.router,
        payments.router
    )
