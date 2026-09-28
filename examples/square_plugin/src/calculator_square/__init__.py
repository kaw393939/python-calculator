class Square:
    name = "square"
    description = "Square one number"
    usage = "square NUMBER"

    def execute(self, *args: float, **kwargs: float) -> float:
        if len(args) != 1 or kwargs:
            raise ValueError("Usage: square NUMBER")
        return args[0] ** 2
