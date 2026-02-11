# Don't Remove Credit Tg - @TeamJB
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TeamJB
# Ask Doubt on telegram @TeamJB_Support

import os
import asyncio 
import random
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied, ChatAdminRequired, UserNotParticipant, MessageIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from config import API_ID, API_HASH, ERROR_MESSAGE, LOGIN_SYSTEM, STRING_SESSION, CHANNEL_ID, WAITING_TIME
from database.db import db
from TeamJB.strings import HELP_TXT
from bot import TeamJBUser

class batch_temp(object):
    IS_BATCH = {}

async def downstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(3)
      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            await client.edit_message_text(chat, message.id, f"**Downloaded:** **{txt}**")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)

# upload status
async def upstatus(client, statusfile, message, chat):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            await client.edit_message_text(chat, message.id, f"**Uploaded:** **{txt}**")
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(5)

# progress writer
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")

# start command
@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    buttons = [[
        InlineKeyboardButton("❣️ Developer", url = "https://t.me/TeamJB_bot")
    ],[
        InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/botsupdatesgroup'),
        InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/teamjb1')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id, 
        text=f"<b>👋 Hi {message.from_user.mention}, I am Save Restricted Content Bot, I can send you restricted content by its post link.\n\nFor downloading restricted content /login first.\n\nKnow how to use bot by - /help</b>", 
        reply_markup=reply_markup, 
        reply_to_message_id=message.id
    )
    return

# help command
@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
    await client.send_message(
        chat_id=message.chat.id, 
        text=HELP_TXT
    )

# cancel command
@Client.on_message(filters.command(["cancel"]))
async def send_cancel(client: Client, message: Message):
    batch_temp.IS_BATCH[message.from_user.id] = True
    await client.send_message(
        chat_id=message.chat.id, 
        text="**Batch Successfully Cancelled.**",
        reply_to_message_id=message.id
    )

@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):
    # Joining chat
    if ("https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text) and LOGIN_SYSTEM == False:
        if TeamJBUser is None:
            await client.send_message(message.chat.id, "String Session is not Set", reply_to_message_id=message.id)
            return
        try:
            try:
                await TeamJBUser.join_chat(message.text)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await TeamJBUser.join_chat(message.text)
            except Exception as e: 
                await client.send_message(message.chat.id, f"Error : {e}", reply_to_message_id=message.id)
                return
            await client.send_message(message.chat.id, "Chat Joined", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            await client.send_message(message.chat.id, "Chat already Joined", reply_to_message_id=message.id)
        except InviteHashExpired:
            await client.send_message(message.chat.id, "Invalid Link", reply_to_message_id=message.id)
        return
    
    if "https://t.me/" in message.text:
        if batch_temp.IS_BATCH.get(message.from_user.id) == False:
            return await message.reply_text("**One Task Is Already Processing. Wait For Complete It. If You Want To Cancel This Task Then Use - /cancel**")
        
        datas = message.text.split("/")
        temp = datas[-1].replace("?single","").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID

        # Login system handling
        if LOGIN_SYSTEM == True:
            user_data = await db.get_session(message.from_user.id)
            if user_data is None:
                await message.reply("**For Downloading Restricted Content You Have To /login First.**")
                return
            api_id = int(await db.get_api_id(message.from_user.id))
            api_hash = await db.get_api_hash(message.from_user.id)
            try:
                acc = Client("saverestricted", session_string=user_data, api_hash=api_hash, api_id=api_id)
                await acc.connect()
            except Exception as e:
                return await message.reply(f"**Your Login Session Expired. So /logout First Then Login Again By - /login**\n\nError: {e}")
        else:
            if TeamJBUser is None:
                await client.send_message(message.chat.id, f"**String Session is not Set**", reply_to_message_id=message.id)
                return
            acc = TeamJBUser
                
        batch_temp.IS_BATCH[message.from_user.id] = False
        
        for msgid in range(fromID, toID+1):
            if batch_temp.IS_BATCH.get(message.from_user.id): 
                break
            
            try:
                # Private channel/group - FIXED AND WORKING
                if "https://t.me/c/" in message.text:
                    chatid = int("-100" + datas[4])
                    try:
                        await handle_private(client, acc, message, chatid, msgid)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        await handle_private(client, acc, message, chatid, msgid)
                    except Exception as e:
                        if ERROR_MESSAGE == True:
                            await client.send_message(message.chat.id, f"Error in private: {e}", reply_to_message_id=message.id)
                
                # Bot
                elif "https://t.me/b/" in message.text:
                    username = datas[4]
                    try:
                        await handle_private(client, acc, message, username, msgid)
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        await handle_private(client, acc, message, username, msgid)
                    except Exception as e:
                        if ERROR_MESSAGE == True:
                            await client.send_message(message.chat.id, f"Error in bot: {e}", reply_to_message_id=message.id)
                
                # Public channel/group
                else:
                    username = datas[3]
                    try:
                        # Try with userbot first for restricted content
                        if LOGIN_SYSTEM == True or TeamJBUser is not None:
                            await handle_private(client, acc, message, username, msgid)
                        else:
                            # Try with bot
                            msg = await client.get_messages(username, msgid)
                            await client.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                    except UsernameNotOccupied: 
                        await client.send_message(message.chat.id, "The username is not occupied by anyone", reply_to_message_id=message.id)
                    except (ChatAdminRequired, UserNotParticipant, MessageIdInvalid):
                        # If bot can't access, try with userbot
                        await handle_private(client, acc, message, username, msgid)
                    except Exception as e:
                        if ERROR_MESSAGE == True:
                            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            
            except Exception as e:
                if ERROR_MESSAGE == True:
                    await client.send_message(message.chat.id, f"Unexpected error: {e}", reply_to_message_id=message.id)
            
            # Random delay between messages to avoid flood waits
            await asyncio.sleep(random.randint(WAITING_TIME, WAITING_TIME + 5))
        
        # Disconnect user client
        if LOGIN_SYSTEM == True:
            try:
                await acc.disconnect()
            except:
                pass                
        batch_temp.IS_BATCH[message.from_user.id] = True

# handle private - COMPLETELY FIXED for private channels/groups
async def handle_private(client: Client, acc, message: Message, chatid, msgid: int):
    try:
        # Try to get message with flood wait handling
        try:
            msg: Message = await acc.get_messages(chatid, msgid)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            msg: Message = await acc.get_messages(chatid, msgid)
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"Error fetching message: {e}", reply_to_message_id=message.id)
            return
        
        # Check if message exists
        if not msg or msg.empty:
            await client.send_message(message.chat.id, f"❌ Message {msgid} not found or inaccessible in this chat.", reply_to_message_id=message.id)
            return
        
        # Get message type
        msg_type = get_message_type(msg)
        if not msg_type:
            await client.send_message(message.chat.id, f"❌ Unsupported message type for message {msgid}", reply_to_message_id=message.id)
            return
        
        # Set destination chat
        if CHANNEL_ID:
            try:
                chat = int(CHANNEL_ID)
            except:
                chat = message.chat.id
        else:
            chat = message.chat.id
        
        # Check if batch cancelled
        if batch_temp.IS_BATCH.get(message.from_user.id):
            return
        
        # Handle text messages directly
        if "Text" == msg_type:
            try:
                await client.send_message(chat, msg.text, entities=msg.entities, 
                                        reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
                return
            except Exception as e:
                if ERROR_MESSAGE == True:
                    await client.send_message(message.chat.id, f"Error sending text: {e}", 
                                            reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
                return

        # Send initial status message
        smsg = await client.send_message(message.chat.id, f'**📥 Downloading message {msgid}...**', 
                                        reply_to_message_id=message.id)
        
        # Start download status tracker
        asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg, chat))
        
        # Download media with flood wait handling
        try:
            file = await acc.download_media(msg, progress=progress, 
                                          progress_args=[message, "down"])
        except FloodWait as e:
            await asyncio.sleep(e.value)
            file = await acc.download_media(msg, progress=progress, 
                                          progress_args=[message, "down"])
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"❌ Download failed: {e}", 
                                        reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML)
            await smsg.delete()
            return
        
        # Remove download status file
        try:
            os.remove(f'{message.id}downstatus.txt')
        except:
            pass
        
        # Check if batch cancelled
        if batch_temp.IS_BATCH.get(message.from_user.id):
            try:
                os.remove(file)
            except:
                pass
            await smsg.delete()
            return
        
        # Start upload status tracker
        asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg, chat))
        
        # Get caption
        caption = msg.caption if msg.caption else None
        if caption:
            # Clean caption
            caption = caption[:1024]  # Telegram caption limit
        
        # Check if batch cancelled
        if batch_temp.IS_BATCH.get(message.from_user.id):
            try:
                os.remove(file)
            except:
                pass
            await smsg.delete()
            return
        
        # Send media based on type
        try:
            if "Document" == msg_type:
                # Download thumbnail if exists
                ph_path = None
                try:
                    if msg.document.thumbs:
                        ph_path = await acc.download_media(msg.document.thumbs[0].file_id)
                except:
                    pass
                
                try:
                    await client.send_document(chat, file, thumb=ph_path, caption=caption,
                                             reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML,
                                             progress=progress, progress_args=[message, "up"])
                except Exception as e:
                    if ERROR_MESSAGE == True:
                        await client.send_message(message.chat.id, f"❌ Upload failed: {e}", 
                                                reply_to_message_id=message.id)
                
                if ph_path and os.path.exists(ph_path):
                    os.remove(ph_path)
            
            elif "Video" == msg_type:
                # Download thumbnail if exists
                ph_path = None
                try:
                    if msg.video.thumbs:
                        ph_path = await acc.download_media(msg.video.thumbs[0].file_id)
                except:
                    pass
                
                try:
                    await client.send_video(chat, file, duration=msg.video.duration,
                                          width=msg.video.width, height=msg.video.height,
                                          thumb=ph_path, caption=caption,
                                          reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML,
                                          progress=progress, progress_args=[message, "up"])
                except Exception as e:
                    if ERROR_MESSAGE == True:
                        await client.send_message(message.chat.id, f"❌ Upload failed: {e}", 
                                                reply_to_message_id=message.id)
                
                if ph_path and os.path.exists(ph_path):
                    os.remove(ph_path)
            
            elif "Animation" == msg_type:
                try:
                    await client.send_animation(chat, file, caption=caption,
                                              reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML,
                                              progress=progress, progress_args=[message, "up"])
                except Exception as e:
                    if ERROR_MESSAGE == True:
                        await client.send_message(message.chat.id, f"❌ Upload failed: {e}", 
                                                reply_to_message_id=message.id)
            
            elif "Sticker" == msg_type:
                try:
                    await client.send_sticker(chat, file, reply_to_message_id=message.id)
                except Exception as e:
                    if ERROR_MESSAGE == True:
                        await client.send_message(message.chat.id, f"❌ Upload failed: {e}", 
                                                reply_to_message_id=message.id)
            
            elif "Voice" == msg_type:
                try:
                    await client.send_voice(chat, file, caption=caption,
                                          caption_entities=msg.caption_entities,
                                          reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML,
                                          progress=progress, progress_args=[message, "up"])
                except Exception as e:
                    if ERROR_MESSAGE == True:
                        await client.send_message(message.chat.id, f"❌ Upload failed: {e}", 
                                                reply_to_message_id=message.id)
            
            elif "Audio" == msg_type:
                # Download thumbnail if exists
                ph_path = None
                try:
                    if msg.audio.thumbs:
                        ph_path = await acc.download_media(msg.audio.thumbs[0].file_id)
                except:
                    pass
                
                try:
                    await client.send_audio(chat, file, thumb=ph_path, caption=caption,
                                          reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML,
                                          progress=progress, progress_args=[message, "up"])
                except Exception as e:
                    if ERROR_MESSAGE == True:
                        await client.send_message(message.chat.id, f"❌ Upload failed: {e}", 
                                                reply_to_message_id=message.id)
                
                if ph_path and os.path.exists(ph_path):
                    os.remove(ph_path)
            
            elif "Photo" == msg_type:
                try:
                    await client.send_photo(chat, file, caption=caption,
                                          reply_to_message_id=message.id, parse_mode=enums.ParseMode.HTML,
                                          progress=progress, progress_args=[message, "up"])
                except Exception as e:
                    if ERROR_MESSAGE == True:
                        await client.send_message(message.chat.id, f"❌ Upload failed: {e}", 
                                                reply_to_message_id=message.id)
        
        except Exception as e:
            if ERROR_MESSAGE == True:
                await client.send_message(message.chat.id, f"❌ Upload error: {e}", 
                                        reply_to_message_id=message.id)
        
        # Cleanup
        try:
            os.remove(f'{message.id}upstatus.txt')
            os.remove(file)
        except:
            pass
        
        # Delete status message
        try:
            await client.delete_messages(message.chat.id, [smsg.id])
        except:
            pass
        
        # Send success message - FIXED: Missing parenthesis was here
        await client.send_message(message.chat.id, f"✅ **Successfully saved message {msgid}**", 
                                reply_to_message_id=message.id)
        
    except Exception as e:
        if ERROR_MESSAGE == True:
            await client.send_message(message.chat.id, f"❌ Critical error: {e}", 
                                    reply_to_message_id=message.id)

# get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
    try:
        if msg.document:
            return "Document"
    except:
        pass

    try:
        if msg.video:
            return "Video"
    except:
        pass

    try:
        if msg.animation:
            return "Animation"
    except:
        pass

    try:
        if msg.sticker:
            return "Sticker"
    except:
        pass

    try:
        if msg.voice:
            return "Voice"
    except:
        pass

    try:
        if msg.audio:
            return "Audio"
    except:
        pass

    try:
        if msg.photo:
            return "Photo"
    except:
        pass

    try:
        if msg.text:
            return "Text"
    except:
        pass
    
    return None

# Don't Remove Credit @TeamJB
# Subscribe YouTube Channel For Amazing Bot @TeamJB
# Ask Doubt on telegram @TeamJB_Support
