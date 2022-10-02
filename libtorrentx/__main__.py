# python demo.py -m magnet:?xt=urn:btih:4C9B41D664D7B6B23F0BF39AE185858CBADDA3FF

import libtorrentx
import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-m', '--magnet', help="torrent magnet link", required=True)
    ap.add_argument('-o', '--output', help="download path", default='./downloads')
    ap.add_argument('-s', '--sequential',
                    help="download sequentially", type=bool, default=False)
    args = ap.parse_args()

    client = libtorrentx.TorrentClient()
    torrent = client.add_magnet(args.magnet, args.output, sequential=args.sequential)
    
    while True:
        status, props = torrent.read(sleep=1)
        if not status:
            continue
        
        print(f"{props.name}, {(props.download_speed+1) / 1e+6:.2f} MB/s, {props.progress}%")
        
        if props.is_finished:
            break

if __name__ == '__main__':
    main()