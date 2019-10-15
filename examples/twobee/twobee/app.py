import random
import toga
from toga.style.pack import Pack, COLUMN, CENTER

HEADS = toga.Image('https://beeware.org/static/images/brutus-270.png')
TAILS = toga.Image('https://beeware.org/project/projects/libraries/toga/toga.png')
TOSS = toga.Image('https://beeware.org/project/projects/tools/cricket/cricket.png')
IMG_SIZE = toga.style.Pack(height=75, width=75)  # TODO be nice if didn't have to specify size


def build(_):
    coins = (toga.ImageView(HEADS, style=IMG_SIZE), toga.ImageView(TAILS, style=IMG_SIZE))
    announce = toga.Label(text="Pick and win if you get two")
    buttons = (
        toga.Button("Bee", on_press=lambda b: choose(True)),
        toga.Button("Not Bee", on_press=lambda b: choose(False))
    )
    content = toga.Box(children=[
            announce, 
            toga.Box(children=coins), 
            toga.Box(children=buttons)
        ],
        style=Pack(direction=COLUMN, padding=40, alignment=CENTER)
        )

    def choose(pick_heads):
        # TODO allow to pick either instead of disable
        buttons[0].enabled, buttons[1].enabled = (not pick_heads, pick_heads)

        speed = 0.08
        while speed < 0.5:
            coins[0].image, coins[1].image, announce.text = (TOSS, TOSS, "Come in spinner")
            yield speed
            coins[0].image, coins[1].image = [random.choice([HEADS, TAILS]) for _ in coins]
            yield speed
            speed = speed * 1.2

        is_mine = [(c.image == HEADS) == buttons[1].enabled for c in coins]
        announce.text = "You Win" if all(is_mine) else "Draw" if any(is_mine) else "I Win"
        yield 5  # TODO: put in loop so works continously

    return content


def main():
    return toga.App("TwoBee or not TwoBee", 'org.beeware.twobee', startup=build)
