### LibtorrentX

A python wrapper for libtorrent, makes it easy to manage torrents. Built in support for state management and state recovery after restart.

- Easily pause and resume your torrent streams.
- Optimized settings for faster download speeds.

**Install via pip**

````sh
pip install libtorrentx
````

**Simple demo app**

````python
from libtorrentx import LibTorrentSession
import time

magnet = "magnet:?xt=urn:btih:4C9B41D664D7B6B23F0BF39AE185858CBADDA3FF"
output_dir = "./downloads"
session = LibTorrentSession()
handle = session.add_torrent(magnet, output_dir)

if handle:
    while True:
        status, props = handle.read()
        if not status:
            time.sleep(1)
            continue

        print(f"{props['name']}, {props['download_speed_human']}, {props['progress']}%")
        if props['is_finished']: break

        time.sleep(1)

````

or use CLI `python -m libtorrentx -m magnet:?xt=urn:btih:4C9B41D664D7B6B23F0BF39AE185858CBADDA3FF`

**Output**

````sh
Spider-Man.No.Way.Home.2022.1080p.BluRay.1600MB.DD5.1.x264-GalaxyRG[TGx], 1.20 MB/s, 19%
Spider-Man.No.Way.Home.2022.1080p.BluRay.1600MB.DD5.1.x264-GalaxyRG[TGx], 12.00 MB/s, 19%
Spider-Man.No.Way.Home.2022.1080p.BluRay.1600MB.DD5.1.x264-GalaxyRG[TGx], 28.11 MB/s, 77%
Spider-Man.No.Way.Home.2022.1080p.BluRay.1600MB.DD5.1.x264-GalaxyRG[TGx], 29.00 MB/s, 100%
````

You can stop the execution and restart again, the download will resume from previous state.

**Install via Docker**

```sh
docker build . -t libtorrentx
```

````sh
docker run --rm -it -v $(pwd)/downloads:/app/downloads libtorrentx -m magnet:?xt=urn:btih:4C9B41D664D7B6B23F0BF39AE185858CBADDA3FF
````

