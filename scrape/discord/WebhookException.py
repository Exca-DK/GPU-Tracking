class EmbedsAmountExcedeed(Exception):
    def __init__(self) -> None:
       pass

    def __str__(self) -> str:
        return repr(f"Excedeed maximum amount of embeds")