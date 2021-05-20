from elements import LogicAnd


class Menu:
    def __init__(self):
        pass

    def start(self):
        while True:
            conns = input("Enter connections: ")
            conns = list(map(int, conns.split()))
            el = LogicAnd(conns[0], conns[1])
            print(f"Result: {el.calculate_result()}")


menu = Menu()
menu.start()
