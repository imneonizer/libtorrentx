import threading
import time


class TorrentStatusCallbackLoop:
    def __init__(self, interval=1):
        self.interval = interval
        self.thread = None
        self.__stop_callback_loop = False
        self.start_callback_loop(force=True)
    
    def stop_callback_loop(self):
        self.__stop_callback_loop = True
        self.thread.join()
    
    def start_callback_loop(self, force=False):
        if not force and self.callback_loop_running:
            return
        
        if self.thread is not None:
            self.stop_callback_loop()
        
        self.__stop_callback_loop = False
        self.thread = threading.Thread(target=self.__callback_loop)
        self.thread.start()
    
    @property
    def callback_loop_running(self):
        return not self.__stop_callback_loop
        
    def __callback_loop(self):
        while True:
            if self.__stop_callback_loop:
                break

            try:
                for t in self.lt_session.get_torrents():
                    s = t.status()
                    info_hash = str(s.info_hash).lower()
                    db = self.store.get(info_hash)
                    if not db:
                        continue

                    db.set(dict(
                        download_speed=s.download_rate,
                        downloaded_bytes=s.total_wanted_done,
                        is_finished=t.is_finished(),
                        is_paused=s.paused,
                        name=t.name() if t.name() else "Unknown",
                        num_connections=s.num_connections,
                        num_peers=s.num_peers,
                        num_seeds=s.num_seeds,
                        num_trackers=len(t.trackers()),
                        progress=int(s.progress*100),
                        queue_position=t.queue_position(),
                        total_bytes=s.total_wanted,
                        upload_speed=s.upload_rate,
                        elapsed=time.time() - db.get('added_time', time.time())
                    ))

                    if t.is_seed():
                        db.set(dict(
                            download_speed=0,
                            is_finished=True,
                            is_paused=False,
                            num_connections=0,
                            num_peers=0,
                            num_seeds=0,
                            num_trackers=0,
                            upload_speed=0
                        ))
                        self.lt_session.remove_torrent(t)
                        self.store.remove(info_hash)
            except Exception as e:
                print("error in callback_loop:", e)

            time.sleep(self.interval)
