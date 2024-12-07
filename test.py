import logging
import lyricsgenius
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your own Genius API key
GENIUS_API_KEY = 'A-r90LO2_LB45Rss-Yp36zhEmEfhga0fuQIOY57SgSBiYI6-1OY0rQniDlr6-J-u'
genius = lyricsgenius.Genius(GENIUS_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm your music lyrics bot. Type /lyrics <artist name> to get the lyrics of the artist's songs.")

async def get_lyrics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Ensure the user provided an artist name
    if not context.args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide an artist name. Use /lyrics <artist name>.")
        return

    artist_name = ' '.join(context.args)
    
    # Search for the artist's songs
    try:
        song = genius.search_song(artist_name)
        if song:
            title = song.title
            lyrics = song.lyrics
            url = song.url

            # Send the lyrics and a link to the song
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Here are the lyrics for {title}:\n\n{lyrics}\n\nRead more: {url}")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Sorry, I couldn't find lyrics for {artist_name}.")
    except Exception as e:
        logger.error(f"Error fetching lyrics: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred while fetching the lyrics. Please try again later.")

def main() -> None:
    """Start the bot."""
    # Replace with your Telegram bot token
    TELEGRAM_BOT_TOKEN = '7610724843:AAFTxP6XgK6w_Q_EvUWnDMEj4yTafXC2ilw'

    # Create the Application and pass it your bot's token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lyrics", get_lyrics))

    # Run the bot until you send a signal to stop it
    application.run_polling()

if __name__ == '__main__':
    main()
