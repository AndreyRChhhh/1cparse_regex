from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pygubu
import win32gui, win32con
import os


os.environ['TCL_LIBRARY'] = os.getcwd()+r'\lib\tcl8.6'
os.environ['TK_LIBRARY'] = os.getcwd()+r'\lib\tk8.6'

# Get .exe with: pyinstaller --hidden-import pygubu.builder.ttkstdwidgets --onefile main.py
# or with: nuitka --exe --standalone --explain-imports --recurse-directory=C:\YOURPATH\Python\Python35\Lib\
#                                                           site-packages/pygubu --show-progress --standalone main.py


def callback():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("txt files", "*.txt"), ("all files", "*.*")))


class Application:
    def __init__(self, root):

        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('GUI_config.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('LabelFrame_1', root)
        builder.connect_callbacks(self)

    def callback1(self):
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        self.builder.get_object('Entry_2').delete(0,999)  # .insert(0,variable)
        self.builder.get_object('Entry_2').insert(0,root.filename)  # .insert(0,variable)
        in_file = root.filename

    def start_pr(self):
        my_file = self.builder.get_object('Entry_2').get()
        try:
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
        except:
                messagebox.showinfo("", "Файл не подходит")

        else:
            count = 0
            if not os.path.exists(dirname.group(1)):
                os.mkdir(dirname.group(1), mode=0o777)
            shet_count=0
            for line in rashshet:
                shet_count+=1
                f = open(os.getcwd() + r'\\' + dirname.group(1) + "\\" + line + ".txt", 'w')
                f.write(startfilet.group(0))
                f.write(line)
                if line in section[count]:
                    f.write("\nСекцияРасчСчет")
                    f.write(section[count])
                    f.write("КонецРасчСчет")
                count += 1

            doc_count = 0
            for doc in document:
                doc_count += 1
                for line in rashshet:
                    search_in_doc = re.search(line, doc, re.DOTALL | re.UNICODE)
                    if search_in_doc:
                        f = open(os.getcwd() + r'\\' + dirname.group(1) + "\\" + line + ".txt", 'a')
                        f.write("\nСекцияДокумент=")
                        f.write(doc)
                        f.write("КонецДокумента")
            for line in rashshet:
                f = open(os.getcwd() + r'\\' + dirname.group(1) + "\\" + line + ".txt", 'a')
                f.write("\nКонецФайла")

            messagebox.showinfo("", "Файлы помещены в: " + os.getcwd() + "\\" + dirname.group(1) + "\nВ файле найдено "
                                + str(doc_count) + " документов" + "\nОбработано счетов: " + str(shet_count))

if __name__ == '__main__':
    root = Tk()
    root.withdraw()

    root.title("Парсер 1С выписок на Python")
    frgrnd_wndw = win32gui.GetForegroundWindow();
    wndw_title = win32gui.GetWindowText(frgrnd_wndw);
    print(wndw_title)
    if wndw_title.endswith("main.exe"):
        win32gui.ShowWindow(frgrnd_wndw, win32con.SW_HIDE);
    app = Application(root)
    root.geometry("329x133")
    root.update()
    root.deiconify()
    root.mainloop()