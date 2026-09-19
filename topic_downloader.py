import asyncio
import os
import sys
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeFilename
from config import API_ID, API_HASH

SESSION_NAME = "topic_session"

# ==== USAGE: python3 topic_downloader.py <chat_id> <topic_id> ====

async def main():
    if len(sys.argv) < 3:
        print("Usage: python3 topic_downloader.py <chat_id> <topic_id>")
        return

    chat_id = int(sys.argv[1])
    topic_id = int(sys.argv[2])

    download_dir = f"downloads/{chat_id}/topic_{topic_id}"
    os.makedirs(download_dir, exist_ok=True)

    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    print(f"Connected. Scanning chat {chat_id} for topic {topic_id}...")

    count = 0
    async for message in client.iter_messages(chat_id, reply_to=topic_id):
        if message.media:
            filename = None
            if message.document:
                for attr in message.document.attributes:
                    if isinstance(attr, DocumentAttributeFilename):
                        filename = attr.file_name
            if not filename:
                filename = f"file_{message.id}"

            filepath = os.path.join(download_dir, filename)
            if os.path.exists(filepath):
                print(f"Skipping (already exists): {filename}")
                continue

            print(f"Downloading: {filename}")
            await client.download_media(message, file=filepath)
            count += 1

    print(f"\nDone! Downloaded {count} new files to {download_dir}")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
