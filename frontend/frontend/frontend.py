import reflex as rx

from .pages import *

app: rx.App = rx.App(
	stylesheets=[
		"/footer.css"
	]
)
app.add_page(index)