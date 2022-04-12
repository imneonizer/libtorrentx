# python demo.py -m magnet:?xt=urn:btih:1C0AD4A6A8CF5E26B6E57C3129CFAE9F42807037

import libtorrentx
import time
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-m', '--magnet', help="torrent magnet link", required=True)
    ap.add_argument('-o', '--output', help="download path", default='./downloads')
    ap.add_argument('-s', '--sequential',
                    help="download sequentially", type=bool, default=False)
    args = ap.parse_args()

    client = libtorrentx.TorrentClient()
    torrent = client.add_torrent(
        args.magnet, args.output, sequential=args.sequential)

    if torrent:
        while True:
            status, props = torrent.read()
            if not status:
                continue
            print(
                f"{props.name}, {(props.download_speed+1) / 1e+6:.2f} MB/s, {props.progress}%")
            if props.is_finished:
                break
            time.sleep(1)

    client.close()

if __name__ == '__main__':
    main()