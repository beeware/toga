import toga
import random

HEADS = toga.Image('https://beeware.org/static/images/brutus-270.png')
TAILS = toga.Image('https://beeware.org/project/projects/libraries/toga/toga.png')
TOSS = toga.Image('https://beeware.org/project/projects/tools/cricket/cricket.png')
IMG_SIZE = toga.style.Pack(height=75, width=75) # TODO be nice if didn't have to specify size


def build(app):
    coins = (toga.ImageView(HEADS, style=IMG_SIZE), toga.ImageView(TAILS, style=IMG_SIZE))
    announce = toga.Label(text="")
    buttons = (
        toga.Button("Two Bee", on_press=lambda b: choose(True)),
        toga.Button("Two Not Bee", on_press=lambda b: choose(False))
    )
    content = toga.Box(children=[announce, toga.Box(children=coins), toga.Box(children=buttons)],
                       style=toga.style.Pack(direction=toga.style.pack.COLUMN, padding=40, alignment=toga.style.pack.CENTER))

    def choose(pick_heads):
        # TODO allow to pick either instead of disable
        buttons[0].enabled, buttons[1].enabled = (not pick_heads, pick_heads)

        coins[0].image, coins[1].image, announce.text = (TOSS, TOSS, "Come in spinner")
        yield 2

        for coin in coins:
            coin.image = random.choice([HEADS, TAILS])
        is_mine = [(c.image == HEADS) == buttons[1].enabled for c in coins]
        announce.text = "You Win" if all(is_mine) else "Draw" if any(is_mine) else "I Win"
        yield 5  # TODO: put in loop so works continously

    return content


def main():
    toga.App("TwoBee or not TwoBee", 'org.beeware.twobee', startup=build).main_loop()
