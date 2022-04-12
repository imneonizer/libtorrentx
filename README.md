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
import libtorrentx
import time

magnet = "magnet:?xt=urn:btih:1C0AD4A6A8CF5E26B6E57C3129CFAE9F42807037"
output_dir = "./downloads"
client = libtorrentx.TorrentClient()
torrent = client.add_torrent(magnet, output_dir)

if torrent:
    while True:
        status, props = torrent.read()
        if not status: continue
        print(f"{props.name}, {(props.download_speed+1) / 1e+6:.2f} MB/s, {props.progress}%")
        if props.is_finished: break
        time.sleep(1)

client.close()
````

or use CLI `python -m libtorrentx -m magnet:?xt=urn:btih:1C0AD4A6A8CF5E26B6E57C3129CFAE9F42807037`

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
docker run --rm -it -v $(pwd)/downloads:/app/downloads libtorrentx -m magnet:?xt=urn:btih:1C0AD4A6A8CF5E26B6E57C3129CFAE9F42807037
````

