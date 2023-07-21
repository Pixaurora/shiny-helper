class Game:
    __slots__ = ('valid_input', 'api_name')

    valid_input: str
    api_name: str

    def __init__(self, valid_input, api_name) -> None:
        self.valid_input = valid_input
        self.api_name = api_name


sun_moon = Game('sm', 'sun-moon')
ultra_sun_ultra_moon = Game('usum', 'ultra-sun-ultra-moon')

gen_7_games: list[Game] = [sun_moon, ultra_sun_ultra_moon]
