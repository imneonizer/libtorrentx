import time
import threading
import traceback


class TorrentHandleWrapper:
    def __init__(self, session, handle, callback=None):
        self.session = session
        self.handle = handle
        self.callback = callback
        self.info_hash = str(self.handle.status().info_hash)
        self.save_path = self.handle.status().save_path
        self.start_callback()

    def start_callback(self):
        """Start callback thread"""
        self.stop_callback = False
        self.thread = None
        if self.callback:
            self.thread = threading.Thread(target=self.handle_callback)
            # self.thread.daemon = True
            self.thread.start()

    def handle_callback(self):
        """Handle callback, this can be used to update to db in the background"""
        while True:
            status, props = self.read(sleep=1)
            if not status:
                continue

            try:
                self.callback(props)
            except Exception:
                traceback.print_exc()

            if props.is_finished or self.stop_callback:
                break

    def __human_speed(self, speed):
        """Convert speed to human readable format

        Args:
            speed (int): speed in bytes

        Returns:
            str: human readable speed
        """

        if speed > 1024**3:
            return f"{round(speed / 1024 ** 3, 2)} GB/s"
        elif speed > 1024**2:
            return f"{round(speed / 1024 ** 2, 2)} MB/s"
        elif speed > 1024:
            return f"{round(speed / 1024, 2)} KB/s"
        else:
            return f"{round(speed, 2)} B/s"

    def props(self):
        """Get torrent properties

        Returns:
            dict: torrent properties
        """

        try:
            s = self.handle.status()
            name = self.handle.name() or "Unknown"
        except Exception as e:
            print(e)
            return {}

        return dict(
            info_hash=self.info_hash,
            name=name,
            download_speed=s.download_rate + 1,
            download_speed_human=self.__human_speed(s.download_rate),
            downloaded_bytes=s.total_wanted_done,
            is_finished=self.handle.is_finished(),
            is_paused=s.paused,
            num_connections=s.num_connections,
            num_peers=s.num_peers,
            num_seeds=s.num_seeds,
            num_trackers=len(self.handle.trackers()),
            progress=int(s.progress * 100),
            queue_position=s.queue_position,
            total_bytes=s.total_wanted,
            upload_speed=s.upload_rate,
            save_path=s.save_path,
        )

    def read(self, sleep=0):
        """Read torrent properties

        Args:
            sleep (int, optional): sleep time. Defaults to 0.

        Returns:
            tuple: (status, props)
        """

        if sleep:
            time.sleep(sleep)

        props = self.props()
        status = props.get("name", "Unknown") != "Unknown"
        return (status, props)

    def stop(self):
        """Stop torrent download

        Returns:
            bool: True if stopped
        """

        self.stop_callback = True
        self.session._stop(self.info_hash)

    def start(self):
        """Start torrent download

        Returns:
            bool: True if started
        """

        self.start_callback()
        self.handle = self.session.add_magnet_uri(
            f"magnet:?xt=urn:btih:{self.info_hash}", self.save_path
        )
        return self.handle

    def __repr__(self):
        return f"<{self.__class__.__name__} info_hash={self.info_hash}>"
