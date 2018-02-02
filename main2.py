import trio
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, qApp


async def say_hello():
    await trio.sleep(1)
    print('Hello 1')
    await trio.sleep(1)
    print('Hello 2')
    await trio.sleep(1)
    print('Hello 3')


async def loop(event):
    while not event.is_set():
        qApp.processEvents()
        with trio.move_on_after(0.01):
            await event.wait()


async def run_func_and_set_event(async_fn, event):
    try:
        return await async_fn()
    finally:
        event.set()


async def run_in_loop(async_fn):
    event = trio.Event()
    async with trio.open_nursery() as nursery:
        nursery.start_soon(run_func_and_set_event, async_fn, event)
        nursery.start_soon(loop, event)


def async_bind(async_fn):
    def inner():
        return trio.run(run_in_loop, async_fn)


    return inner


def main():
    app = QApplication([])

    widget = QWidget()
    layout = QHBoxLayout(widget)
    hello = QPushButton('Hello', widget)
    exit = QPushButton('Exit')
    layout.addWidget(hello)
    layout.addWidget(exit)
    widget.show()

    hello.clicked.connect(async_bind(say_hello))
    exit.clicked.connect(app.exit)

    app.exec_()


if __name__ == '__main__':
    main()
