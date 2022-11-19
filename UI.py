import pyperclip
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Header, Input, Static


class MainMenu(App):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Select an option:", classes="center", id="toptext")
        yield Static(
            "Download info - Downloads info from Twitter in JSON form.",
            classes="center",
        )
        yield Static(
            "Download media from info - Looks at the URLs in the JSON files and then downloads their media.",
            classes="center",
        )
        yield Vertical(
            Button("Download info", id="info", variant="primary", classes="button"),
            Button(
                "Download media from info",
                id="download",
                variant="error",
                classes="button",
            ),
            classes="center",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)


class ChooseOption(App):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Select an option:", classes="center", id="toptext")
        yield Vertical(
            Button(
                "Tweets and retweets", name="1", variant="primary", classes="button"
            ),
            Button("Likes", name="2", variant="secondary", classes="button"),
            Button("Bookmarks", name="3", variant="primary", classes="button"),
            Button("Following", name="4", variant="secondary", classes="button"),
            classes="center",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(int(event.button.name))


class InputCode(App):
    def action_copy_text(self):
        pyperclip.copy(self.authorize_url)
        self.bell()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(
            f"Open this site (click to copy):\n[@click='copy_text()']{self.authorize_url}[/]",
            classes="center",
            id="toptext",
        )
        yield Static(
            "Input the code that you received here:", classes="center", id="lilpad"
        )
        yield Input(placeholder="Paste it here", id="input")
        yield Vertical(
            Button("PASTE", variant="secondary", classes="button", id="paste"),
            Button("CONFIRM", variant="primary", classes="button"),
            classes="center",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "paste":
            self.query_one(Input).value = pyperclip.paste()
        else:
            self.exit(self.query_one(Input).value)
