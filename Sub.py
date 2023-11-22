specialcharacters = [
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "`",
    "{",
    "|",
    "}",
    "~",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]

substitutions = [
    ("let's", "let us"),
    #
    ("can't", "cannot"),
    ("don't", "do not"),
    ("doesn't", "does not"),
    ("ain't", "aint"),
    ("isn't", "is not"),
    ("aren't", "are not"),
    ("wasn't", "was not"),
    ("weren't", "were not"),
    ("haven't", "have not"),
    ("hasn't", "has not"),
    ("hadn't", "had not"),
    ("won't", "will not"),
    ("wouldn't", "would not"),
    ("shouldn't", "should not"),
    ("couldn't", "could not"),
    ("mustn't", "must not"),
    ("shan't", "shall not"),
    #
    ("i'm", "i am"),
    ("it's", "it is"),
    ("he's", "he is"),
    ("she's", "she is"),
    ("they're", "they are"),
    ("you're", "you are"),
    #
    ("i'll", "i will"),
    ("it'll", "it will"),
    ("he'll", "he will"),
    ("she'll", "she will"),
    ("they'll", "they will"),
    ("you'll", "you will"),
    ("we'll", "we will"),
    #
    ("i've", "i have"),
    ("they've", "they have"),
    ("you've", "you have"),
    ("we've", "we have"),
    #
    ("i'd", "i would"),
    ("it'd", "it would"),
    ("he'd", "he would"),
    ("she'd", "she would"),
    ("you'd", "you would"),
    #
    ("y'all", "you all"),
    ("in'", "ing"),
    ("'t", "it "),
    #
    ("o'clock", "oclock"),
    #
    ("'s", ""),
]


def substitute(str):
    ret = str
    for x, y in substitutions:
        ret = ret.replace(x, y)
    for sc in specialcharacters:
        ret = ret.replace(sc, " ")
    return ret
