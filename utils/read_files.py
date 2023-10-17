# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import *

class fileList:
    def __init__(self) -> None:
        self.root_dir = ''
        self.file_ls = []
        self.root = None

    def getFileList(self):
        directory_name = tk.filedialog.askdirectory() # Open directory and get its name
        if directory_name == '':
            return
        
        dir_path = directory_name
        self.root_dir = dir_path
        dir_ls = os.listdir(dir_path)
        file_ls = [] # All file name list here
        for item in dir_ls:
            if not os.path.isdir(item):
                file_ls.append(item)
        self.file_ls = file_ls

def filter_extension(extension, file_ls):
    filtered = []
    for file_name in file_ls:
        sufix = os.path.splitext(file_name)[1][1:]
        if sufix == extension:
            filtered.append(file_name)

    return filtered

class process:
    def __init__(self, blur, hiled) -> None:
        self.blur = blur
        self.hiled = hiled
        self.output_dir = hiled.root_dir

    def run(self):
        self.blur.file_ls = filter_extension('py', self.blur.file_ls)
        self.hiled.file_ls = filter_extension('py', self.hiled.file_ls)
        blur_file_num = len(self.blur.file_ls)
        hiled_file_num = len(self.hiled.file_ls)
        if blur_file_num > 0 and hiled_file_num > 0:
            self.searchExcuteCommand()
        print('Run')

    def searchExcuteCommand(self):
        hiled_dir = self.hiled.root_dir
        split_element = 'blur'
        for hiled_name in self.hiled.file_ls:
            hiled_prefix = hiled_name.split(split_element, maxsplit=1)[0]
            for blur_name in self.blur.file_ls:
                if blur_name.rfind(hiled_prefix) != -1:
                    # Find the corresponding blur name
                    print(hiled_prefix)
                    if self.root is not None:
                        l1 = tk.Label(self.root, text=hiled_prefix , fg="black", bg="white").pack()
                    #command = 
                    #os.system(command)

    def attach_window(self, root_window):
        self.root = root_window



def main():
    root = Tk()
    blur_file_ls = fileList()
    hiled_file_ls = fileList()
    blur_btn = ttk.Button(root, text="blur", style="C.TButton", command=blur_file_ls.getFileList).pack()
    hiled_btn = ttk.Button(root, text="HILed", style="C.TButton", command=hiled_file_ls.getFileList).pack()
    process_instance = process(blur_file_ls, hiled_file_ls)
    run = ttk.Button(root, text="RUN", style="C.TButton", command=process_instance.run).pack()
    process_instance.attach_window(root)
    root.mainloop()
    print('Main passed!')
if __name__ == '__main__':
    main()

