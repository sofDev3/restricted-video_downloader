# restricted-video_downloader

A lightweight Python script to download media (videos, documents, etc.) from a **specific topic/thread** inside a Telegram forum-style supergroup — without downloading the entire group's media.

## Why this exists

Many Telegram supergroups (especially study/course groups) use **Forum Topics** to organize content into separate threads (e.g., one topic per subject). Most existing Telegram media downloader tools only support filtering by `chat_id`, which downloads **everything** in the group — including unrelated topics.

This script uses [Telethon](https://github.com/LonamiWebs/Telethon)'s `iter_messages(chat, reply_to=topic_id)` to fetch messages from **only one topic/thread**, and downloads just the media attached to those messages.

## Features

- Download media from a single forum topic only (not the whole group)
- Skips files that are already downloaded (safe to stop and resume anytime)
- Organizes downloads into `downloads/<chat_id>/topic_<topic_id>/`
- Minimal dependencies, single script, easy to read and modify

## Requirements

- Python 3.8+
- A Telegram account
- Telegram API credentials (`api_id` and `api_hash`) — free, from [my.telegram.org/apps](https://my.telegram.org/apps)

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/<your-username>/restricted-video_downloader.git
   cd restricted-video_downloader
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Get your Telegram API credentials**
   - Go to [https://my.telegram.org/apps](https://my.telegram.org/apps)
   - Log in with your Telegram account
   - Create a new application (any name/platform works — e.g. Platform: Desktop)
   - Copy the `api_id` and `api_hash` shown

5. **Create your config file**
   ```bash
   cp config.example.py config.py
   ```
   Open `config.py` and paste in your actual credentials:
   ```python
   API_ID = 12345678
   API_HASH = "your_actual_api_hash"
   ```
   > ⚠️ `config.py` is git-ignored — never commit your real credentials.

## Usage

```bash
python3 topic_downloader.py <chat_id> <topic_id>
```

### Finding your `chat_id` and `topic_id`

Open the topic in Telegram Web (`web.telegram.org/a/` or `/k/`) and look at the URL:
```
https://web.telegram.org/a/#-1002320221806_1489
                            └──────┬──────┘ └─┬─┘
                              chat_id      topic_id
```
Use the `chat_id` exactly as shown (including the `-100` prefix).

### Example

```bash
python3 topic_downloader.py -1002320221806 1489
```

This downloads all media from topic `1489` inside chat `-1002320221806` into:
```
downloads/-1002320221806/topic_1489/
```

### First run

On first run, you'll be asked to log in with your phone number and the OTP sent to your Telegram account. This creates a local session file (`topic_session.session`) so you won't need to log in again.

### Stopping and resuming

You can safely stop the script anytime with `Ctrl+C`. Files that were fully downloaded are skipped on the next run — only missing files are downloaded. If a download was interrupted mid-file, delete that partial file before resuming to avoid a corrupted/incomplete copy.

## Project structure

```
restricted-video_downloader/
├── topic_downloader.py     # main script
├── config.example.py       # credential template (safe to commit)
├── config.py                # your real credentials (gitignored, not committed)
├── requirements.txt         # dependencies
├── .gitignore
└── README.md
```

## Notes

- This tool only accesses topics/chats your own Telegram account already has access to — it does not bypass any privacy or access restrictions.
- Keep your `api_id` / `api_hash` and `.session` file private; they act like login credentials for your account.

## License

MIT
