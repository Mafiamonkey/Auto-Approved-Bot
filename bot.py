# MIT License

# Copyright (c) 2022 Muhammed

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Telegram Link : https://telegram.dog/Mo_Tech_Group
# Repo Link : https://github.com/PR0FESS0R-99/Auto-Approved-Bot
# License Link : https://github.com/PR0FESS0R-99/Auto-Approved-Bot/blob/Auto-Approved-Bot/LICENSE

from os import environ
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User, ChatJoinRequest

API_ID = "23654242"
API_HASH = "e466bc6290636019c66946a40993b4c3"
BOT_TOKEN = "6154167962:AAG1W-mWr_4KD8IC_q_CQJnWrt5J6O1jCus"

pr0fess0r_99=Client(
    "Auto Approved Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

CHAT_ID = "-1001906618833"
APPROVED_WELCOME_TEXT = environ.get("APPROVED_WELCOME_TEXT", "Hello {mention}\nWelcome To {title}\n\nYour Auto Approved")
APPROVED_WELCOME = environ.get("APPROVED_WELCOME", "on").lower() == "on"


@pr0fess0r_99.on_chat_join_request()
async def autoapprove(client: pr0fess0r_99, message: ChatJoinRequest):
    chat=message.chat # Chat
    user=message.from_user # User
    print(f"{user.first_name} Joined 🤝") # Logs
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if APPROVED_WELCOME:
        await client.send_message(chat_id=chat.id, text=APPROVED_WELCOME_TEXT.format(mention=user.mention, title=chat.title))
    if CHAT_ID:
        log_chat = await client.get_chat(chat_id=CHAT_ID)
        log_text = f"{user.first_name} ({user.mention}) has been auto-approved to {chat.title} ({chat.username})"
        await client.send_message(chat_id=log_chat.id, text=log_text)

from pymongo import MongoClient

# set up MongoDB connection
client_mongo = MongoClient('mongodb+srv://Dave:Dave@cluster0.nvjotuh.mongodb.net/?retryWrites=true&w=majority')
db = client_mongo['mydb']
collection = db['users']

# define start command to save new users
@pr0fess0r_99.on_message(filters.command('start'))
def start_command(client, message):
    # check if user is already in the database
    user = collection.find_one({'user_id': message.chat.id})
    if not user:
        # add new user to the database
        user = {
            'user_id': message.chat.id,
            'username': message.chat.username,
            'first_name': message.chat.first_name,
            'last_name': message.chat.last_name
        }
        collection.insert_one(user)
    # send welcome message
    client.send_message(message.chat.id, '<b>Welcome to the bot, __Add This Bot To Your Channels or Groups To Accept Join Requests Automatically__\n\n 😊By Team @CineMaVilla</b>')

# define broadcast command to send message to all users
@pr0fess0r_99.on_message(filters.command('broadcast'))
def broadcast_command(client, message):
    msg = ' '.join(message.command[1:])
    if not msg:
        client.send_message(message.chat.id, 'Please provide a message to broadcast.')
        return
    for user in collection.find():
        client.send_message(user['user_id'], msg)

@pr0fess0r_99.on_message(filters.command('users'))
def users_command(client, message):
    users = collection.find()
    if users.count() == 0:
        client.send_message(message.chat.id, 'No users found.')
        return
    user_list = []
    for user in users:
        if user['username']:
            user_list.append('@' + user['username'] + ' (' + str(user['user_id']) + ')')
        else:
            user_list.append(str(user['user_id']))
    if message.chat.type == 'private':
        client.send_message(message.chat.id, '\n'.join(user_list))
    else:
        client.send_document(message.chat.id, 'users.json', {'user_list': user_list})

print("Auto Approved Bot Started")
pr0fess0r_99.run()
