import tkinter
import tkinter as tk
from tkinter import scrolledtext
from tkinter.messagebox import showinfo
from visualize import Visualizer
from scheme import Scheme
from input_module import raw_input


class SchemeGUI:
    """Encapsulate tkinter widgets and events functions"""

    # TODO: 1. create log readonly entry
    #  2. make entry wider +
    #  3. add updating clock

    def __init__(self, master: tkinter.Tk):
        self._master = master

        # configure main window
        self._master.title('L4Logic')
        self._master.resizable(width=False, height=False)

        # objects
        self.scheme = Scheme()

        # test scheme
        # self.scheme.add_element('constant', 0, (1, 1),
        #                         constant_value=1)
        # self.scheme.add_element('constant', 1, (1, 2),
        #                         constant_value=1)
        # self.scheme.add_element('constant', 2, (1, 3),
        #                         constant_value=1)
        # self.scheme.add_element('shifter', 3, (3, 1), num_bits=4)
        #
        # self.scheme.add_connection(0, 'out', 3, 'in2')
        # self.scheme.add_connection(1, 'out', 3, 'in3')
        # self.scheme.add_connection(2, 'out', 3, 'shift_line1')

        # control variables
        self.interrupt_work = False
        self.update_interval = 100
        self.scheme_max_width = 800
        self.scheme_max_height = 800

        # widgets
        self.scheme_frame = tk.Frame(self._master, width=self.scheme_max_width,
                                     height=self.scheme_max_height, borderwidth=4,
                                     relief='sunken')
        self.tool_frame = tk.Frame(self._master, width=self.scheme_max_width,
                                   borderwidth=4,
                                   relief='sunken')

        self.scheme_img_label = tk.Label(self.scheme_frame)
        self.status_lbl = tk.Label(self.scheme_frame, text='Idle..')

        self.help_btn = tk.Button(self.tool_frame, text='Help',
                                  command=self.open_help)
        self.user_command = tk.StringVar()
        self.command_entry = tk.Entry(self.tool_frame,
                                      textvariable=self.user_command,
                                      width=50)
        self.load_commands_btn = tk.Button(self.tool_frame, text='Load',
                                           command=self.load_file)

        self.commands_log_entry = tk.Text(self.tool_frame, height=20, width=50,
                                          state='disabled')
        self.cmd_entry_scroll = tk.Scrollbar(self.tool_frame)
        self.commands_log_entry.configure(yscrollcommand=self.cmd_entry_scroll.set)
        self.cmd_entry_scroll.config(command=self.commands_log_entry.yview)

        # layout
        self.scheme_frame.grid(column=0, row=0)
        self.scheme_frame.grid_propagate(flag=False)
        self.tool_frame.columnconfigure(0, weight=1)
        self.tool_frame.rowconfigure(0, weight=1)

        # for correct work of self.scheme_frame.winfo_height()
        self.scheme_frame.update()

        self.status_lbl.place(x=self.scheme_frame.winfo_width() / 2,
                              y=self.scheme_frame.winfo_height() - 20,
                              anchor='center')
        self.scheme_img_label.place(x=self.scheme_frame.winfo_width() / 2,
                                    y=self.scheme_frame.winfo_height() / 2,
                                    anchor='center')

        self.tool_frame.grid(column=1, row=0, sticky=tk.N)
        self.tool_frame.columnconfigure(0, weight=1)
        self.tool_frame.columnconfigure(1, weight=1)

        self.command_entry.grid(column=0, row=0, columnspan=2)
        self.load_commands_btn.grid(column=2, row=0)
        self.commands_log_entry.grid(column=0, row=2, columnspan=3, sticky=tk.EW)
        self.cmd_entry_scroll.grid(column=2, row=2, sticky='nse')
        self.help_btn.grid(column=2, row=3)

        # bindings
        self._master.bind('<Control-KeyPress-s>', lambda e: self.start_scheme())
        self._master.bind('<Control-KeyPress-t>', lambda e: self.stop_scheme())
        self._master.bind('<Control-KeyPress-r>', lambda e: self.redraw_scheme())
        self._master.bind('<Control-KeyPress-h>', lambda e: self.open_help())
        self._master.bind('<Return>', lambda e: self.execute_scheme_command())
        self._master.bind('<Control-KeyPress-e>', lambda e: self.close_app())

        # last tunings

    @staticmethod
    def open_help():
        showinfo('Help', ('In main window press:\n'
                          '- "Enter" to execute command\n'
                          '- "Ctr + s" to start scheme\n'
                          '- "Ctr + t" to stop scheme\n'
                          '- "Ctr + r" to once redraw scheme\n'
                          '- "Ctr + h" to open help\n'
                          '- "Ctrl + e" to exit'))

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

    def execute_scheme_command(self):
        command = self.user_command.get()
        try:
            raw_input(self.scheme, command)
        except Exception as ex:
            self.write_to_log(f"Command: {command}\n"
                              f"Status: Error\n"
                              f"Error message: {ex}\n"
                              f"-------------------------\n")
        else:
            self.write_to_log(f"Command: {command}\n"
                              f"Status: Completed\n"
                              f"-------------------------\n")
            self.redraw_scheme()

    def write_to_log(self, info: str):
        self.commands_log_entry.configure(state='normal')
        self.commands_log_entry.insert('1.0', info)
        self.commands_log_entry.configure(state='disabled')

    def load_file(self):
        self.write_to_log('abc\nabc\n')

    def close_app(self):
        showinfo(':)', 'Thanks for using L4Logic today')
        self._master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    SchemeGUI(root)
    root.mainloop()
