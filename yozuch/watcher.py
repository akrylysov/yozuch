"""
Files/directories watcher.
"""

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from yozuch import logger


class DirectoryChangeHandler(FileSystemEventHandler):

    def __init__(self, command):
        self._command = command

    def on_any_event(self, event):
        if not event.is_directory:
            logger.info('{} changed'.format(event.src_path))
            self._command()


class FileChangeHandler(FileSystemEventHandler):

    def __init__(self, name, command):
        self._name = name
        self._command = command

    def dispatch(self, event):
        if not event.is_directory and event.src_path and os.path.basename(event.src_path) == self._name:
            self._command()


def watch(directory, command):
    observer = Observer()

    dirs = [
        os.path.join(directory, 'documents'),
        os.path.join(directory, 'posts'),
        os.path.join(directory, 'pages'),
        os.path.join(directory, 'themes'),
        os.path.join(directory, 'templates'),
        os.path.join(directory, 'assets'),
    ]
    dir_handler = DirectoryChangeHandler(command)
    for watch_dir in dirs:
        if os.path.isdir(watch_dir):
            logger.info('Watching {} for changes...'.format(watch_dir))
            observer.schedule(dir_handler, watch_dir, recursive=True)

    config_handler = FileChangeHandler('config.py', command)
    logger.info('Watching config.py for changes...')
    observer.schedule(config_handler, directory)

    observer.start()

    def stop():
        observer.stop()
        observer.join()

    return stop
