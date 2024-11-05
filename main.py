import tkinter as tk
from tkinter import filedialog, messagebox
import os, sys
import json
from datetime import datetime
import shutil
from custom_widgets import CustomEntry
from path_utils import *

class OrganizerApp(tk.Tk):
    def __init__(self):
        self.settings = self.load_settings()
        self.ranges = self.create_ranges()
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
        filepath = external_path('settings.json')
        try:
            with open(filepath) as file:
                data = json.load(file)
        except Exception as e:
            self.display_error(f'Error opening settings file: {e}')

        self.check_years(data)
        self.check_file_structure(data)

        return data
        
    def create_ranges(self):
        # ranges = {
        #     (12387, 182380): {
        #         'year': 'year1',
        #         'sem': 'sem1'
        #     }
        # }
        ranges = {}
        for year, sems in self.settings.get('years').items():
            sem1_rng = self.gen_range(year, 'sem1', sems.get('sem1'))
            ranges[sem1_rng[0]] = sem1_rng[1]
            sem2_rng = self.gen_range(year, 'sem2', sems.get('sem2'))
            ranges[sem2_rng[0]] = sem2_rng[1]

        return ranges

    def gen_range(self, year: str, sem_name, sem: str) -> tuple[tuple[int], dict[str, str]]:
        sem_dates = sem.split('-')
        sem_start = self.get_timestamp(sem_dates[0], True)
        sem_end = self.get_timestamp(sem_dates[1], False)

        return (sem_start, sem_end), {'year': year, 'sem': sem_name}

    def get_timestamp(self, date, range_start):
        try:
            if range_start:
                datetime_obj = datetime.strptime(date, '%m/%d/%Y')
            else:
                datetime_obj = datetime.strptime(date, '%m/%d/%Y').replace(hour=23, minute=59, second=59)
            return datetime_obj.timestamp()
        except Exception as e:
            self.display_error(f'Invalid date with error: {e}')

    def check_years(self, data):
        if not data.get('years'):
            self.display_error('No years found in settings')
        for year in data.get('years').keys():
            if not data.get('years').get(year).get('sem1'):
                self.display_error(f'No {year}/sem1 found in settings')
            if not data.get('years').get(year).get('sem2'):
                self.display_error(f'No {year}/sem2 found in settings')
    
    def check_file_structure(self, data):
        if not data.get('file_structure'):
            self.display_error('No file_structure found in settings')
        elif not data.get('file_structure').get('2D'):
            self.display_error('No 2D found in settings')
        elif not data.get('file_structure').get('3D'):
            self.display_error('No 3D found in settings')

    def display_error(self, msg):
        messagebox.showerror('Error', msg)
        sys.exit()

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
            self.organize_success.config(text='')
            return
        
        self.move_files()
        self.organize_success.config(text='Organized successfully!')
    
    def move_files(self):
        '''
        - Create year folders
        - Create semester folders
        - Create 2D/3D folders
        - Create name folders

        For each file's creation date,
            If date is within a range,
                Put file in range dir
        '''
        for filename in os.listdir(self.input_dir):
            file_path = os.path.join(self.input_dir, filename)
            if not os.path.isfile(file_path):
                continue

            ctime = os.path.getctime(file_path)
            for range, info in self.ranges.items():
                start, end = range
                if ctime >= start and ctime <= end:
                    ext = os.path.splitext(filename)[1][1:]
                    dest = self.get_file_dest(info, ext)
                    if not dest:
                        continue
                    self.safe_move_file(file_path, dest)
                    break

    def safe_move_file(self, src, dest):
        try:
            os.makedirs(dest, exist_ok=True)

            filename =  os.path.basename(src)
            final_file_path = os.path.join(dest, filename)
            if os.path.isfile(final_file_path):
                final_file_path = new_path(final_file_path)

            shutil.move(src, final_file_path)
        except Exception as e:
            self.display_error(f'Error occured while moving file: {e}')
    
    def get_file_dest(self, info, ext):
        year = info.get('year')
        sem = info.get('sem')
        type, name = '', ''
        for n, exts in self.settings.get('file_structure').get('2D').items():
            if ext in exts:
                type = '2D'
                name = n
                break
        for n, exts in self.settings.get('file_structure').get('3D').items():
            if ext in exts:
                type = '3D'
                name = n
                break

        if not type or not name:
            return None
        
        path = os.path.join(self.output_dir, year, sem, type, name)
        return os.path.normpath(path)
        
if __name__ == '__main__':
    OA = OrganizerApp()
    OA.run()