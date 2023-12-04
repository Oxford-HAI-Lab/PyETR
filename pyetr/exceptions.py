class OperationUndefinedError(ValueError):
    def __init__(self, message, *args: object) -> None:  # pragma: not covered
        super().__init__(message, *args)
