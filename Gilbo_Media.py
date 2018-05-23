# Gilbo_Media is built using VLC's python interface.
# Using Gilbo_Media.py means you agree to their license.
from sys import path
path.append('./deps/')


class music_manager():
    def __init__(self, wait_time=5):
        self.music_dict = {'track': None, 'pause_position': [], 'looping': False, 'wait_time': wait_time}

    @property
    def track(self):
        return self.music_dict['track']

    @property
    def pause_pos(self):
        return self.music_dict['players']

    @property
    def looping(self):
        return self.music_dict['looping']

    @property
    def wait_time(self):
        return self.music_dict['wait_time']

    def init_track(self, filepath):
        try:
            self.stop()
        except AttributeError:
            pass

        from vlc import MediaPlayer
        p = MediaPlayer(filepath)
        self.music_dict['track'] = p

    def play(self):
        self.track.play()

    def play_loop(self):
        self.music_dict['looping'] = True

        def loop():
            from time import sleep
            self.track.play()
            sleep(self.wait_time)
            while self.looping is True:
                if self.track.is_playing() == 0:
                    self.track.stop()
                    self.track.play()
                sleep(self.wait_time)

        from threading import Thread

        loop_thread = Thread(target=loop)
        loop_thread.start()

    def pause(self):
        self.music_dict['pause_position'] = (self.track, self.track.get_time())

    def resume(self, command):
        self.init_track(self.pause_pos[0])
        self.track.set_time(self.pause_pos[1])

        command()

    def stop(self):
        if self.looping is True:
            self.music_dict['looping'] = False

        self.track.stop()
