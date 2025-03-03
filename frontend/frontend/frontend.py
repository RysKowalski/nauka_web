import reflex as rx

from .pages import *

app: rx.App = rx.App(
	stylesheets=[
		"https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css",
		"/footer.css",
		"discord_login.css"
	]
)
app.add_page(index)