"""Desktop-only PNG pass generator. No PowerPoint, WPS, COM, or web server."""
from pathlib import Path
import queue
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from batch import generate_batch
from configuration import read_configuration
from renderer import PassRenderer

ROOT = Path(__file__).resolve().parent


class Application:
    def __init__(self, window, config, renderer):
        self.window, self.config, self.renderer = window, config, renderer
        self.events = queue.Queue()
        self.serials = config['initial_serials'].copy()
        self.busy = False
        window.title('Campus Pass Image Generator')
        window.geometry('690x465')
        window.resizable(False, False)
        style = ttk.Style(window)
        style.configure('.', font=('Segoe UI', 11))
        frame = ttk.Frame(window, padding=24)
        frame.pack(fill='both', expand=True)
        frame.columnconfigure(1, weight=1)
        self.color = tk.StringVar(value='green')
        self.serial = tk.StringVar(value=str(self.serials['green']).zfill(8))
        self.quantity = tk.StringVar(value='1')
        self.next_text = tk.StringVar()
        self.status = tk.StringVar(value='Ready. Generation uses calibrated images only.')
        self.resolution = tk.StringVar()
        ttk.Label(frame, text='Color').grid(row=0, column=0, sticky='w', pady=8)
        self.color_box = ttk.Combobox(frame, textvariable=self.color, values=['red', 'green', 'blue'], state='readonly')
        self.color_box.grid(row=0, column=1, sticky='ew', padx=(18, 0))
        self.color_box.bind('<<ComboboxSelected>>', self.change_color)
        ttk.Label(frame, text='Current serial').grid(row=1, column=0, sticky='w', pady=8)
        self.serial_entry = ttk.Entry(frame, textvariable=self.serial)
        self.serial_entry.grid(row=1, column=1, sticky='ew', padx=(18, 0))
        ttk.Label(frame, text='Quantity').grid(row=2, column=0, sticky='w', pady=8)
        self.count_entry = ttk.Spinbox(frame, textvariable=self.quantity, from_=1, to=999)
        self.count_entry.grid(row=2, column=1, sticky='ew', padx=(18, 0))
        ttk.Label(frame, textvariable=self.next_text).grid(row=3, column=0, columnspan=2, sticky='w', pady=(14, 4))
        ttk.Label(frame, textvariable=self.resolution).grid(row=4, column=0, columnspan=2, sticky='w')
        self.button = ttk.Button(frame, text='Generate PNG Images', command=self.start)
        self.button.grid(row=5, column=0, columnspan=2, sticky='ew', pady=(22, 12), ipady=8)
        self.bar = ttk.Progressbar(frame, mode='determinate')
        self.bar.grid(row=6, column=0, columnspan=2, sticky='ew')
        ttk.Label(frame, textvariable=self.status, wraplength=630).grid(row=7, column=0, columnspan=2, sticky='w', pady=(14, 0))
        self.serial.trace_add('write', self.update_preview)
        self.change_color()
        window.protocol('WM_DELETE_WINDOW', self.close)
        window.after(100, self.process_events)

    def update_preview(self, *_):
        try:
            value = int(self.serial.get())
            if value < 0 or value >= 9999999999:
                raise ValueError
            self.next_text.set(f'Next: JT-{value + 1:08d}    QR: 109-JT-{value + 1:08d}')
        except ValueError:
            self.next_text.set('Enter a valid current serial number.')

    def change_color(self, *_):
        color = self.color.get()
        self.serial.set(f'{self.serials[color]:08d}')
        width, height = self.renderer.manifest['colors'][color]['size']
        self.resolution.set(f'PNG output: {width} x {height} pixels. Fixed reference layout.')
        self.update_preview()

    def start(self):
        if self.busy:
            return
        try:
            value, count = self.serial.get(), self.quantity.get()
            if not value.isascii() or not value.isdigit() or not 1 <= len(value) <= 10:
                raise ValueError('The current serial must contain one to ten digits.')
            if not count.isascii() or not count.isdigit() or not 1 <= int(count) <= 999:
                raise ValueError('Quantity must be an integer from 1 to 999.')
            current, count, color = int(value), int(count), self.color.get()
            if current + count > 9999999999:
                raise ValueError('The final serial must not exceed 9999999999.')
        except ValueError as error:
            messagebox.showerror('Invalid Input', str(error), parent=self.window)
            return
        self.busy = True
        self.button.configure(state='disabled')
        self.color_box.configure(state='disabled')
        self.serial_entry.configure(state='disabled')
        self.count_entry.configure(state='disabled')
        self.bar.configure(maximum=count, value=0)
        self.status.set('Generating PNG images...')

        def worker():
            try:
                result = generate_batch(self.renderer, color, current, count, self.config['output_directory'],
                                        lambda done, total: self.events.put(('progress', done)))
                self.events.put(('complete', (color, current + count, result)))
            except Exception as error:
                self.events.put(('error', str(error)))
        threading.Thread(target=worker, daemon=True).start()

    def process_events(self):
        while not self.events.empty():
            kind, value = self.events.get_nowait()
            if kind == 'progress':
                self.bar.configure(value=value)
            else:
                self.busy = False
                self.button.configure(state='normal')
                self.color_box.configure(state='readonly')
                self.serial_entry.configure(state='normal')
                self.count_entry.configure(state='normal')
                if kind == 'complete':
                    color, last, result = value
                    self.serials[color] = last
                    self.serial.set(f'{last:08d}')
                    self.status.set(f'Created {len(result.files)} PNG images and a ZIP archive.\n{result.archive}')
                    messagebox.showinfo('Complete', f'Images: {result.directory}\n\nZIP: {result.archive}', parent=self.window)
                else:
                    self.status.set('Generation failed: ' + value)
                    messagebox.showerror('Generation Failed', value, parent=self.window)
        self.window.after(100, self.process_events)

    def close(self):
        if self.busy:
            messagebox.showinfo('Generation in Progress', 'Wait for the current batch to finish.', parent=self.window)
            return
        self.window.destroy()


def main():
    window = tk.Tk()
    window.withdraw()
    try:
        if len(sys.argv) != 1:
            raise ValueError('This release provides a desktop interface only. Use Launch.cmd without arguments.')
        config = read_configuration(ROOT)
        renderer = PassRenderer()
    except Exception as error:
        messagebox.showerror('Configuration Error', str(error), parent=window)
        window.destroy()
        return 1
    Application(window, config, renderer)
    window.deiconify()
    window.mainloop()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
