import tkinter
import tkinter as tk
from tkinter.messagebox import showinfo
from visualize import Visualizer
from scheme import Scheme


class SchemeGUI:
    """Encapsulate tkinter widgets and events functions"""

    def __init__(self, master: tkinter.Tk):
        self._master = master

        # configure main window
        self._master.title('L4Logic')
        self._master.resizable(width=False, height=False)

        # objects
        self.scheme = Scheme()

        # test scheme
        self.scheme.add_element('constant', 0, (1, 1),
                                constant_value=1)
        self.scheme.add_element('constant', 1, (1, 2),
                                constant_value=1)
        self.scheme.add_element('constant', 2, (1, 3),
                                constant_value=1)
        self.scheme.add_element('shifter', 3, (3, 1), num_bits=4)

        self.scheme.add_connection(0, 'out', 3, 'in2')
        self.scheme.add_connection(1, 'out', 3, 'in3')
        self.scheme.add_connection(2, 'out', 3, 'shift_line1')

        # control variables
        self.interrupt_work = False
        self.update_interval = 100
        self.scheme_max_width = 800
        self.scheme_max_height = 800

        # widgets
        self.scheme_frame = tk.Frame(self._master, width=self.scheme_max_width,
                                     height=self.scheme_max_height, borderwidth=4,
                                     relief='sunken')
        self.tool_frame = tk.Frame(self._master, width=self.scheme_max_width)

        self.scheme_img_label = tk.Label(self.scheme_frame)
        self.help_btn = tk.Button(self.tool_frame, text='Help',
                                  command=self.open_help)
        self.status_lbl = tk.Label(self.tool_frame, text='Idle..')
        self.status_lbl.grid(column=1, row=1)
        self.user_command = tk.StringVar()
        self.command_entry = tk.Entry(self.tool_frame,
                                      textvariable=self.user_command)

        # layout
        self.scheme_frame.grid(column=0, row=0)
        self.scheme_frame.grid_propagate(flag=False)

        self.tool_frame.grid(column=0, row=1)
        self.tool_frame.columnconfigure(0, weight=1)
        self.tool_frame.columnconfigure(1, weight=1)
        self.tool_frame.columnconfigure(2, weight=1)

        # for correct work of self.scheme_frame.winfo_height()
        self.scheme_frame.update()

        self.scheme_img_label.place(x=self.scheme_frame.winfo_width() / 2,
                                    y=self.scheme_frame.winfo_height() / 2,
                                    anchor='center')
        self.help_btn.grid(column=1, row=0)
        self.command_entry.grid(column=0, row=2, columnspan=3)

        # bindings
        self._master.bind('<KeyPress-s>', lambda e: self.start_scheme())
        self._master.bind('<KeyPress-t>', lambda e: self.stop_scheme())
        self._master.bind('<KeyPress-r>', lambda e: self.redraw_scheme())
        self._master.bind('<KeyPress-h>', lambda e: self.open_help())

        # last tunings

    @staticmethod
    def open_help():
        showinfo('Help', ('In main window press:\n'
                          '- "s" to start scheme\n'
                          '- "t" to stop scheme\n'
                          '- "r" to once redraw scheme\n'
                          '- "h" to open help'))

    def start_scheme(self):
        """Start infinite scheme update"""
        self.status_lbl.configure(text='Working')
        self.interrupt_work = False
        self._master.after(self.update_interval, self.update_scheme)

    def stop_scheme(self):
        """Stop infinite scheme update"""
        self.status_lbl.configure(text='Idle..')
        self.interrupt_work = True

    def update_scheme(self):
        """Update scheme every specified update interval"""
        if self.interrupt_work:
            return
        self.redraw_scheme(iterate_circuit=True)
        self._master.after(self.update_interval, self.update_scheme)

    def redraw_scheme(self, iterate_circuit: bool = False):
        """Redraw scheme once

        Arguments
        ----------
            iterate_circuit: specifies if to calculate values
            for output on image and iterate circuit
        """
        scheme_image = Visualizer.get_tkinter_image(self.scheme,
                                                    self.scheme_max_width,
                                                    self.scheme_max_height,
                                                    iterate_circuit)

        self.scheme_img_label.configure(image=scheme_image)
        self.scheme_img_label.image = scheme_image


if __name__ == "__main__":
    root = tk.Tk()
    SchemeGUI(root)
    root.mainloop()
