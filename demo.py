from tkinter import Tk, filedialog


class InvalidInput(Exception):
    def __init__(self, message=""):
        super().__init__(message)


class Table:

    data: str = ""
    size: int = 0
    style: str = ""

    def read(self, file_path):
        self.data = open(file_path, "r").read().splitlines()
        if self.data[0].startswith("\\begin{array}") and self.data[-1].endswith("\\end{array}"):
            self.style = "KaTeX"
        else:
            self.style="table"

    def translate(self):

        def to_KaTeX():
            def valid_size():
                self.size = len(self.data[0])
                return all([len(x) == self.size for x in self.data])
            for i in range(len(self.data)):
                self.data[i] = self.data[i].split("\t")
            if not valid_size():
                self.data = ""
                self.size = 0
                raise InvalidInput("Table Size Incorrect")

            for x in range(len(self.data)):
                for y in range(self.size):

                    # split content letter by letter
                    temp = list(self.data[x][y])
                    # a stack for \text{} processing
                    stack = Stack()

                    for c in range(len(temp)):

                        # processing text inclosed by `` (\text{})
                        # check if exist `` charactor for \text{}
                        if temp[c] == "`":
                            stack.add(c)  # add the index of `
                        if stack.full():  # if a pair of `` exist
                            # pop the last index
                            temp[stack.pop()] = "}"
                            # pop the last index, where is the first index as well
                            temp[stack.pop()] = "\\text{"
                        
                        # when outside of ``
                        if stack.empty():
                            # check if exist letter violate KaTeX language
                            if temp[c] in ["&", "%", "$", "#"]:
                                temp[c] = "\\" + temp[c]
                            elif temp[c] == "~":
                                temp[c] = "\\textasciitilde "
                            # change blankspace tp \;
                            if temp[c] == " ":
                                temp[c] = "\\;"
                            if not temp[c].endswith(" "):
                                temp[c]=temp[c]+" "
                        
                        else: # inside of ``
                            # check if exist letter violate KaTeX language
                            if temp[c] in ["&", "%", "$", "#", "_", "{", "}"]:
                                temp[c] = "\\" + temp[c]
                            elif temp[c] == "~":
                                temp[c] = "\\textasciitilde "
                            elif temp[c] == "^":
                                temp[c] = "\\textasciicircum "
                            elif temp[c] == "\\":
                                temp[c] = "\\textbackslash "

                    # union the string back
                    self.data[x][y] = "".join(temp)

            line = "\\hline\n"
            output = "\\begin{array}" + " {| " + \
                " | ".join(["c" for i in range(self.size)]) + " |}" + line
            for i in self.data:
                output = output + " "+" & ".join(i) + "\\\\" + line
            output = output + "\end{array}"
            return output

        def to_table():
            output=self.data[0].split("\hline")
            for i in range(len(output)):
                output[i] = output[i].split(" & ")
            return output



        if self.style=="KaTeX":
            return to_table()
        elif self.style == "table":
            return to_KaTeX()

class PathSelector:
    def __init__(self):
        Tk().withdraw()

    def open_file(self, *args, **kwargs):
        return filedialog.askopenfilename(*args, **kwargs)

    def open_directory(self, *args, **kwargs):
        return filedialog.askdirectory(*args, **kwargs)


class Stack:

    stack = []

    def add(self, new):
        self.stack.append(new)

    def pop(self):
        return self.stack.pop()

    def full(self):
        return len(self.stack) == 2
    
    def empty(self):
        return len(self.stack) == 0


class Main():
    table = Table()
    table.read(PathSelector().open_file(filetypes=(('text files', '*.txt'),)))

    def exec(self):
        print(self.table.translate())


if __name__ == '__main__':
    Main().exec()
