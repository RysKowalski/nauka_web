import reflex as rx


def footer():
	return rx.fragment(
	rx.box(
		rx.box(
			rx.text.span("Wersja: \u0142adowanie...", id="version"),
			" | ",
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
			class_name="footer",
			text_align="center",
		)
	)
)