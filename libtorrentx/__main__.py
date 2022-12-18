# python -m libtorrentx -m magnet:?xt=urn:btih:4C9B41D664D7B6B23F0BF39AE185858CBADDA3FF

from libtorrentx import LibTorrentSession
import argparse


def main(args):
    session = LibTorrentSession()
    handle = session.add_magnet_uri(
        args.magnet,
        args.output,
        sequential=args.sequential,
    )

    while True:
        status, props = handle.read(sleep=1)
        if not status:
            continue

        print(f"{props['name']}, {props['download_speed_human']}, {props['progress']}%")

        if props["is_finished"]:
            break


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--magnet", help="torrent magnet link", required=True)
    ap.add_argument("-o", "--output", help="download path", default="./downloads")
    ap.add_argument(
        "-s", "--sequential", help="download sequentially", type=bool, default=False
    )
    args = ap.parse_args()

    main(args)
