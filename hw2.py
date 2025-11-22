class Move:
    def __init__(self, name: str, power: int, pp: int):
        if not isinstance(name, str):
            raise TypeError("Move name must be a string")
        if not isinstance(power, int) or power < 0:
            raise ValueError("Move power must be a non-negative integer")
        if not isinstance(pp, int) or pp <= 0:
            raise ValueError("Move pp must be a positive integer")

        self.name = name
        self.power = power
        self.max_pp = pp
        self.pp = pp

    def use(self):
        if self.pp <= 0:
            raise ValueError(f"No PP left for move {self.name}")
        self.pp -= 1


class Pokemon:
    def __init__(self, name: str, hp: int, attack: int, defense: int, speed: int, moves: dict[str, "Move"]):
        if not isinstance(name, str):
            raise TypeError("Pokemon name must be a string")
        for stat_name, stat_value in [("hp", hp), ("attack", attack), ("defense", defense), ("speed", speed)]:
            if not isinstance(stat_value, int) or stat_value < 0:
                raise ValueError(f"{stat_name} must be a non-negative integer")

        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = moves

    def is_fainted(self):
        return self.hp <= 0

    def get_move_names(self):
        return list(self.moves.keys())

    def use_move(self, move_name: str, target: "Pokemon"):
        if move_name not in self.moves:
            raise KeyError(f"{self.name} does not know {move_name}")
        move = self.moves[move_name]
        move.use()
        damage = max(1, move.power + self.attack - target.defense)
        target.hp = max(0, target.hp - damage)
        return damage


class Battle:
    def __init__(self, p1: Pokemon, p2: Pokemon):
        self.p1 = p1
        self.p2 = p2

    def order(self):
        if self.p1.speed > self.p2.speed:
            return (self.p1, self.p2)
        elif self.p2.speed > self.p1.speed:
            return (self.p2, self.p1)
        else:
            return (self.p1, self.p2) if self.p1.name < self.p2.name else (self.p2, self.p1)

    def turn(self, attacker_move: str, defender_move: str):
        first, second = self.order()
        move_first = attacker_move if first is self.p1 else defender_move
        move_second = defender_move if first is self.p1 else attacker_move

        first.use_move(move_first, second)
        first_actor_name = first.name

        if second.is_fainted():
            return (first_actor_name, None)

        second.use_move(move_second, first)
        second_actor_name = second.name

        return (first_actor_name, second_actor_name)

    def simulate(self, move_seq_p1: list[str], move_seq_p2: list[str]):
        i = 0
        while not self.p1.is_fainted() and not self.p2.is_fainted():
            if i >= len(move_seq_p1) or i >= len(move_seq_p2):
                raise ValueError("No move provided")
            self.turn(move_seq_p1[i], move_seq_p2[i])
            i += 1

        if self.p1.is_fainted() and not self.p2.is_fainted():
            return self.p2.name
        elif self.p2.is_fainted() and not self.p1.is_fainted():
            return self.p1.name
        else:
            return min(self.p1.name, self.p2.name)

