# python -m libtorrentx -m magnet:?xt=urn:btih:4C9B41D664D7B6B23F0BF39AE185858CBADDA3FF

import modulepath
from libtorrentx import LibTorrentSession
import argparse


def callback(props, prefix=""):
    # do something with props
    print(prefix + props.string)


def main(args):
    session = LibTorrentSession()

    handle = session.add_torrent(args.magnet, args.output)

    handle.set_callback(callback, callback_interval=0.3)

    # use lambda to pass arguments to callback
    # handle.set_callback(lambda props: callback(props, prefix=">> "))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-m", "--magnet", help="torrent file path or magnet link", required=True
    )
    ap.add_argument("-o", "--output", help="download path", default="./downloads")
    args = ap.parse_args()

    main(args)
