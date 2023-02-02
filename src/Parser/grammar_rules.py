# Abstraction of the Skiylia grammar


class grammar:
    PREC_NONE = 0
    PREC_PRIMARY = 1

    """ Structures. """

    def expression(self):
        pass

    """ Raw Data types. """

    def number(self, value: float) -> None:
        value = self.current.literal  # type: ignore
        self.emitConstant(value)  # type: ignore
