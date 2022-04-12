import libtorrent as lt
from easydict import EasyDict
import shutil

class TorrentRecord:    
    def __init__(self, info_hash, lt_session, store, db=None):
        self.info_hash = info_hash
        self.lt_session = lt_session
        self.store = store
        self.db = self.store.get(info_hash) or db

    @property
    def props(self):
        meta = self.db.all()
        if (not self.store.contains(self.info_hash)) and meta.get('is_finished') == False and meta.get('is_paused') == False:
            self.db.set({'is_paused': True})
        return EasyDict(self.db.all())
    
    def read(self):
        props = self.props
        status = props.get('name', 'unknown').lower() != 'unknown'
        return (status, props)
    
    def pause(self):
        for t in self.lt_session.get_torrents():
            if str(t.status().info_hash).lower() == self.info_hash:
                self.lt_session.remove_torrent(t)
                self.store.remove(self.info_hash)
                self.db.set(dict(
                    download_speed=0,
                    is_paused=True,
                    num_connections=0,
                    num_peers=0,
                    num_seeds=0,
                    num_trackers=0,
                    upload_speed=0
                ))
                break

    def resume(self):
        torrent = lt.add_magnet_uri(
            self.lt_session,
            f"magnet:?xt=urn:btih:{self.info_hash}",
            {"save_path": self.props.save_path}
        )
        
        info_hash = str(torrent.status().info_hash)
        self.store.add(info_hash, self.db)
    
    def delete(self):
        for t in self.lt_session.get_torrents():
            if str(t.status().info_hash).lower() == self.info_hash:
                self.lt_session.remove_torrent(t)
        self.store.remove(self.info_hash)
        shutil.rmtree(self.props.save_path)
    
    @property
    def handle(self):
        for t in self.lt_session.get_torrents():
            if str(t.status().info_hash).lower() == self.info_hash:
                return t
    
    def __repr__(self):
        return str(self.info_hash)
