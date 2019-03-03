import Tkinter as tk

class ExampleView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        cbframe = tk.Frame(self)
        cb1 = tk.Checkbutton(cbframe, text="Choice 1")
        cb2 = tk.Checkbutton(cbframe, text="Choice 2")
        cb3 = tk.Checkbutton(cbframe, text="Choice 3")

        cb1.pack(side="left", fill=None, expand=False)
        cb2.pack(side="left", fill=None, expand=False)
        cb3.pack(side="left", fill=None, expand=False)

        # this entry is for illustrative purposes: it
        # will force column 2 to be widget than a checkbutton
        e1 = tk.Entry(self, width=20)
        e1.grid(row=1, column=1, sticky="ew")

        # place our frame of checkbuttons in the same column
        # as the entry widget. Because the checkbuttons are
        # packed in a frame, they will always be "stuck"
        # to the left side of the cell.
        cbframe.grid(row=2, column=1, sticky="w")

        # let column 1 expand and contract with the
        # window, so you can see that the column grows
        # with the window, but that the checkbuttons
        # stay stuck to the left
        self.grid_columnconfigure(1, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    view = ExampleView(root)
    view.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x200")
    root.mainloop()