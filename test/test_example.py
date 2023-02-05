from src import example


def test_add() -> None:
    example.add(1, 1) == 2


def test_mul() -> None:
    example.mul(2, 3) == 6
