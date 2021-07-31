from Tools.StrTools import TableManipulator

process = TableManipulator()
process.read("data.txt")
with open("data.txt", "w+") as file:
    file.write(process.toKaTeX())
    file.close()
