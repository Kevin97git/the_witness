import tarfile
from datetime import datetime
def dump(file_list: list[str], message=None):
    if message is None:
        message = 'pre-'+str(datetime.today()).split(' ')[0]
    if type(message) != str:
        message = repr(message)
    with tarfile.open(f'./update_package-{message}.tar.gz', mode='w:gz') as tar:
        for name in file_list:
            tar.add(name)
dump('.')