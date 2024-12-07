
import requests
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Your Genius API credentials
GENIUS_API_TOKEN = 'A-r90LO2_LB45Rss-Yp36zhEmEfhga0fuQIOY57SgSBiYI6-1OY0rQniDlr6-J-u'  # Replace with your Genius API token

# Your Telegram bot token
TELEGRAM_API_TOKEN = '7610724843:AAFTxP6XgK6w_Q_EvUWnDMEj4yTafXC2ilw'  # Replace with your Telegram bot token

# Function to get song information from Genius API
def get_songs(artist_name):
    search_url = f"https://api.genius.com/search?q={artist_name}"
    headers = {'Authorization': f'Bearer {GENIUS_API_TOKEN}'}
    response = requests.get(search_url, headers=headers)
    data = response.json()
    
    songs = []
    for hit in data['response']['hits'][:3]:  # Limit to the first 3 songs
        song_title = hit['result']['title']
        song_artist = hit['result']['primary_artist']['name']
        song_url = hit['result']['url']
        song_image = hit['result']['header_image_url']
        
        songs.append({
            'title': song_title,
            'artist': song_artist,
            'url': song_url,
            'image': song_image
        })
    
    return songs

# Function to start the bot and fetch songs based on user input
async def start(update, context):
    await update.message.reply_text("Welcome! Type /songs [artist name] to get the first 3 songs of an artist.")

# Command to fetch and display songs for an artist
async def get_artist_songs(update, context):
    artist_name = ' '.join(context.args)
    
    if not artist_name:
        await update.message.reply_text("Please provide an artist name. Example: /songs Kendrick Lamar")
        return
    
    songs = get_songs(artist_name)
    
    if not songs:
        await update.message.reply_text(f"Sorry, no songs found for {artist_name}")
        return

    keyboard = [
        [InlineKeyboardButton(f"🎶 {song['title']} by {song['artist']}", url=song['url'])]
        for song in songs
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send song titles as buttons
    await update.message.reply_text(f"Here are the top 3 songs by {artist_name}:", reply_markup=reply_markup)

# Main function to run the bot
def main():
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("songs", get_artist_songs))
    
    application.run_polling()

if __name__ == '__main__':
    main()