import os
import sys
import git
import shutil
from fuse import FUSE, Operations


class Passthrough(Operations):
    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        partial = partial.lstrip("/")
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def readdir(self, path, fh):
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    # File methods
    # ============

    def open(self, path, flags):
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)


def git_mount(url):
    origin_path = os.getcwd()
    path = '../../../git_dir'
    os.mkdir(path)
    os.chdir(path)
    git.Repo.init()
    g = git.Git()
    g.pull(url)
    os.chdir(origin_path)
    return path


# git_mount('https://github.com/Anthony1128/Image_size')


def main(mountpoint, url):
    root = git_mount(url)
    FUSE(Passthrough(root), mountpoint, nothreads=True, foreground=True)
    if KeyboardInterrupt:
        shutil.rmtree(root)

if __name__ == '__main__':
    main(sys.argv[2], sys.argv[1])