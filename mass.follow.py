import asyncio
import random
import time
from telethon import TelegramClient, functions
from telethon.errors import FloodWaitError

# --- ТВОИ ДАННЫЕ ---
API_ID = 1234567 # Твой API ID с my.telegram.org
API_HASH = "7d481ca19c1be95dacfe86e26bab8326" 
PHONE = "+380978226544" # Твой номер телефона
TARGET_CHANNEL = "@https://t.me/bogdan201627" # Ссылка на канал, где искать людей

async def main():
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(phone=PHONE)
    
    print("🔍 Собираем участников канала...")
    participants = []
    async for user in client.iter_participants(TARGET_CHANNEL):
        if not user.bot and not user.deleted:
            participants.append(user.id)
    
    random.shuffle(participants)
    print(f"✅ Найдено {len(participants)} человек. Начинаем подписку...")
    
    count = 0
    for user_id in participants:
        try:
            await client(functions.contacts.AddContactRequestRequest(
                id=user_id,
                first_name="Friend",
                last_name="",
                phone="",
                add_phone_privacy_exception=False
            ))
            count += 1
            print(f"[+] Добавлен {user_id} ({count}/{len(participants)})")
            
            # Задержка, чтобы не забанили
            time.sleep(random.randint(15, 30))
            
            if count >= 50: # Лимит в день
                print("🛑 Достигнут лимит на сегодня (50). Ждем 24 часа.")
                break
                
        except FloodWaitError as e:
            print(f"⏳ FloodWait: ждем {e.seconds} секунд...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
