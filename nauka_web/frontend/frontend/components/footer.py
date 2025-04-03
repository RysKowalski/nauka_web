import reflex as rx

def load_version() -> str:
	with open('../version.txt', 'r') as plik:
		return plik.read()

def footer():
	return rx.box(
		rx.flex(
			rx.text.span(f"Wersja: {load_version()}", id="version"),
			rx.text(" | "),
			rx.el.a(
				rx.image(
					src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/github.svg",
					alt="GitHub",
					class_name="github-icon",
				),
				href="https://github.com/RysKowalski/nauka_web",
				target="_blank",
				class_name="repo-link",
			),
			align="center",
			justify="center",
			gap="0.5rem",
		),
		class_name="footer"
	)
