import tkinter
import tkinter as tk
from tkinter.messagebox import showinfo
from src.visualize import Visualizer
from src.scheme import Scheme
from src.input_module import InputParser


class SchemeGUI:
    """Encapsulate tkinter widgets and events functions"""

    # TODO: 1. create log readonly entry +
    #  2. make entry wider +
    #  3. add updating clock
    #  4. write file to test GUI

    def __init__(self, master: tkinter.Tk):
        self._master = master

        # configure main window
        self._master.title('L4Logic')
        self._master.resizable(width=False, height=False)

        # objects
        self.scheme = Scheme()
        self._visualizer = Visualizer(self.scheme)
        self._user_input_parser = InputParser(self.scheme)

        # control variables
        self._scheme_run = False
        self.interrupt_work = False
        self.update_interval = 100

        # size variables
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
        self.user_entry_var = tk.StringVar()
        self.user_entry = tk.Entry(self.tool_frame,
                                   textvariable=self.user_entry_var,
                                   width=50)
        self.load_commands_btn = tk.Button(self.tool_frame, text='Load',
                                           command=self.load_from_file)

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

        self.user_entry.grid(column=0, row=0, columnspan=2)
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
        if not self._scheme_run:
            self.status_lbl.configure(text='Working')
            self._scheme_run = True
            self.interrupt_work = False
            self._master.after(self.update_interval, self.update_scheme)
        else:
            self.write_to_log(f"-------------------------\n"
                              f"Stop scheme firstly\n")

    def stop_scheme(self):
        """Stop infinite scheme update"""
        if self._scheme_run:
            self.status_lbl.configure(text='Idle..')
            self._scheme_run = False
            self.interrupt_work = True
        else:
            self.write_to_log(f"-------------------------\n"
                              f"Start scheme firstly\n")

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
        scheme_image = self._visualizer.get_tkinter_image(iterate_circuit)

        self.scheme_img_label.configure(image=scheme_image)
        self.scheme_img_label.image = scheme_image

    def execute_scheme_command(self, command: str = None):
        if not command:
            command = self.user_entry_var.get()
        # self._user_input_parser.parse_raw_input(command)
        try:
            self._user_input_parser.parse_raw_input(command)
        except Exception as ex:
            self.write_to_log(f"Command: {command}\n"
                              f"Status: Error\n"
                              f"Error message: {ex}\n")
        else:
            self.write_to_log(f"Command: {command}\n"
                              f"Status: Completed\n")
            self.redraw_scheme()
        finally:
            self.write_to_log(f"-------------------------\n")

    def execute_many_commands(self, commands: list):
        cmd = commands[0]
        self.execute_scheme_command(cmd)

        if len(commands) > 1:
            self._master.after(10, lambda: self.execute_many_commands(commands[1:]))
        else:
            self.write_to_log(f"-------------------------\n"
                              f"Scheme added\n")

    def write_to_log(self, info: str):
        self.commands_log_entry.configure(state='normal')
        self.commands_log_entry.insert('1.0', info)
        self.commands_log_entry.configure(state='disabled')

    def load_from_file(self):
        path = self.user_entry_var.get()
        self.write_to_log(f"Command: read commands from {path}\n")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as ex:
            self.write_to_log(f"Status: Error\n"
                              f"Error message: {ex}\n")
            return
        else:
            self.write_to_log(f"Status: Completed\n")
        finally:
            self.write_to_log(f"-------------------------\n")

        commands = [line.strip() for line in lines]

        self.execute_many_commands(commands)

    def close_app(self):
        showinfo(':)', 'Thanks for using L4Logic today')
        self._master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    SchemeGUI(root)
    root.mainloop()
