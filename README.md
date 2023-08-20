# AI Playlist API

Welcome to the AI Playlist API, a work in progress API that harnesses the power of Google's Pathways Language Model (PaLM) to generate music playlists from user requests using natural language. This API serves as the backend for Apollo Music, providing the intelligence to create curated playlists based on natural language prompts.

Looking for a user-friendly way to interact with the AI Playlist API and explore the curated playlists? Check out [Apollo Music](https://github.com/MitchellZ/Apollo-Music), a front-end application that seamlessly integrates with this API to enhance your music discovery experience.

## Introduction

This API is designed to leverage the capabilities of Google's Pathways Language Model to generate music playlists that cater to user preferences expressed in natural language. It functions as an integral part of the Apollo Music project, enhancing the music discovery experience for users.

### Endpoints

1. **Ping Endpoint**
   - **Endpoint**: `/ping`
   - **Description**: Responds with a "pong" message, indicating the API's availability.

2. **Query Endpoint**
   - **Endpoint**: `/query`
   - **Description**: Takes a `message` parameter, which is used as the language model prompt to generate the playlist. The model follows specific instructions to ensure that the playlist can be parsed from the response.
   - **Response**: The API returns a JSON array of song objects, each with the following structure:
   
     ```json
     {
       "album_art": "https://lastfm.freetls.fastly.net/i/u/300x300/635c844d26acc4452f214b6780c78de1.png",
       "artist": "The Weeknd",
       "song": "Blinding Lights",
       "song_link": "https://www.youtube.com/watch?v=fHI8X4OXluQ"
     }
     ```

     If the language model fails to understand the request and the reply cannot be parsed, the message in the response will indicate: "Unable to generate playlist."

## Usage

1. **Ping Endpoint**: Use this endpoint to check if the API is up and running.

2. **Query Endpoint**: Send a `message` parameter with a natural language request in terms of a response to the question: "What you would like to hear?" The API will respond with a JSON array of song objects or an indication if the playlist could not be generated.
