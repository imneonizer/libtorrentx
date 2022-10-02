from .session import LibTorrentSession
from .handle import TorrentHandleWrapper
from loguru import logger

class TorrentClient:
    def __init__(self):
        self.lts = LibTorrentSession()
    
    def add_magnet(self, magnet, save_path="./downloads", sequential=False):
        info_hash = self.lts.get_info_hash(magnet)

        if self.lts.exist(info_hash):
            # return existing torrent_handler
            logger.warning("torrent already added")
            torrent_handle = self.lts.get_torrent_handle(info_hash)
            return TorrentHandleWrapper(self.lts, torrent_handle)

        else:
            # add new item to libtorrent session
            logger.info("torrent added")
            torrent_handle = self.lts.add_magnet_uri(magnet, save_path, sequential)
            return TorrentHandleWrapper(self.lts, torrent_handle)