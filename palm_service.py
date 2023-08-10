# Import PaLM API Key from cred.py
import json
from cred import api_key
from youtube_search import YoutubeSearch

def initializeConversation():
    import google.generativeai as palm
    palm.configure(api_key = api_key)

    # Initialize thread
    system = "Act as a playlist generator. Respond to requests with a list of songs in the following format: Title | Artist. List the songs in a bulleted lists. Preferably these songs are available on YouTube. Strict adherence to this format is required the song title must always come first followed by the artists seperated by a pipe symbol rather than the word 'by'. Multiple artists should be separated by a comma."

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

def search_youtube(query):
    results = YoutubeSearch(query + 'VEVO Audio', max_results=1).to_dict()
    if results:
        video_id = results[0]['id']
        # print('Song located...')
        return video_id
    else:
        return None

def get_links(songs):

    for song_object in songs:
        song = song_object.song
        artist = song_object.artist

        # Check if artist is unknown or anonymous ignore case
        if (artist.lower() == 'unknown' or artist.lower() == 'anonymous'):
            video_id = search_youtube(song + ' VEVO Audio')
        else:
            video_id = search_youtube(song + ' by ' + artist + ' VEVO Audio')
        
        if (video_id):
            song_object.song_link = 'https://www.youtube.com/watch?v=' + video_id
        # No link found    
        else:
            # Remove the song
            songs.remove(song_object)



def prompt(prompt):
    bot = initializeConversation()

    if (bot == None):
        return None
    
    reply = bot.reply('I want to hear: ' + prompt + 'Please generate a playlist in the predefined format ("Title" | "Artist").').last

    # print(reply)

    # Playlist
    songs = []

    count = 0

    # Parse the songs and artists
    try:
        # Get each line of the reply split by a new line
            for line in reply.split('\n'):
                # Check if the line starts with a bullet point
                if (line.strip().startswith('*')):
                    count += 1
                    if count > 20:
                        break
                    # Remove the asterisks
                    line = line.replace('*', '')
                    # Remove any quotation marks and trim
                    line = line.replace('\"', '').strip()
                    # Get the song
                    song = line.split('|')[0].strip()
                    # Check if the song is prefaced with 'Title:'
                    if(song.startswith('Title:')):
                        # Remove the 'Title:'
                        song = song.replace('Title:', '').strip()
                    # Get the artist
                    artist = line.split('|')[1].strip()
                    # Ensure song is not header/example
                    if(song != 'Title'):
                        # Define a song object
                        new_song = Song(song, artist, None, None)
                        # Add the song to the list
                        songs.append(new_song)
                        print(song + ' by ' + artist)
    except Exception as e:
        print(e)
        return None
    
    get_links(songs)

    # Convert songs to JSON format using __dict__
    songs = [song.__dict__ for song in songs]

    return songs