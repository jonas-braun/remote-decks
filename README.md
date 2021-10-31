# Remote Decks

A latency-aware DJ tool for remote collaborative music playing.

## Idea
When two or more people want to record or stream a DJ session together and are not in the same location, network latency makes them out of sync and thus a joint recording would be messy.

But the audio stream from a DJ set - in contrast to e.g. a remote orchestra rehearsal - is somewhat predictable and can be retroactively synched between devices without much loss of listening quality.

* Sync clocks between remote clients (already done using NTP on th OS)
* Send all user input from a client to all other connected clients. Include a timestamp.
* On the remote clients, act on the user input but account to the time lag from the transmission.

Example:
Alice presses the play button on her DJ deck. On her machine, the song starts playing immediately.
Bob receives the message 100ms later that Alice started playing the song. He starts playback of the same song but skips ahead 100ms. He hears somethinig different than Alice for 100ms but after that, the two audio playbacks are perfectly in sync.
A server is attached to the same events in "Streamer" mode. It sets it's internal clock comfortably behind Alice's and Bob's synchronous clocks, so it will have received every event before it has to act on it. The streamer creates a perfect version of the DJ set but with some latency.


## Installation

Depends on python3 and PyQt5

`pip install -r requirements.txt`

Uses `ffmpeg` to convert audio files.

Set up a RabbitMQ cluster for communication between clients.


## Run

Set some varibles in the shell environment:

`export AMQP_HOST="X.X.X.X"            # set your RabbitMQ IP
export RD_LIBRARY="/home/user/Music"  # set local path to music library`

Run the program with `./main`


## TODO

### Music Library
The clients need to have access to a common music library and pull songs that other clients have loaded into a deck.

### Headphone Logic
Any client can play songs only locally to pre-listen. Those events are not sent to the other clients.


