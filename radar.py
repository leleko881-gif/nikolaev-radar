import re
from telethon import TelegramClient, events

# --- НАЛАШТУВАННЯ БОТА ---
API_ID = 35622918  
API_HASH = '7641a9e939e59ac62a23ac19b07da409'
BOT_TOKEN = '8986509917:AAG32u1xE5hfF3_W5Cb4G0bd7qQ4hc_s3NE'
MY_CHAT_ID = 1011295878  

CHANNELS = ['kpszsu', 'vanek_nikolaev'] 
KEYWORDS = [r'шахед', r'бпла', r'мопед', r'дрон', r'курс', r'шахід']

UKRAINE_GEO_BASE = {
    'миколаїв': (46.9750, 31.9946),
    'очаків': (46.6136, 31.5494),
    'баштанка': (47.4142, 32.4478),
    'вознесенськ': (47.5623, 31.3284),
    'южноукраїнськ': (47.8217, 31.1744),
    'березанка': (46.8518, 31.3888),
    'первомайськ': (48.0439, 30.8503),
    'снігурівка': (47.0694, 32.8106),
    'коблево': (46.6633, 31.2001),
    'нова одеса': (47.3072, 31.7853)
}

client = TelegramClient('radar_fresh_bot_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CHANNELS))
async def my_event_handler(event):
    text = event.message.message
    if not text:
        return
    
    text_lower = text.lower()
    has_drone = any(re.search(word, text_lower) for word in KEYWORDS)
    
    if has_drone:
        for city, coords in UKRAINE_GEO_BASE.items():
            if re.search(city, text_lower):
                lat, lon = coords
                
                # Формуємо красивий текст для телефону
                report_message = (
                    f"🚨 **РАДАР: ВИЯВЛЕНО ЦІЛЬ!**\n\n"
                    f"🎯 **Локація:** {city.upper()}\n"
                    f"📍 **Координати:** `{lat}, {lon}`\n\n"
                    f"📝 **Повідомлення:**\n{text}"
                )
                
                # Виводимо в консоль на ПК
                print("\n" + "🚨" * 20)
                print(f"🎯 Ціль [{city.upper()}] зафіксовано! Надсилаю сповіщення на телефон...")
                print("🚨" * 20 + "\n")
                
                try:
                    # Надсилаємо текстове сповіщення в чат вашого бота
                    await client.send_message(MY_CHAT_ID, report_message)
                except Exception as e:
                    print(f"⚠️ Не вдалося надіслати повідомлення в Telegram: {e}")
                break

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("📡 Радар-бот успішно запустився та перейшов у режим моніторингу з трансляцією на телефон!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())