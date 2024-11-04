import tkinter as tk
from tkinter import filedialog, messagebox
import os, sys
import json
from datetime import datetime
from custom_widgets import CustomEntry

class OrganizerApp(tk.Tk):
    def __init__(self):
        self.settings = self.load_settings()
        print(self.settings.get('file_structure'))
        super().__init__()
        self.title('File Organizer')

        self.input_dir = ''
        self.output_dir = ''
        self.font = 'Arial Rounded MT Bold'

        self.create_input_field()
        self.create_output_field()
        self.create_organize_section()

    def run(self):
        self.mainloop()

    def load_settings(self):
        '''Reads in settings from a file'''
        data = {}
        filepath = self.external_path('settings.json')
        try:
            with open(filepath) as file:
                data = json.load(file)
        except Exception as e:
            messagebox.showerror('Error', f'Error opening settings file: {e}')
            sys.exit()

        if not data.get('file_structure'):
            messagebox.showerror('Error', 'No file_structure found in settings')
            sys.exit()
        elif not data.get('file_structure').get('2D'):
            messagebox.showerror('Error', 'No 2D found in settings')
            sys.exit()
        elif not data.get('file_structure').get('3D'):
            messagebox.showerror('Error', 'No 3D found in settings')
            sys.exit()
        else:
            return data
        
    def external_path(self, relative_path):
        '''Gets path for resource in same directory as app file on macOS'''
        # If running as exe,
        if getattr(sys, 'frozen', False):
            exe_path = os.path.abspath(sys.executable)
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(exe_path))))
        # else running as script
        else:
            base_path = os.path.abspath('.')

        return os.path.join(base_path, relative_path)

    def create_input_field(self):
        self.input_frame = tk.Frame(self)
        self.input_frame.grid(row=0, column=0, padx=20, pady=(10, 5), sticky='w')
        self.input_label = tk.Label(self.input_frame, text='Input Folder', font=(self.font, 12))
        self.input_label.grid(row=0, column=0, sticky='w')
        self.input_path_entry = CustomEntry(self.input_frame, width=40, font=(self.font, 9), state='readonly')
        self.input_path_entry.grid(row=1, column=0, padx=(0, 10), ipady=5, sticky='w')
        self.input_button = tk.Button(self.input_frame, text='Select folder', command=self.get_input_dir)
        self.input_button.grid(row=1, column=1, sticky='w')
        self.input_error = tk.Label(self.input_frame, font=(self.font, 9), fg='red')
        self.input_error.grid(row=2, column=0, sticky='w')
    
    def create_output_field(self):
        self.output_frame = tk.Frame(self)
        self.output_frame.grid(row=1, column=0, padx=20, pady=(0, 50), sticky='w')
        self.output_label = tk.Label(self.output_frame, text='Output Folder', font=(self.font, 12))
        self.output_path_entry = CustomEntry(self.output_frame, width=40, font=(self.font, 9), state='readonly')
        self.output_path_entry.grid(row=1, column=0, padx=(0, 10), ipady=5, sticky='w')
        self.output_label.grid(row=0, column=0, sticky='w')
        self.output_button = tk.Button(self.output_frame, text='Select folder', command=self.get_output_dir)
        self.output_button.grid(row=1, column=1, sticky='w')
        self.output_error = tk.Label(self.output_frame, font=(self.font, 9), fg='red')
        self.output_error.grid(row=2, column=0, sticky='w')

    def create_organize_section(self):
        self.organize_frame = tk.Frame(self)
        self.organize_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky='w')
        self.organize_button = tk.Button(self.organize_frame, text='Organize', command=self.organize)
        self.organize_button.grid(row=0, column=0, padx=(0, 10), sticky='w')
        self.organize_success = tk.Label(self.organize_frame, font=(self.font, 9), fg='green')
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
        if not self.input_dir:
            self.input_error.config(text='Please select a folder')
        else:
            self.input_error.config(text='')
        if not self.output_dir:
            self.output_error.config(text='Please select a folder')
        else:
            self.output_error.config(text='')
        
        if not (self.input_dir and self.output_dir):
            print('INVALID ENTRIES')
            self.organize_success.config(text='')
            return
        
        print('ORGANIZING')
        self.make_dirs()
        self.move_files()
        self.organize_success.config(text='Organized successfully!')
    
    def make_dirs(self):
        '''
        - Create year folders
        - Create semester and other folders
        - Create name folders

        aug 26 - dec 16; jan 27 - may 16
        Aug 1 - Dec 31; Jan 1 - July 31
        Aug-Dec; Jan-July
        '''
        min_year, max_year = self.get_years()
    
    def get_years(self):
        for filename in os.listdir(self.input_dir):
            print(filename)

        return None, None

    def move_files(self):
        return
        
if __name__ == '__main__':
    OA = OrganizerApp()
    OA.run()