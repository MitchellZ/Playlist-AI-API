# Import PaLM API Key from cred.py
import json
from cred import api_key

def initializeConversation():
    import google.generativeai as palm
    palm.configure(api_key = api_key)

    # Initialize thread
    system = "Act as a playlist generator. Respond to requests with a list of songs in the following format: Song | Artist. List the songs in a bulleted lists. Preferably these songs are available on YouTube. Strict adherence to this format is required the song title must always come first followed by the artists seperated by a pipe symbol rather than the word by. Multiple artists should be separated by a comma."

    PaLM = palm.chat(
        context=system,
        messages="Confirm ready.",
        model="models/chat-bison-001")
    
    # Return the bot
    return PaLM

# Define a song class
class Song:
    def __init__(self, song, artist, song_link, album_art):
        self.song = song
        self.artist = artist
        self.song_link = song_link
        self.album_art = album_art

def prompt(prompt):
    bot = initializeConversation()

    if (bot == None):
        return None
    
    reply = bot.reply('I want to hear: ' + prompt + 'Please generate a playlist in the pre-defined format.').last

    print(reply)

    # Playlist
    songs = []

    # Parse the songs and artists
    try:
        # Get each line of the reply split by a new line
            for line in reply.split('\n'):
                # Check if the line starts with a bullet point
                if (line.strip().startswith('*')):
                    # Remove the asterisks
                    line = line.replace('*', '')
                    # Remove any quotation marks and trim
                    line = line.replace('\"', '').strip()
                    # Get the song
                    song = line.split('|')[0].strip()
                    # Get the artist
                    artist = line.split('|')[1].strip()
                    # Ensure song is not header/example
                    if(song != 'Song'):
                        # Define a song object
                        song = Song(song, artist, None, None)
                        # Add the song to the list
                        songs.append(song)
                        print(line)
    except Exception as e:
        print(e)
        return None

    # Convert songs to JSON format using __dict__
    songs = [song.__dict__ for song in songs]

    return songs