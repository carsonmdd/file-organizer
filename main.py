import tkinter as tk

'''
UI Features:
- Define year1
- Choose input directory
- Choose output directory
'''

class OrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('File Organizer')

        self.create_year_entry()
        self.create_input_entry()
        self.create_output_entry()
        self.create_organize_section()

    def run(self):
        self.mainloop()

    def create_year_entry(self):
        self.year_frame = tk.Frame(self)
        self.year_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.year_label = tk.Label(self.year_frame, text='Year 1', font=('Colibri', 14))
        self.year_label.grid(row=0, column=0, sticky='w')
        self.year_entry = tk.Entry(self.year_frame)
        self.year_entry.grid(row=1, column=0, sticky='w')
        self.year_error = tk.Label(self.year_frame, text='Invalid year format. Please use YYYY-YYYY', font=('Colibri', 10), fg='red')
        self.year_error.grid(row=2, column=0, sticky='w')

    def create_input_entry(self):
        self.input_frame = tk.Frame(self)
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.input_label = tk.Label(self.input_frame, text='Input Folder', font=('Colibri', 14))
        self.input_label.grid(row=0, column=0, sticky='w')
        self.input_path_label = tk.Label(self.input_frame, width=20, font=('Colibri', 14), borderwidth=2, relief='sunken')
        self.input_path_label.grid(row=1, column=0, sticky='w')
        self.input_button = tk.Button(self.input_frame, text='Select folder').grid(row=1, column=1, sticky='w')
        self.input_error = tk.Label(self.input_frame, text='Please select a folder', font=('Colibri', 10), fg='red')
        self.input_error.grid(row=2, column=0, sticky='w')
    
    def create_output_entry(self):
        self.output_frame = tk.Frame(self)
        self.output_frame.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.output_label = tk.Label(self.output_frame, text='Output Folder', font=('Colibri', 14))
        self.output_path_label = tk.Label(self.output_frame, width=20, font=('Colibri', 14), borderwidth=2, relief='sunken')
        self.output_path_label.grid(row=1, column=0, sticky='w')
        self.output_label.grid(row=0, column=0, sticky='w')
        self.output_button = tk.Button(self.output_frame, text='Select folder').grid(row=1, column=1, sticky='w')
        self.output_error = tk.Label(self.output_frame, text='Please select a folder', font=('Colibri', 10), fg='red')
        self.output_error.grid(row=2, column=0, sticky='w')

    def create_organize_section(self):
        self.organize_frame = tk.Frame(self)
        self.organize_frame.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.organize_button = tk.Button(self.organize_frame, text='Organize')
        self.organize_button.grid(row=0, column=0, sticky='w')
        self.organize_success = tk.Label(self.organize_frame, text='Successfully organized!', font=('Colibri', 10), fg='green')
        self.organize_success.grid(row=0, column=1, sticky='w')

if __name__ == '__main__':
    OA = OrganizerApp()
    OA.run()