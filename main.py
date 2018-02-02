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


async def main():
    app = QApplication([])

    widget = QWidget()
    layout = QHBoxLayout(widget)
    hello = QPushButton('Hello', widget)
    exit = QPushButton('Exit')
    layout.addWidget(hello)
    layout.addWidget(exit)
    widget.show()
    if 0:
        def say_hello():
            print('Hello')
        hello.clicked.connect(say_hello)
        app.exec_()

    event = trio.Event()

    def on_exit():
        print('on_exit')
        event.set()

    exit.clicked.connect(on_exit)

    async def say_hello():
        print('Hello')

    async with trio.open_nursery() as nursery:
        nursery.start_soon(loop, app, event)

        def wrapper():
            nursery.start_soon(say_hello)

        hello.clicked.connect(wrapper)


if __name__ == '__main__':
    trio.run(main)
