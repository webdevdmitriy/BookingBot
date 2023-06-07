from aiogram.types import Message


class Request:
    def __init__(self, connector):
        self.connector = connector

    async def add_user(self, message: Message):
        query = f"INSERT INTO datausers(user_id, user_name) VALUES ({message.from_user.id}, '{message.from_user.first_name}') ON CONFLICT (user_id) DO UPDATE SET user_name = 'message.from_user.first_name'"

        await self.connector.execute(query)
        return
