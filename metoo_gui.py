'''
Create a user interface using Tkinter where users can explore what words people 
used on Twitter during the MeToo movement.
'''

import tkinter as tk
from PIL import Image, ImageTk
from dateutil.parser import parse
import basic_algorithm
import datetime

fields = 'Start date (MM/DD/YYYY):', 'End date (MM/DD/YYYY):'


def fetch_load(entries, root):
    '''
    Fetch the input start date and end date, and load the created plots on the 
    screan.

    Inputs:
        entries: a list of the content entered by the user.
        root: a tkinter.Tk() object for the GUI.
    '''

    start = entries[0]
    end = entries[1]
    start_entry = start[1].get()
    end_entry = end[1].get()

    try:
        format_str = '%m/%d/%Y'
        start_date = datetime.datetime.strptime(start_entry, format_str)
        end_date = datetime.datetime.strptime(end_entry, format_str)
        assert(end_date >= start_date)

        start1 = datetime.datetime(2017, 10, 30)
        end1 = datetime.datetime(2018, 2, 8)
        start2 = datetime.datetime(2020, 3, 4)
        end2 = datetime.datetime(2020, 3, 5)

        assert((start_date >= start1 and start_date <= end1 and \
                end_date >= start1 and end_date <= end1) \
               or (start_date >= start2 and start_date <= end2 \
                and end_date >= start2 and end_date <= end2))
    except:
        warning = tk.Toplevel()
        warning.geometry('250x150')
        warning_label = tk.Label(warning, 
                                 text="Invalid date(s). Please try again.",
                                 wraplength=0.9 * root.winfo_width(), 
                                 justify=tk.LEFT, fg="red")
        warning_label.place(relx=0.5, rely=0.5, anchor='center')
    else:
        basic_algorithm.main('cleandata.csv', start_date, end_date, n=25)
        new_root = tk.Toplevel()
        load1 = Image.open("wordcloud.png")
        load2 = Image.open("frequency_plot.png")
        load3 = Image.open("top_n_dataframe.png")
        resized_load1 = load1.resize((600, 375))
        resized_load2 = load2.resize((600, 375))
        resized_load3 = load3.resize((275, 750))
        render1 = ImageTk.PhotoImage(resized_load1)
        render2 = ImageTk.PhotoImage(resized_load2)
        render3 = ImageTk.PhotoImage(resized_load3)

        cv_width = render1.width() + render3.width()
        cv_height = max(render1.height(), render2.height(), render3.height())
        cv = tk.Canvas(new_root, bg='white', width=cv_width, height=cv_height)
        cv.create_image((0, 0), anchor='nw', image=render1)
        cv.create_image((0, 375), anchor='nw', image=render2)
        cv.create_image((600, 0), anchor='nw', image=render3)
        cv.pack()
        new_root.mainloop()


def create_entries(root, fields):
    '''
    Create input boxes on the screen that ask the user to input the values.

    Inputs:
        root: a tkinter.Tk() object for the GUI.
        fields: the inputs we want to ask from the user.

    Returns:
        entries: a list of tuples (field, entry) where field is what we ask 
            from the user and entry is the input of the user.
    '''

    entries = []
    y_pos = 0.5
    for field in fields:
        row = tk.Frame(root)
        text = tk.Label(row, width=20, text=field, anchor='w')
        entry = tk.Entry(row)
        row.place(relx=0.05, rely=y_pos)
        text.pack(side=tk.LEFT)
        entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, entry))
        y_pos += 0.08

    return entries


if __name__ == '__main__':
    '''
    The main program that creates Tkinter interface and load relevant text and
    buttons of the interface. 
    '''

    root = tk.Tk()
    root.geometry('600x700')
    root.update()
    title = 'What did People Say about MeToo?'
    label1 = tk.Label(root, text=title, wraplength=0.9 * root.winfo_width(), 
        font=("MS Serif", 20, 'bold'), fg="forest green", justify=tk.LEFT)
    label1.place(relx=0.5, rely=0.02, anchor=tk.CENTER)
    intro_text = "This GUI is designed as a tool for studying how the " + \
        "MeToo movement developed on social media.\nChoose a start date" + \
        " and an end date for the time period that you want to study, then" + \
        " hit the show button below and explore what was said about the" + \
        " MeToo movement (in English) on Twitter during this time period." + \
        " The process could take a while since the dataset is large." +\
        "\nDue to data availability, the date could be between 10/30/2017" + \
        " and 02/08/2018, or between 03/04/2020 and 03/05/2020."
    label2 = tk.Label(root, text=intro_text,
                      wraplength=0.9 * root.winfo_width(), 
                      font=("Times", 16), bg='mint cream', 
                      fg="sea green", justify=tk.LEFT, relief=tk.RAISED)
    label2.place(relx=0.05, rely=0.08, anchor='nw')
    ents = create_entries(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch_load(e, root)))
    button_show = tk.Button(root, text='Show',
                   command=(lambda e=ents: fetch_load(e, root)), 
                   relief=tk.RAISED, bg='red')
    button_show.place(relx=0.05, rely=0.9)
    button_quit = tk.Button(root, text='Quit', command=root.quit,
                   relief=tk.RAISED, bg='red')
    button_quit.place(relx=0.2, rely=0.9)
    root.mainloop()
