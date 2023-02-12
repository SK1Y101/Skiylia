# Rules to dictate token creation

string_chars = ['"', "'", "`"]

symbols = {
    # Special characters
    "\0": "EOF",
    "\n": "NEWLINE",
    "\t": "TAB",
    " ": "SPACE",
    # one char only
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "{": "LEFT_CURLY_BRACE",
    "}": "RIGHT_CURLY_BRACE",
    # two char
}

keywords = {""}
