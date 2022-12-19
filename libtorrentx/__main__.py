# python -m libtorrentx -m magnet:?xt=urn:btih:4C9B41D664D7B6B23F0BF39AE185858CBADDA3FF

from libtorrentx import LibTorrentSession
import argparse
import time


def main(args):
    session = LibTorrentSession()

    handle = session.add_torrent(
        args.magnet,
        args.output,
        sequential=args.sequential,
    )

    while True:
        status, props = handle.read()
        if not status:
            time.sleep(1)
            continue

        name = props["name"]
        downloaded_bytes = handle.format_bytes(props["downloaded_bytes"])
        total_bytes = handle.format_bytes(props["total_bytes"])
        download_speed = handle.format_bytes(props["download_speed"])
        progress = props["progress"]
        num_seeds = props["num_seeds"]

        print(
            f"{name} - {downloaded_bytes}/{total_bytes} - {download_speed}/s - {num_seeds} Seeds - {progress}%"
        )

        if props["is_finished"]:
            break

        time.sleep(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-m", "--magnet", help="torrent file path or magnet link", required=True
    )
    ap.add_argument("-o", "--output", help="download path", default="./downloads")
    ap.add_argument(
        "-s", "--sequential", help="download sequentially", action="store_true"
    )
    args = ap.parse_args()

    main(args)
