

class CogValidator(validator.Validator):

    code = 1
    message = "-"

    def check(self) -> Iterable[str]:
        return []


