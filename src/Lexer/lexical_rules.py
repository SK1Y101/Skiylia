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
    # two char
}

keywords = {""}
