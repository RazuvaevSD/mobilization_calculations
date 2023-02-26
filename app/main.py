from tkinter import Label

from app.core.config import WindowConf
from app.frames import MainMenu, TabControl, TabMenu, Window

app = Window()
app.title = WindowConf.TITLE.value,
app.geometry(WindowConf.SIZE.value)


###############################################################################
#                                  T E S T                                    #
###############################################################################

# Добавляем меню
main_menu = MainMenu()
main_menu.add_command(label='Открыть список документов')
app.config(menu=main_menu)

tab_control = TabControl(master=app.main_frame)


def foo(a):
    print('print test text', a)


def open_tab():
    tab = tab_control.add_tab(text='asdfasdf \n')
    menu = TabMenu(master=tab, bg='white')
    menu.add_btn(text='btn1', command=lambda: foo(1))
    menu.add_btn(text='btn2', command=lambda: foo(2))
    lbl_test = Label(master=tab, text='test_text', bg='white')
    lbl_test.pack()


# привяжем функцию открытия таба для списка документов
# т.к. она заранее предопределена
main_menu.entryconfigure(0, command=open_tab)



app.mainloop()
