import reflex as rx

def discord_login():
	return rx.fragment(
    rx.box(
        rx.box(
            rx.el.a(
                rx.image(
                    src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/discord.svg",
                    alt="Discord",
                    class_name="discord-icon me-2",
                ),
                rx.text.span("Zaloguj si\u0119"),
                href="https://discord.com/oauth2/authorize?client_id=1337921140949254154&redirect_uri=http://localhost:8000/auth/callback&response_type=code&scope=identify",
                class_name="align-items-center d-flex text-decoration-none",
                color="#ffffff",
            ),
            id="discord-login",
            class_name="align-items-center d-md-flex d-none end-0 position-absolute",
            margin="0.75rem",
            padding="0.5rem",
            border_radius="0.25rem",
            top="0",
        ),
        rx.box(
            rx.el.a(
                rx.image(
                    src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/discord.svg",
                    alt="Discord",
                    class_name="discord-icon me-2",
                ),
                rx.text.span("Zaloguj si\u0119"),
                href="https://discord.com/oauth2/authorize?client_id=1337921140949254154&redirect_uri=http://localhost:8000/auth/callback&response_type=code&scope=identify",
                class_name="align-items-center btn btn-primary d-flex justify-content-center",
            ),
            id="discord-login-mobile",
            class_name="d-md-none",
            margin_top="0.75rem",
            text_align="center",
        ),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        padding_top="1rem",
        padding_bottom="1rem",
    )
)
