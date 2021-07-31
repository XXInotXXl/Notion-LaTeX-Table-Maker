class InvalidInput(Exception):
    def __init__(self, message=""):
        super().__init__(message)


class TableManipulator:
    data: str = ""
    size: int = 0

    def read(self, file_path):
        def valid_size():
            self.size = len(self.data[0])
            return all([len(x) == self.size for x in self.data])

        self.data = open(file_path, "r").read().splitlines()
        for i in range(len(self.data)):
            self.data[i] = self.data[i].split("\t")
        print(self.data)
        if not valid_size():
            self.data = ""
            self.size = 0
            raise InvalidInput("Table Size Incorrect")

    def toKaTeX(self):
        def transform():
            for x in range(len(self.data)):
                for y in range(self.size):
                    temp = list(self.data[x][y])
                    for c in range(len(temp)):
                        if temp[c] in ["&", "%", "$", "#", "_", "{", "}"]:
                            temp[c] = "\\" + temp[c]
                        elif temp[c] == "~":
                            temp[c] = "\\textasciitilde "
                        elif temp[c] == "^":
                            temp[c] = "\\textasciicircum"
                        elif temp[c] == "\\":
                            temp[c] = "\\textbackslash"
                    self.data[x][y] = "".join(temp)

        transform()
        line = "\\hline\n"
        output = "\\begin{array}" + "{|" + "|".join(["c" for i in range(self.size)]) + "|}" + line
        for i in self.data:
            output = output + " & ".join(["\\text{" + x + "}" for x in i]) + "\\\\" + line
        output = output + "\end{array}"
        return output
