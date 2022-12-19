# Rules to dictate token creation

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
}
