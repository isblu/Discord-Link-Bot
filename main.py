import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import requests

# Replace with your bot token
BOT_TOKEN = 'insert_bot_token_from_discord'

# Channel IDs
SOURCE_CHANNEL_ID = 0 # Replace with the ID of the channel where links are posted
TARGET_CHANNEL_ID = 0  # Replace with the ID of the channel to forward combined links

# Define intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Temporary storage for links
link_storage = {
    "Twitch": "https://www.twitch.tv/your_user_name",  # Placeholder for link from platform 1
    "Youtube": None,  # Placeholder for link from platform 2
    "Kick": "https://kick.com/your_user_name",  # Placeholder for link from platform 3
    "FaceBook": "https://web.facebook.com/your_user_name"
}

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author.bot:
        return

    # Check if the message is in the source channel
    if message.channel.id == SOURCE_CHANNEL_ID:
        # Identify the platform based on the message or bot name
        platform = identify_platform(message)

        if platform and link_storage.get(platform) is None:
            # Extract the link from the message
            link = extract_link(message.content)
            if link:
                link_storage[platform] = link  # Store the link
                print(f"Stored link for {platform}: {link}")
                print(link_storage)
                # Check if all links are collected
                if all(link_storage.values()):
                    # Format and send the combined message
                    await forward_combined_links()
                    # Clear the storage for the next batch
                    clear_storage()

async def forward_combined_links():
    # Format the message with all collected links
    Title = get_youtube_title(link_storage['Youtube'])
    formatted_message = (
        "🔗 *Stream Links*:\n"
        f"*_{Title}_*\n"
        f"🎥 YouTube: {link_storage['Youtube']}\n"
        f"🎥 Kick: {link_storage['Kick']}\n"
        f"🎥 Twitch: {link_storage['Twitch']}\n"
        f"🎥 FaceBook: {link_storage['FaceBook']}"
    )

    # Send to the target channel
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if target_channel:
        await target_channel.send(formatted_message)
        print("Forwarded combined links!")

def clear_storage():
    # Reset storage for the next batch of links
    for key in link_storage:
        link_storage[key] = None
    print("Cleared link storage for the next batch.")

def identify_platform(message):
    # Determine the platform based on the bot's name or message content
    if "Kick" in message.author.name or "kick" in message.content.lower():
        return "Kick"
    elif "Twitch" in message.author.name or "twitch" in message.content.lower():
        return "Twitch"
    elif "Youtube" in message.author.name or "youtube" in message.content.lower():
        return "Youtube"
    return None

def extract_link(message_content):
    # Find and return the first URL in the message
    words = message_content.split()
    for word in words:
        if word.startswith("http"):
            return word
    return None

def get_kick_title(stream_url):
    try:
        response = requests.get(stream_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            # Try to find the title in multiple places
            # 1. Look for meta tag (most common for titles)
            title_tag = soup.find("meta", property="og:title")
            if title_tag and "content" in title_tag.attrs:
                return title_tag["content"]

            # 2. Fall back to the <title> tag
            title = soup.find("title")
            if title:
                return title.text.strip()

            # 3. Fall back to specific Kick page structure (e.g., headings or other meta tags)
            heading = soup.find("h1")  # Example: main heading
            if heading:
                return heading.text.strip()
    except Exception as e:
        print(f"Error fetching Kick title: {e}")
    return "Title not found"

def get_youtube_title(video_url):
    # Extract the video ID from the URL
    video_id = video_url.split("v=")[-1]
    api_key = "google_api_key"  # Replace with your API key
    api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["snippet"]["title"]
    return "Title not found"

# Run the bot
bot.run(BOT_TOKEN)
