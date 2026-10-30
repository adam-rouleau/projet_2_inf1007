class ErreurInputLongueurFilm(ValueError):
    def __init__(self, message:str):
        super().__init__(self, message)

class ErreurInputBudgetFilm(ValueError):
    def __init__(self, message:str):
        super().__init__(self, message)