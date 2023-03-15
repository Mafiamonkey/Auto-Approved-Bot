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
    text = '<b>Welcome to the bot, __Add This Bot To Your Channels or Groups To Accept Join Requests Automatically__\n\n 😊By Team @CineMaVilla</b>'
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Updates Channel", url="https://t.me/Cinema_Villa")],
        [InlineKeyboardButton("Support Group", url="https://t.me/Cinema_Villa_Group")]
    ])
    client.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='html')

import time

@pr0fess0r_99.on_message(filters.command('broadcast'))
async def broadcast_command(client, message):
    # get the message to broadcast
    msg = ' '.join(message.command[1:])
    if not msg:
        await message.reply('Please provide a message to broadcast.')
        return

    await message.reply(f"Broadcasting message: {msg}")
    count = 0
    success = 0
    failure = 0
    for user in collection.find():
        try:
            await client.send_message(user['user_id'], msg)
            success += 1
        except:
            failure += 1
        count += 1
   
        if count % 10 == 0:
            await message.reply(f"Broadcast Status:\nTotal Users: {count}\nSuccessful: {success}\nFailed: {failure}")
        time.sleep(0.5)
    
    await message.reply(f"Broadcasted Status:\nTotal Users: {count}\nSuccessful: {success}\nFailed: {failure}")

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
