import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv_file
import graph
import os

table_created = False
table = None
file_selected = None
file_fields = []
path_file = ""
highest_index = 0
open_file = None

def file_selector(frame,scrollx,scrolly,btn_close_file,btn_add,btn_up,btn_del,btn_plot):
    global table_created, table, file_selected,file_fields,path_file,highest_index, open_file
    archivo = filedialog.askopenfilename()
    if archivo:
        extension = os.path.splitext(archivo)[1]
        if extension == ".csv":
            
            print("Selected File:", archivo)
            path_file = archivo
            open_file = csv_file.CsvFile(archivo)
            if len(archivo) > 65:
                file_selected.set(archivo[:65])
            else:
                file_selected.set(archivo)
            data = open_file.select()
            if table_created:
                table.destroy()
            table = ttk.Treeview(frame,columns=data[0][0],xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
            table.column("#0",width=0,stretch=tk.NO)
            table.heading("#0",text="Index")
            scrollx.config(command=table.xview)
            scrolly.config(command=table.yview)
            for i in data[0][0]:
                table.heading(i,text=i)
                file_fields.append(i)
            table.pack(fill='both',expand=True)
            for i in range(len(data)):
                if i != 0:
                    table.insert("",tk.END,text=data[0][1][i-1],values=(data[i]))
                    if data[0][1][i-1] > highest_index:
                        highest_index = data[0][1][i-1]
            table_created = True
        else:
            tk.messagebox.showwarning(message="The file you chose is not csv", title="Alert")
    else:
        print("No file selected")
    toggle_buttons_state(btn_close_file,btn_add,btn_up,btn_del,btn_plot)

def toggle_buttons_state(button,button1,button2,button3,button4):
    global table_created
    state = button.cget('state')
    if state == 'active':
        delete_Table()
        table_created = False
        button.config(state='disabled')
        button1.config(state='disabled')
        button2.config(state='disabled')
        button3.config(state='disabled')
        button4.config(state='disabled')

    if table_created:
        button.config(state='normal')
        button1.config(state='normal')
        button2.config(state='normal')
        button3.config(state='normal')
        button4.config(state='normal')
        
def delete_Table():
    global table, file_selected,file_fields,open_file
    table.destroy()
    file_selected.set("")
    open_file = None
    file_fields = []

def open_modal(root):
    global file_fields,table
    entries = {}
    data = []
    dialog = tk.Toplevel(root)

    def get_values():
        global highest_index,open_file
        for key,entry in entries.items():
            data.append(entry.get())
        
        highest_index = highest_index+1
        open_file.insert(file_fields,data,highest_index)
        table.insert("",tk.END,text=highest_index,values=(data))
        dialog.destroy()        

    for i in file_fields:
        tk.Label(dialog, text="{}:".format(i)).pack()
        entry = tk.Entry(dialog,name=i.lower())
        entry.pack(padx=10)
        entries[i.lower()] = entry

    tk.Button(dialog, text="Save", command=get_values).pack(pady=10)

def get_selected_row(root,action):
    global table,file_fields
    entries = {}
    data = []
    selected_item = table.selection()  # Obtener el ítem seleccionado en el TreeView

    def update(dialog,index):
        for key,entry in entries.items():
            data.append(entry.get())
        table.item(selected_item,values=data)
        open_file.update(index,file_fields,data)
        dialog.destroy()

    if selected_item:  # Verificar si hay un ítem seleccionado
        if action == "del":
            value = table.item(selected_item)['text']  # Obtener los valores de la fila seleccionada
            open_file.delete(value)
            table.delete(selected_item)
            print("Row Deleted:", value)
        else:
            dialog = tk.Toplevel(root)
            index = table.item(selected_item)['text']
            values =  table.item(selected_item)['values']
            for i in range(len(file_fields)):
                current_data = tk.StringVar(value=values[i])
                tk.Label(dialog, text="{}:".format(file_fields[i])).pack()
                entry = tk.Entry(dialog,name=file_fields[i].lower(),textvariable=current_data)
                entry.pack(padx=10)
                entries[file_fields[i].lower()] = entry
            tk.Button(dialog, text="Update", command=lambda:update(dialog,index)).pack(pady=10)
    else:
        tk.messagebox.showwarning(message="First you must select a row", title="Alert")

def modal_plot(root):
    global file_fields
    dialog = tk.Toplevel(root)
    x_axis = tk.StringVar()
    y_axis = tk.StringVar()
    values = tk.StringVar()
    def get_radio_values(dialog,x,y,values,title):
        global open_file
        if x.get() == "" or y.get() == "" or values.get() == "":
            tk.messagebox.showwarning(message="You cannot leave any button empty", title="Alert")
        else:
            if x.get() == y.get() or values.get() == y.get() or x.get() == values.get():
                tk.messagebox.showwarning(message="None of the axes or data must be the same", title="Alert")
            else:
                dialog.destroy()
                graph.build_plot(open_file.df,x.get(),y.get(),values.get(),title)

    tk.Label(dialog,text="Name your plot",font=("bold")).pack()

    entry_title = tk.Entry(dialog)
    entry_title.pack()

    tk.Label(dialog,text="Select X axis",font=("bold")).pack()
    for i in file_fields:
        tk.Radiobutton(dialog,text=i,variable=x_axis,value=i).pack()

    tk.Label(dialog,text="Select Y axis",font=("bold")).pack()
    for i in file_fields:
        tk.Radiobutton(dialog,text=i,variable=y_axis,value=i).pack()

    tk.Label(dialog,text="Select the data to graph",font=("bold")).pack()
    for i in file_fields:
        tk.Radiobutton(dialog,text=i,variable=values,value=i).pack()
        
    tk.Button(dialog, text="End",command=lambda:get_radio_values(dialog,x_axis,y_axis,values,entry_title.get())).pack(pady=10)


def initGui():
    global file_selected,open_file

    root = tk.Tk()
    root.geometry("1200x500")
    root.title('Csv File Reader')

    file_selected = tk.StringVar()
    
    frame1 = tk.Frame(root)
    frame2 = tk.Frame(root)
    frame1.pack(fill='y',)
    frame2.pack(fill='both', expand=True)

    xscroll = tk.Scrollbar(frame2,orient='horizontal')
    xscroll.pack(side='bottom',fill='x')

    yscroll = ttk.Scrollbar(frame2,orient='vertical')
    yscroll.pack(side='right',fill='y')

    file_label = tk.Label(frame1,text="Current File: ")
    file_label.grid(column=1,row=0)

    file_label_value = tk.Label(frame1, textvariable=file_selected)
    file_label_value.grid(column=2, row=0)

    btn_add_row = tk.Button(frame1,text="Add",command=lambda:open_modal(root))
    btn_add_row.config(state="disabled")
    btn_add_row.grid(column=4,row=0,padx=5)

    btn_upd_row = tk.Button(frame1,text="Update",command=lambda:get_selected_row(root,"upd"))
    btn_upd_row.config(state="disabled")
    btn_upd_row.grid(column=5,row=0,padx=5)

    btn_del_row = tk.Button(frame1,text="Delete",command=lambda:get_selected_row(root,"del"))
    btn_del_row.config(state="disabled")
    btn_del_row.grid(column=6,row=0,padx=5)

    plot_button = tk.Button(frame1,text="Make Plot",command=lambda:modal_plot(root))
    plot_button.config(state="disabled")
    plot_button.grid(column=7,row=0,padx=5)

    btn_close_file = tk.Button(frame1,text="Close File",command=lambda:toggle_buttons_state(btn_close_file,btn_add_row,btn_upd_row,btn_del_row,plot_button))
    btn_close_file.config(state="disabled")
    btn_close_file.grid(column=3,row=0,padx=10)

    fileButton = tk.Button(frame1,text="Select file",command=lambda:file_selector(frame2,xscroll,yscroll,btn_close_file,btn_add_row,btn_upd_row,btn_del_row,plot_button))
    fileButton.grid(column=0,row=0,padx=10)

    btn_exit = tk.Button(frame1,text="Exit",bg="#FF9999",activebackground="red",command=root.destroy)
    btn_exit.grid(column=8,row=0,padx=10)

    root.mainloop()