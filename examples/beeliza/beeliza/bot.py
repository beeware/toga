###########################################################################
# eliza.py
#
# A cheezy little Eliza knock-off by Joe Strout
# with some updates by Jeff Epler
# Hacked into a module and updated by Jez Higgins
# Updated and tweaked for PEP8 compliance by Russell Keith-Magee
#
# Original source: https://github.com/jezhiggins/eliza.py
#
# Used under the terms of the MIT Licence.
#
# Copyright (c) 2002-2017 JezUK Ltd, Joe Strout, Jeff Epler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
###########################################################################
import random
import re


class Eliza:
    ###########################################################################
    # reflections, a translation table used to convert things you say
    #    into things the computer says back, e.g. "I am" --> "you are"
    ###########################################################################
    REFLECTIONS = {
        "am": "are",
        "was": "were",
        "i": "you",
        "i'd": "you would",
        "i've": "you have",
        "i'll": "you will",
        "my": "your",
        "are": "am",
        "you've": "I have",
        "you'll": "I will",
        "your": "my",
        "yours": "mine",
        "you": "me",
        "me": "you",
    }

    ###########################################################################
    # RESPONSES, the main response table.  Each element of the list is a
    #  two-element list; the first is a regexp, and the second is a
    #  list of possible responses, with group-macros labelled as
    #  {0}, {1}, etc.
    ###########################################################################
    RESPONSES = [
        [
            re.compile(r"I need (.*)", re.IGNORECASE),
            [
                "Why do you need {0}?",
                "Would it really help you to get {0}?",
                "Are you sure you need {0}?",
            ],
        ],
        [
            re.compile(r"Why don\'?t you ([^\?]*)\??", re.IGNORECASE),
            [
                "Do you really think I don't {0}?",
                "Perhaps eventually I will {0}.",
                "Do you really want me to {0}?",
            ],
        ],
        [
            re.compile(r"Why can\'?t I ([^\?]*)\??", re.IGNORECASE),
            [
                "Do you think you should be able to {0}?",
                "If you could {0}, what would you do?",
                "I don't know -- why can't you {0}?",
                "Have you really tried?",
            ],
        ],
        [
            re.compile(r"I can\'?t (.*)", re.IGNORECASE),
            [
                "How do you know you can't {0}?",
                "Perhaps you could {0} if you tried.",
                "What would it take for you to {0}?",
            ],
        ],
        [
            re.compile(r"I am (.*)", re.IGNORECASE),
            [
                "Did you come to me because you are {0}?",
                "How long have you been {0}?",
                "How do you feel about being {0}?",
            ],
        ],
        [
            re.compile(r"I\'?m (.*)", re.IGNORECASE),
            [
                "How does being {0} make you feel?",
                "Do you enjoy being {0}?",
                "Why do you tell me you're {0}?",
                "Why do you think you're {0}?",
            ],
        ],
        [
            re.compile(r"Are you ([^\?]*)\??", re.IGNORECASE),
            [
                "Why does it matter whether I am {0}?",
                "Would you prefer it if I were not {0}?",
                "Perhaps you believe I am {0}.",
                "I may be {0} -- what do you think?",
            ],
        ],
        [
            re.compile(r"What (.*)", re.IGNORECASE),
            [
                "Why do you ask?",
                "How would an answer to that help you?",
                "What do you think?",
            ],
        ],
        [
            re.compile(r"How (.*)", re.IGNORECASE),
            [
                "How do you suppose?",
                "Perhaps you can answer your own question.",
                "What is it you're really asking?",
            ],
        ],
        [
            re.compile(r"Because (.*)", re.IGNORECASE),
            [
                "Is that the real reason?",
                "What other reasons come to mind?",
                "Does that reason apply to anything else?",
                "If {0}, what else must be true?",
            ],
        ],
        [
            re.compile(r"(.*) sorry (.*)", re.IGNORECASE),
            [
                "There are many times when no apology is needed.",
                "What feelings do you have when you apologize?",
            ],
        ],
        [
            re.compile(r"Hello(.*)", re.IGNORECASE),
            [
                "Hello... I'm glad you could drop by today.",
                "Hi there... how are you today?",
                "Hello, how are you feeling today?",
            ],
        ],
        [
            re.compile(r"I think (.*)", re.IGNORECASE),
            [
                "Do you doubt {0}?",
                "Do you really think so?",
                "But you're not sure {0}?",
            ],
        ],
        [
            re.compile(r"(.*) friend (.*)", re.IGNORECASE),
            [
                "Tell me more about your friends.",
                "When you think of a friend, what comes to mind?",
                "Why don't you tell me about a childhood friend?",
            ],
        ],
        [
            re.compile(r"Yes", re.IGNORECASE),
            ["You seem quite sure.", "OK, but can you elaborate a bit?"],
        ],
        [
            re.compile(r"(.*) computer(.*)", re.IGNORECASE),
            [
                "Are you really talking about me?",
                "Does it seem strange to talk to a computer?",
                "How do computers make you feel?",
                "Do you feel threatened by computers?",
            ],
        ],
        [
            re.compile(r"Is it (.*)", re.IGNORECASE),
            [
                "Do you think it is {0}?",
                "Perhaps it's {0} -- what do you think?",
                "If it were {0}, what would you do?",
                "It could well be that {0}.",
            ],
        ],
        [
            re.compile(r"It is (.*)", re.IGNORECASE),
            [
                "You seem very certain.",
                "If I told you that it probably isn't {0}, what would you feel?",
            ],
        ],
        [
            re.compile(r"Can you ([^\?]*)\??", re.IGNORECASE),
            [
                "What makes you think I can't {0}?",
                "If I could {0}, then what?",
                "Why do you ask if I can {0}?",
            ],
        ],
        [
            re.compile(r"Can I ([^\?]*)\??", re.IGNORECASE),
            [
                "Perhaps you don't want to {0}.",
                "Do you want to be able to {0}?",
                "If you could {0}, would you?",
            ],
        ],
        [
            re.compile(r"You are (.*)", re.IGNORECASE),
            [
                "Why do you think I am {0}?",
                "Does it please you to think that I'm {0}?",
                "Perhaps you would like me to be {0}.",
                "Perhaps you're really talking about yourself?",
            ],
        ],
        [
            re.compile(r"You\'?re (.*)", re.IGNORECASE),
            [
                "Why do you say I am {0}?",
                "Why do you think I am {0}?",
                "Are we talking about you, or me?",
            ],
        ],
        [
            re.compile(r"I don\'?t (.*)", re.IGNORECASE),
            ["Don't you really {0}?", "Why don't you {0}?", "Do you want to {0}?"],
        ],
        [
            re.compile(r"I feel (.*)", re.IGNORECASE),
            [
                "Good, tell me more about these feelings.",
                "Do you often feel {0}?",
                "When do you usually feel {0}?",
                "When you feel {0}, what do you do?",
            ],
        ],
        [
            re.compile(r"I have (.*)", re.IGNORECASE),
            [
                "Why do you tell me that you've {0}?",
                "Have you really {0}?",
                "Now that you have {0}, what will you do next?",
            ],
        ],
        [
            re.compile(r"I would (.*)", re.IGNORECASE),
            [
                "Could you explain why you would {0}?",
                "Why would you {0}?",
                "Who else knows that you would {0}?",
            ],
        ],
        [
            re.compile(r"Is there (.*)", re.IGNORECASE),
            [
                "Do you think there is {0}?",
                "It's likely that there is {0}.",
                "Would you like there to be {0}?",
            ],
        ],
        [
            re.compile(r"My (.*)", re.IGNORECASE),
            [
                "I see, your {0}.",
                "Why do you say that your {0}?",
                "When your {0}, how do you feel?",
            ],
        ],
        [
            re.compile(r"You (.*)", re.IGNORECASE),
            [
                "We should be discussing you, not me.",
                "Why do you say that about me?",
                "Why do you care whether I {0}?",
            ],
        ],
        [
            re.compile(r"Why (.*)", re.IGNORECASE),
            ["Why don't you tell me the reason why {0}?", "Why do you think {0}?"],
        ],
        [
            re.compile(r"I want (.*)", re.IGNORECASE),
            [
                "What would it mean to you if you got {0}?",
                "Why do you want {0}?",
                "What would you do if you got {0}?",
                "If you got {0}, then what would you do?",
            ],
        ],
        [
            re.compile(r"(.*) mother(.*)", re.IGNORECASE),
            [
                "Tell me more about your mother.",
                "What was your relationship with your mother like?",
                "How do you feel about your mother?",
                "How does this relate to your feelings today?",
                "Good family relations are important.",
            ],
        ],
        [
            re.compile(r"(.*) father(.*)", re.IGNORECASE),
            [
                "Tell me more about your father.",
                "How did your father make you feel?",
                "How do you feel about your father?",
                "Does your relationship with your father relate to your feelings today?",
                "Do you have trouble showing affection with your family?",
            ],
        ],
        [
            re.compile(r"(.*) child(.*)", re.IGNORECASE),
            [
                "Did you have close friends as a child?",
                "What is your favorite childhood memory?",
                "Do you remember any dreams or nightmares from childhood?",
                "Did the other children sometimes tease you?",
                "How do you think your childhood experiences relate to your feelings today?",
            ],
        ],
        [
            re.compile(r"(.*)\?", re.IGNORECASE),
            [
                "Why do you ask that?",
                "Please consider whether you can answer your own question.",
                "Perhaps the answer lies within yourself?",
                "Why don't you tell me?",
            ],
        ],
        [
            re.compile(r"quit", re.IGNORECASE),
            [
                "Thank you for talking with me.",
                "Good-bye.",
                "Thank you, that will be $150.  Have a good day!",
            ],
        ],
        [
            re.compile(r"(.*)", re.IGNORECASE),
            [
                "Please tell me more.",
                "Let's change focus a bit... Tell me about your family.",
                "Can you elaborate on that?",
                "Why do you say that {0}?",
                "I see.",
                "Very interesting.",
                "{0}.",
                "I see.  And what does that tell you?",
                "How does that make you feel?",
                "How do you feel when you say that?",
            ],
        ],
    ]

    ###########################################################################
    # reflect: take an input string, and reflect the direction of any
    # statments (i.e., "I think I'm happy" - > "you think you're happy")
    ###########################################################################
    def reflect(self, input):
        return " ".join(
            self.REFLECTIONS.get(word, word) for word in input.lower().split()
        )

    ###########################################################################
    # respond: take a string, a set of regexps, and a corresponding
    # set of response lists; find a match, and return a randomly
    # chosen response from the corresponding list.
    ###########################################################################
    def respond(self, input):
        # find a match among keys
        for pattern, responses in self.RESPONSES:
            match = pattern.match(input)
            if match:
                # Found a match; randomly choose a response,
                # and populate it with the captured regex group data.
                response = random.choice(responses).format(
                    *[self.reflect(group) for group in match.groups()]
                )

                # fix punctuation
                if response[-2:] == "?.":
                    response = response[:-2] + "."
                if response[-2:] == "??":
                    response = response[:-2] + "?"
                return response


if __name__ == "__main__":
    print("Talk to the program by typing in plain English, using normal upper-")
    print('and lower-case letters and punctuation.  Enter "quit" when done.')
    print("=" * 72)
    print("Hello. How are you feeling today?")

    s = ""
    bot = Eliza()
    while s != "quit":
        try:
            s = input("> ")
        except EOFError:
            s = "quit"
        except KeyboardInterrupt:
            print()
            s = "quit"

        while s[-1] in "!.":
            s = s[:-1]
        print(bot.respond(s))
