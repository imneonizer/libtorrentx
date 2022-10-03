import time
from easydict import EasyDict
from loguru import logger
import libtorrent as lt

class TorrentHandleWrapper:
    def __init__(self, session, handle):
        self.session = session
        self.handle = handle
        self.info_hash = str(self.handle.status().info_hash)
        self.save_path = self.handle.status().save_path
    
    def props(self):        
        try:
            s = self.handle.status()
            name = self.handle.name() or "Unknown"
        except Exception as e:
            logger.error(e)
            return {}

        return EasyDict(
                info_hash=self.info_hash,
                name=name,
                download_speed=s.download_rate,
                downloaded_bytes=s.total_wanted_done,
                is_finished=self.handle.is_finished(),
                is_paused=s.paused,
                num_connections=s.num_connections,
                num_peers=s.num_peers,
                num_seeds=s.num_seeds,
                num_trackers=len(self.handle.trackers()),
                progress=int(s.progress*100),
                queue_position=s.queue_position,
                total_bytes=s.total_wanted,
                upload_speed=s.upload_rate,
                save_path=s.save_path
            )
    
    def read(self, sleep=0):
        if sleep:
            time.sleep(sleep)
        
        props = self.props()
        status = props.get('name', 'Unknown') != 'Unknown'
        return (status, props)
    
    def stop(self):
        logger.info("torrent removed")
        self.session.stop(self.info_hash)
    
    def start(self):
        logger.info("torrent added")
        self.handle = self.session.start(self.info_hash, self.save_path)

    def __repr__(self):
        return f"<{self.__class__.__name__} info_hash={self.info_hash}>"