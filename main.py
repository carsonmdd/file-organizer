import tkinter as tk
from tkinter import filedialog
from custom_widgets import CustomEntry

class OrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('File Organizer')

        self.year_placeholder = 'e.g. 2022-2023'
        self.year1 = ''
        self.input_dir = ''
        self.output_dir = ''

        self.create_year_field()
        self.create_input_field()
        self.create_output_field()
        self.create_organize_section()

    def run(self):
        self.mainloop()

    def create_year_field(self):
        self.year_frame = tk.Frame(self)
        self.year_frame.grid(row=0, column=0, padx=20, pady=(20, 5), sticky='w')
        self.year_label = tk.Label(self.year_frame, text='Year 1', font=('Colibri', 12))
        self.year_label.grid(row=0, column=0, sticky='w')
        self.year_entry = CustomEntry(self.year_frame, self.year_placeholder)
        self.year_entry.grid(row=1, column=0, ipady=5, sticky='w')
        self.year_error = tk.Label(self.year_frame, font=('Colibri', 9), fg='red')
        self.year_error.grid(row=2, column=0, sticky='w')

    def create_input_field(self):
        self.input_frame = tk.Frame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=(0, 5), sticky='w')
        self.input_label = tk.Label(self.input_frame, text='Input Folder', font=('Colibri', 12))
        self.input_label.grid(row=0, column=0, sticky='w')
        self.input_path_entry = CustomEntry(self.input_frame, width=40, font=('Colibri', 9), state='readonly')
        self.input_path_entry.grid(row=1, column=0, padx=(0, 10), ipady=5, sticky='w')
        self.input_button = tk.Button(self.input_frame, text='Select folder', command=self.get_input_dir)
        self.input_button.grid(row=1, column=1, sticky='w')
        self.input_error = tk.Label(self.input_frame, font=('Colibri', 9), fg='red')
        self.input_error.grid(row=2, column=0, sticky='w')
    
    def create_output_field(self):
        self.output_frame = tk.Frame(self)
        self.output_frame.grid(row=2, column=0, padx=20, pady=(0, 50), sticky='w')
        self.output_label = tk.Label(self.output_frame, text='Output Folder', font=('Colibri', 12))
        self.output_path_entry = CustomEntry(self.output_frame, width=40, font=('Colibri', 9), state='readonly')
        self.output_path_entry.grid(row=1, column=0, padx=(0, 10), ipady=5, sticky='w')
        self.output_label.grid(row=0, column=0, sticky='w')
        self.output_button = tk.Button(self.output_frame, text='Select folder', command=self.get_output_dir)
        self.output_button.grid(row=1, column=1, sticky='w')
        self.output_error = tk.Label(self.output_frame, font=('Colibri', 9), fg='red')
        self.output_error.grid(row=2, column=0, sticky='w')

    def create_organize_section(self):
        self.organize_frame = tk.Frame(self)
        self.organize_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky='w')
        self.organize_button = tk.Button(self.organize_frame, text='Organize', command=self.organize)
        self.organize_button.grid(row=0, column=0, padx=(0, 10), sticky='w')
        self.organize_success = tk.Label(self.organize_frame, font=('Colibri', 9), fg='green')
        self.organize_success.grid(row=0, column=1, sticky='w')

    def get_input_dir(self):
        self.input_dir = filedialog.askdirectory(title='Select input folder')
        self.update_entry(self.input_path_entry, self.input_dir)

    def get_output_dir(self):
        self.output_dir = filedialog.askdirectory(title='Select output folder')
        self.update_entry(self.output_path_entry, self.output_dir)

    def update_entry(self, entry, text):
        entry.config(state='normal')
        entry.delete(0, tk.END)
        entry.insert(0, text)
        entry.config(state='readonly')

    def organize(self):
        year_entry_text = self.year_entry.get()
        self.year1 = year_entry_text if year_entry_text != self.year_placeholder else ''
        if not self.year_valid(self.year1):
            self.year_error.config(text='Invalid year format. Please use YYYY-YYYY')
        else:
            self.year_error.config(text='')
        if not self.input_dir:
            self.input_error.config(text='Please select a folder')
        else:
            self.input_error.config(text='')
        if not self.output_dir:
            self.output_error.config(text='Please select a folder')
        else:
            self.output_error.config(text='')
        
        if not (self.year1 and self.input_dir and self.output_dir):
            print('INVALID ENTRIES')
            self.organize_success.config(text='')
            return
        
        print('ORGANIZING')
        self.organize_success.config(text='Organized successfully!')

    def year_valid(self, year) -> bool:
        if not year:
            return False
        if len(year) != 9:
            return False
        if year[4] != '-':
            return False

        y1 = year[:4]
        y2 = year[5:]
        if not y1.isdigit() or not y2.isdigit():
            return False
        if not (int(y2) - int(y1) == 1):
            return False

        return True
        
if __name__ == '__main__':
    OA = OrganizerApp()
    OA.run()