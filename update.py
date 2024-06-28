from os import listdir, remove, rmdir, path
import tarfile as tf

def main():
    def f(members: list[tf.TarInfo]):
        for tarinfo in members:
            if path.exists(tarinfo.name):
                if tarinfo.isdir(): pass
                else: remove(tarinfo.name)
            yield tarinfo
    l = listdir('.')
    for filename in l:
        if filename.startswith('update_package') and tf.is_tarfile(filename):
            postfix = filename.split('.')[-1]
            mode = f'r:{postfix}' if postfix != 'tar' else 'r'
            with tf.open(filename, mode=mode) as tar:
                tar.extractall(members=f(tar))
main()