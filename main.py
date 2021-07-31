from Tools.StrTools import TableManipulator

process = TableManipulator()
process.read("data.txt")
with open("data.txt", "w+") as file:
    data = process.toKaTeX()
    file.write(data)
    file.close()
    print(data)
