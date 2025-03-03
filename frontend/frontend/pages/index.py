import reflex as rx

from ..components import *

class State(rx.State):
    count: int = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

def index():
    return rx.hstack(
        discord_login(),
        footer(),
        spacing="4",
    )