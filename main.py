import trio
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton


async def loop(app, event):
    app.lastWindowClosed.connect(event.set)

    while True:
        app.processEvents()
        with trio.move_on_after(0.01):
            await event.wait()
        if event.is_set():
            return


_nursery = None


def get_nursery():
    return _nursery


def async_bind(fn):
    def wrapper():
        get_nursery().start_soon(fn)


    return wrapper


async def say_hello():
    print('Hello')


async def main():
    app = QApplication([])

    widget = QWidget()
    layout = QHBoxLayout(widget)
    hello = QPushButton('Hello', widget)
    exit = QPushButton('Exit')
    layout.addWidget(hello)
    layout.addWidget(exit)
    widget.show()

    event = trio.Event()


    def on_exit():
        print('on_exit')
        event.set()


    hello.clicked.connect(async_bind(say_hello))
    exit.clicked.connect(on_exit)

    async with trio.open_nursery() as nursery:
        global _nursery
        _nursery = nursery
        nursery.start_soon(loop, app, event)


if __name__ == '__main__':
    trio.run(main)
