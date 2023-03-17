# Spotify to Youtube 

### This is a simple script that allows you to transger your playist from Spotify to Youtube Music.
#### Feel Free to do pl if you have any good idea, plz follow basic commit rules.

## How to use

* You can just run main.py, if you have any missing package, it will tell you what to do next.

* User Guide/Steps
    * Get auth headers (headers_auth.json)
        * https://ytmusicapi.readthedocs.io/en/stable/setup.html#copy-authentication-headers
    * Get your Spotify playlist in csv format
        * Just run main.py, it will ask you to login and automatically download your Spotify playlist in csv format inside the playlist folder.
* Your YouTube playlist will be created in your YouTube Music library, and named as the Spotify playlist name.
    * based on {    }.csv
        * For example, if your Spotify playlist name is "Pikachu.csv", your YouTube playlist will be named as "Pikachu"

## More info about auth headers.json

* To run authenticated requests, set it up by first copying your request headers from an authenticated POST request in your browser.

* Open a new tab
    * Open the developer tools (Ctrl-Shift-I) and select the “Network” tab
    * Go to https://music.youtube.com and ensure you are logged in
    * Find an authenticated POST request. The simplest way is to filter by /browse using the search bar of the developer tools. If you don’t see the request, try scrolling down a bit or clicking on the library button in the top bar.

* Firefox
    * Verify that the request looks like this: Status 200, Method POST, Domain music.youtube.com, File browse?...
    * Copy the request headers (right click > copy > copy request headers)
* Chromium (Chrome/Edge)
    * Verify that the request looks like this: Status 200, Name browse?...
    * Click on the Name of any matching request. In the “Headers” tab, scroll to the section “Request headers” and copy everything starting from “accept: */*” to the end of the section

* for additional detail, please check https://ytmusicapi.readthedocs.io/en/stable/setup.html#copy-authentication-headers

## Installation

```py
pip install -r requirements.txt
```

## Usage

```py
python main.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## To do list
- [NTD] Add a GUI
- [Done] Fix a progress bar
- [Done] Add a way to download a playlist
- [IP] Add a way to do Youtube to Spotify
- more to come...

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
[**@Mai0313**](https://github.com/Mai0313/Spotify-to-Youtube)
[**Mai0313**](https://mai0313.com/)

## Dictory tree
```
.
├── README.md
├── .cache
│   └── it will be generated after you run main.py, and login into Spotify;
│       it is an open-source project, and API is from official Spotify API, nothing to worry about.
├── main.py
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── spotify.py
│   │   └── Main function to download Spotify playlist
│   └── ytmusic.py
│       └── Main function to upload Spotify playlist to Youtube Music
│   
```
