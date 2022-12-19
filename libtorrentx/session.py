import os
import re
import libtorrent as lt
from .magnet import MagnetUtils
from .handle import TorrentHandleWrapper


class LibTorrentSession(MagnetUtils):
    def __init__(self):
        super(LibTorrentSession, self).__init__()
        self.session = lt.session()

        settings = self.session.get_settings()
        settings.update(
            {
                "alert_mask": lt.alert.category_t.all_categories,
                "upload_rate_limit": 0,
                "connections_limit": 500,
                "enable_outgoing_utp": False,
                "enable_incoming_utp": False,
            }
        )

        self.session.apply_settings(settings) if hasattr(
            self.session, "apply_settings"
        ) else self.session.set_settings(settings)

    def _get_torrent_handle(self, info_hash):
        """Get torrent_handle from info_hash

        Args:
            info_hash (str): info_hash

        Returns:
            lt.torrent_handle: torrent_handle
        """

        for torrent_handle in self.session.get_torrents():
            if (
                str(torrent_handle.info_hash()).strip().lower()
                == info_hash.strip().lower()
            ):
                return torrent_handle

    def _exist(self, info_hash):
        """Check if torrent exist in session

        Args:
            info_hash (str): info_hash

        Returns:
            bool: True if exist
        """

        return bool(self._get_torrent_handle(info_hash))

    def _get_info_hash(self, magnet):
        """Get info_hash from magnet uri or torrent_handle

        Args:
            magnet (str or lt.torrent_handle): magnet uri or torrent_handle

        Returns:
            str: info_hash
        """

        if isinstance(magnet, str):
            info_hash = re.findall(r"btih:.*", magnet)[0][5:45].lower()
            assert len(info_hash) == 40, "invalid magnet"
            return info_hash

        elif isinstance(magnet, lt.torrent_handle):
            return str(magnet.status().info_hash)

    def _stop(self, handle):
        """Stop torrent

        Args:
            handle (str or lt.torrent_handle): magnet link or torrent_handle

        Returns:
            bool: True if stopped
        """

        if isinstance(handle, str) and self._exist(handle):
            self.session.remove_torrent(self._get_torrent_handle(handle))
            return True
        elif isinstance(handle, lt.torrent_handle):
            self.session.remove_torrent(handle)
            return True

    def add_torrent(self, magnet, save_path, sequential=False, callback=None):
        """Add magnet link or torrent file to libtorrent session

        Args:
            magnet (str): magnet link or torrent file
            save_path (str): download path
            sequential (bool, optional): download sequentially. Defaults to False.

        Returns:
            TorrentHandleWrapper: TorrentHandleWrapper
        """

        if magnet.strip().lower().endswith(".torrent"):
            if not os.path.exists(magnet):
                raise FileNotFoundError(f"{magnet} not found")
            magnet = self._get_magnet_from_torrent_file(magnet)
        else:
            magnet = self._clean_magnet_uri(magnet)

        info_hash = self._get_info_hash(magnet)
        if self._exist(info_hash):
            return TorrentHandleWrapper(
                self, self._get_torrent_handle(magnet), callback
            )

        if os.path.basename(save_path) != info_hash:
            save_path = os.path.realpath(os.path.join(save_path, info_hash))
        os.makedirs(save_path, exist_ok=True)

        handle = lt.add_magnet_uri(self.session, magnet, {"save_path": save_path})
        handle.set_sequential_download(sequential)

        return TorrentHandleWrapper(self, handle, callback)
