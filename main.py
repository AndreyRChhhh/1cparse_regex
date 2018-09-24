from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pygubu
import os


def callback():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("txt files", "*.txt"), ("all files", "*.*")))


class Application:
    def __init__(self, root):

        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('test.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('LabelFrame_1', root)
        builder.connect_callbacks(self)

    def callback1(self):
        # print ("click!")
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        self.builder.get_object('Entry_2').delete(0,999)  # .insert(0,variable)
        self.builder.get_object('Entry_2').insert(0,root.filename)  # .insert(0,variable)
        in_file = root.filename

    def start_pr(self):
        my_file = self.builder.get_object('Entry_2').get()
        with open(my_file, 'r', encoding='cp1251') as read_file:
            fulltext = read_file.read()
            regex1 = r"РасчСчет=(.*?)СекцияРасчСчет"
            result1 = re.search(regex1, fulltext, re.DOTALL | re.UNICODE)

            regex1 = r"\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d\d"
            rashshet = re.findall(regex1, result1.group(1), re.DOTALL | re.UNICODE)

            regex1 = r"1CClientBankExchange(.*?)РасчСчет="
            startfilet = re.search(regex1, fulltext, re.DOTALL | re.UNICODE)

            regex1 = r"СекцияРасчСчет(.*?)КонецРасчСчет"
            section = re.findall(regex1, fulltext, re.DOTALL | re.UNICODE)

            regex1 = r"СекцияДокумент=(.*?)КонецДокумента"
            document = re.findall(regex1, fulltext, re.DOTALL | re.UNICODE)

            regex1 = r"ДатаНачала=(.*?)\nДатаКонца="
            dirname = re.search(regex1, fulltext, re.DOTALL | re.UNICODE)
            print(dirname.group(1))
        count = 0

        if not os.path.exists(dirname.group(1)):
            # os.makedirs(directory)
            os.mkdir(dirname.group(1), mode=0o777)

        for line in rashshet:
            f = open(os.getcwd()+r'\\'+dirname.group(1)+"\\"+line + ".txt", 'w')
            f.write(startfilet.group(0))
            f.write(line)
            if line in section[count]:
                f.write("\nСекцияРасчСчет")
                f.write(section[count])
                f.write("КонецРасчСчет")
            count += 1
            if line in document[count]:
                f.write("\nСекцияДокумент=")
                f.write(document[count])
                f.write("КонецДокумента")
            f.write("\nКонецФайла")
            # print("debug:")
            # print (document)
        messagebox.showinfo("","Файлы помещены в: "+os.getcwd()+"\\"+dirname.group(1) )


if __name__ == '__main__':
    root = Tk()
    root.title("Парсер 1С выписок на Python")
    app = Application(root)
    root.mainloop()