import libtorrent as lt
import os
import re

class SessionUtils:
    def exist(self, info_hash):
        return bool(self.get_torrent_handle(info_hash))

    def get_torrent_handle(self, info_hash):
        for torrent_handle in self.session.get_torrents():
            if str(torrent_handle.info_hash()).strip().lower() == info_hash.strip().lower():
                return torrent_handle
    
    def stop(self, handle):
        if isinstance(handle, str) and self.exist(handle):
            self.session.remove_torrent(self.get_torrent_handle(handle))
            return True
        elif isinstance(handle, lt.torrent_handle):
            self.session.remove_torrent(handle)
            return True


class LibTorrentSession(SessionUtils):
    def __init__(self):
        super(LibTorrentSession, self).__init__()
        self.session = lt.session()
        settings = self.session.get_settings()
        settings.update({
            "enable_outgoing_utp": False,
            "enable_incoming_utp": False
        })
        
        if hasattr(self.session, "apply_settings"):
            self.session.apply_settings(settings)
        else:
            self.session.set_settings(settings)
        
        self.session.add_dht_router("router.utorrent.com", 6881)
        self.session.start_dht()
    
    def get_info_hash(self, magnet):
        if isinstance(magnet, str):
            info_hash = re.findall(r"btih:.*", magnet)[0][5:45].lower()
            assert len(info_hash) == 40, "invalid magnet"
            return info_hash

        elif isinstance(magnet, lt.torrent_handle):
            return str(magnet.status().info_hash)
    
    def add_magnet_uri(self, magnet, save_path, sequential=False):
        info_hash = self.get_info_hash(magnet)
        
        if os.path.basename(save_path) != info_hash:
            save_path = os.path.realpath(os.path.join(save_path, info_hash))
        os.makedirs(save_path, exist_ok=True)
        
        torrent_handle = lt.add_magnet_uri(self.session, magnet, {"save_path": save_path})
        torrent_handle.set_sequential_download(sequential)
        return torrent_handle