class LogicAnd:
    def __init__(self, conn1, conn2):
        self.conn1 = conn1 if conn1 is not None else None
        self.conn2 = conn2 if conn2 is not None else None

    def calculate_result(self):
        return self.conn1 * self.conn2

if __name__ == "__main__":
    c1 = 0
    c2 = 1
    el = LogicAnd(c1, c2)
    print(el.calculate_result())