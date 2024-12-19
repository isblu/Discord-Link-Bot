# Discord-Link-Bot

This repository contains a Discord bot designed to automate the process of collecting and forwarding streaming links from multiple platforms (e.g., Twitch, YouTube, Kick, Facebook) to a designated channel in a formatted manner. The bot extracts links, retrieves stream titles (where applicable), and allows easy extensibility for adding or removing platforms.

## Purpose
The primary purpose of this bot is to:
- Collect stream links from various platforms as they are posted in a specific Discord channel.
- Combine these links into a single, formatted message.
- Forward the formatted message to another designated channel for easy sharing.

## Features
- Support for popular streaming platforms: Twitch, YouTube, Kick, and Facebook.
- Automated title fetching for YouTube and Kick streams.
- Easily configurable platform URLs and user-specific data.
- Extensible design to add or remove supported platforms.

---

## Prerequisites
To run this bot, you need:
1. **Python 3.8+**
2. The following Python libraries:
   - `discord.py`
   - `beautifulsoup4`

   Install them using:
   ```
   pip install discord
   ```
   ```
   pip install beautifulsoup4 
   ```
3. A **Discord bot token**
4. A **YouTube Data API v3 key**

---

## Setup Instructions

### 1. Getting API Keys

#### **Bot Token**
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application or select an existing one.
3. Navigate to the **Bot** tab and click "Add Bot."
4. Copy the **token** and paste it into the `BOT_TOKEN` field in the `main.py` file.
5. Give necessary permissions for the bot

#### **YouTube API Key**
1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the **YouTube Data API v3** for your project.
4. Generate an API key and paste it into the `get_youtube_title` function in the `main.py` file.

### 2. Configuring Channel IDs
1. Open Discord and enable **Developer Mode** from Settings > Advanced.
2. Right-click on the desired source channel and select "Copy ID." Paste it into the `SOURCE_CHANNEL_ID` field in the `main.py` file.
3. Do the same for the target channel and paste it into the `TARGET_CHANNEL_ID` field.

### 3. Updating Usernames and Links
Replace the placeholder usernames in `link_storage` with your own:
- For Twitch: `https://www.twitch.tv/your_user_name`
- For Kick: `https://kick.com/your_user_name`
- For Facebook: `https://web.facebook.com/your_user_name`

### 4. Running the Bot
#### Option 1: Run with Python

1. Save the file as `main.py`.
2. Run the bot using:
   ```bash
   python main.py
   ```
3. Ensure the bot is online and monitoring the source channel.

#### Option 2: Run with a `.bat` File

1. Create a `.bat` file (e.g., `linkbot.bat`) with the following content:
   ```bat
   @echo off
   python "path_to_main.py"
   pause
   ```
2. Replace `path_to_main.py` with the full path to your `main.py` file.
3. Double-click the `.bat` file to run the bot like an application.


---

## How to Extend

### Adding a New Platform
1. Add a new key to the `link_storage` dictionary with the platform name and its default link.
2. Update the `identify_platform` function to detect messages for the new platform based on keywords or bot names.
3. Optionally, implement a title-fetching function similar to `get_kick_title` or `get_youtube_title`.

### Removing a Platform
1. Delete the platform's key from the `link_storage` dictionary.
2. Remove any references to the platform in the `identify_platform` function.
3. Update the `forward_combined_links` function to exclude the platform from the final message.

---

## Notes
- Ensure that the bot has permission to read and send messages in the specified channels.
- Use a secure method to store sensitive information like the bot token and API keys (e.g., environment variables).
- Debug any issues by reviewing the bot's console output for error messages.

---

## License
This project is licensed under the MIT License. Feel free to modify and distribute it as needed.

---

For questions or contributions, feel free to open an issue or submit a pull request!
