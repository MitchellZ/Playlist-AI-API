# Import PaLM API Key from cred.py
from bs4 import BeautifulSoup

import requests
from cred import palm_api_key, last_fm_api_key
from youtube_search import YoutubeSearch
import google.generativeai as palm

palm.configure(api_key = palm_api_key)

# Define a song class
class Song:
    def __init__(self, song, artist, song_link, album_art):
        self.song = song
        self.artist = artist
        self.song_link = song_link
        self.album_art = album_art

def search_youtube(query):
    results = YoutubeSearch(query + 'VEVO Audio', max_results=1).to_dict()
    # print(results)
    if results:
        # Get the id of the first result with a duration under 13 minutes
        video_id = None
        for result in results:
            # Under 13 minutes
            if result['duration'].count(':') == 1 and int(result['duration'].split(':')[0]) < 13:
                video_id = result['id']

        # print('Song located...')
        return video_id
    else:
        return None

def get_links(songs):

    songs_with_links = []

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

            # Add the song to the list
            songs_with_links.append(song_object)
        # No link found    
        else:
            # Remove the song
            songs.remove(song_object)
    
    return songs_with_links

def fetch_album_art(track_name, artist_name):
    # Assign API Key
    api_key = last_fm_api_key

    # Get only the first artist to increase reliability, delimited by commas
    if ',' in artist_name:
        artist_name = artist_name.split(',')[0]


    # Search for the track by title and artist
    search_url = f'http://ws.audioscrobbler.com/2.0/?method=track.search&track={track_name}&artist={artist_name}&api_key={api_key}&format=json'
    response = requests.get(search_url)
    data = response.json()

    # Check if the search returned any results
    if 'results' in data and 'trackmatches' in data['results'] and 'track' in data['results']['trackmatches']:
        tracks = data['results']['trackmatches']['track']
        
        # Check if any tracks were returned
        if tracks:
            # Get the first track result
            track = tracks[0]

            # Get the track's information
            track_name = track['name']
            artist_name = track['artist']

            # Get track info to retrieve an image
            track_info_url = f'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&track={track_name}&artist={artist_name}&api_key={api_key}&format=json'
            response = requests.get(track_info_url)
            track_info = response.json()

            # Check if track info contains image data
            if 'track' in track_info and 'album' in track_info['track'] and 'image' in track_info['track']['album']:
                images = track_info['track']['album']['image']
                # Get the largest available image (usually the last one)
                image_url = images[-1]['#text']
                return image_url
        else:
            return None
    else:
        return None

def get_art(songs):
    # Loop through each song in the list and iterate through the proxies by poping them off
    for song in songs:
        # Fetch the album art
        try:
            song.album_art = fetch_album_art(song.song, song.artist)
            # Assign the album art to the song object
            song.album_art = song.album_art
        except Exception as e:
            print('Error fetching album art.')

def generateText(prompt):
    system = "Act as a playlist generator. Respond to requests with a list of songs in the following format: '  * Song Title | Artist Names'. List the songs in a bulleted lists. Strict adherence to this format is required the song title must always come first followed by the artists seperated by a pipe symbol rather than the word 'by'. Multiple artists should be separated by a comma."

    completion = palm.generate_text(
    model='models/text-bison-001',
    prompt= system + ' ' + prompt,
    temperature=0.7,
    # The maximum length of the response
    max_output_tokens=800
    )

    return completion.result


def prompt(prompt):

    print('Generating playlist...')
    reply = generateText('I want to hear: ' + prompt + 'Please generate a playlist in the predefined format ("Title of the Song" | "Artist").')

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
                    print(song.lower())
                    if(song.lower() != 'title' and song.lower() != 'song title' and song.lower() != 'title of the song'):
                        # Define a song object
                        new_song = Song(song, artist, None, None)
                        # Add the song to the list
                        songs.append(new_song)
                        # print(song + ' - ' + artist)
    except Exception as e:
        print(e)
        return None

    # Print the number of songs
    print('Generated ' + str(len(songs)) + ' songs.')
    
    print('Sourcing links...')
    songs = get_links(songs)

    # Print the number of songs
    print('Found ' + str(len(songs)) + ' links.')

    print('Sourcing cover art...')
    song = get_art(songs)
    print('Done.')



    # Create a link to a preview of the playlist
    playlist_link = 'https://www.youtube.com/watch_videos?video_ids='

    for song in songs:
        link = song.song_link
        # Remove preface to isolate the video id
        link = link.replace('https://www.youtube.com/watch?v=', '')
        # Ad video to playlist preview link
        playlist_link += link + ','
    
    # Remove the last comma
    playlist_link = playlist_link[:-1]

    print('\nPlaylist preview: ' + playlist_link + '\n')

    # Convert songs to JSON format using __dict__
    songs = [song.__dict__ for song in songs]

    # TODO: Create a YouTube Playlist using this format: https://www.youtube.com/watch_videos?video_ids=fOe8aEqoN_M,qfZ2P2sWLZw,cew0MuXESGw,1bLlmKzIx0A,CZzcVs8tNfE,O4nHFQMeGo8

    return songs