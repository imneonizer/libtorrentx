import libtorrent as lt
from .torrent.store import TorrentStore
from .torrent.db import TorrentDB
from .torrent.record import TorrentRecord
from .torrent.callback import TorrentStatusCallbackLoop

import time
import re
import os
import glob


class TorrentClient(TorrentStatusCallbackLoop):
    def __init__(self, save_path="downloads"):
        self.save_path = save_path
        self.lt_session = lt.session()
        
        settings = self.lt_session.get_settings()
        settings['enable_outgoing_utp'] = False
        settings['enable_incoming_utp'] = False
        
        if hasattr(self.lt_session, "apply_settings"):
            self.lt_session.apply_settings(settings)
        else:
            self.lt_session.set_settings(settings)
        
        self.store = TorrentStore()
        super().__init__()
    
    def torrent2magnet(self, torrent_file):    
        info = lt.torrent_info(torrent_file)
        link = "magnet:?xt=urn:btih:%s&dn=%s" % (info.info_hash(), info.name())
        return link

    def get_info_hash(self, string):
        try:
            info_hash = re.findall(r"btih:.*", string)[0][5:45].lower()
            assert len(info_hash) == 40, "invalid magnet"
            return info_hash
        except Exception as e:
            print("error in get_info_hash:", e)

    def add_torrent(self, magnet, save_path=None, sequential=False):
        self.start_callback_loop()
        save_path = (save_path or self.save_path)
        info_hash = self.get_info_hash(magnet)
        if not info_hash: return
        
        if self.store.contains(info_hash):
            return TorrentRecord(info_hash, self.lt_session, self.store)

        try:
            save_path = os.path.realpath(os.path.join(save_path, info_hash))
            torrent = lt.add_magnet_uri(
                self.lt_session, magnet,
                {"save_path": save_path}
            )
            
            if sequential:
                torrent.set_sequential_download(sequential)
            
            info_hash = str(torrent.status().info_hash)
            db = TorrentDB(save_path)
            db.set(dict(
                added_time=int(time.time()),
                info_hash=info_hash,
                save_path=save_path
            ), overwrite=True)

            self.store.add(info_hash, db)
            return TorrentRecord(info_hash, self.lt_session, self.store, db)
        except Exception as e:
            print("Error from add_torrent:", str(e))

    def get_torrent(self, info_hash, save_path=None):
        save_path = (save_path or self.save_path)
        info_hash = info_hash.lower()
        
        if self.store.contains(info_hash):
            return TorrentRecord(info_hash, self.lt_session, self.store)

        db = TorrentDB(os.path.join(save_path, info_hash))
        if db.get('info_hash'):
            return TorrentRecord(info_hash, self.lt_session, self.store, db)

    def active_torrents(self):
        torrents = []
        for h in self.store.all().keys():
            torrents.append(TorrentRecord(h, self.lt_session, self.store))
        return torrents

    def get_torrents_from_path(self, save_path=None):
        save_path = (save_path or self.save_path)
        torrents = []
        for i in glob.glob(f"{save_path}/*/status.json"):
            db = TorrentDB(i)
            torrents.append(TorrentRecord(db.get('info_hash'),
                            self.lt_session, self.store, db))
        return torrents

    def close(self):
        self.stop_callback_loop()
