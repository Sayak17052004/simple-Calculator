from tkinter import *
import PIL 
from datetime import datetime

class Calculator:
    def __init__(self, root):
        self.root = root
        self.history = []
        self.setup_ui()
        
    def setup_ui(self):
        self.root.geometry("644x1000")  # Slightly taller for copyright
        self.root.minsize(600, 850)
        self.root.maxsize(700, 1000)
        self.root.title("Sayak's Calculator")
        
        # Screen
        self.scvalue = StringVar()
        self.scvalue.set("")
        self.screen = Entry(self.root, textvar=self.scvalue, font="lucida 40 bold", 
                          borderwidth=26, relief=RIDGE, bg="powder blue", fg="black")
        self.screen.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=12, pady=18, ipadx=10)
        self.screen.focus_set()
        self.screen.icursor(END)
        
        # Configure grid weights
        for i in range(6):  # 6 rows
            self.root.grid_rowconfigure(i+1, weight=1)
        for i in range(4):  # 4 columns
            self.root.grid_columnconfigure(i, weight=1)
        
        # Button configuration: (text, row, column, colspan, bg_color)
        button_config = [
            # Row 1: AC (2-col), (, )
            ("AC", 1, 0, 2, "#848484"), ("(", 1, 2, 1, "#848484"), (")", 1, 3, 1, "#848484"),
            # Row 2: 7, 8, 9, /
            ("7", 2, 0, 1, "black"), ("8", 2, 1, 1, "black"), 
            ("9", 2, 2, 1, "black"), ("/", 2, 3, 1, "#848484"),
            # Row 3: 4, 5, 6, *
            ("4", 3, 0, 1, "black"), ("5", 3, 1, 1, "black"), 
            ("6", 3, 2, 1, "black"), ("*", 3, 3, 1, "#848484"),
            # Row 4: 1, 2, 3, -
            ("1", 4, 0, 1, "black"), ("2", 4, 1, 1, "black"), 
            ("3", 4, 2, 1, "black"), ("-", 4, 3, 1, "#848484"),
            # Row 5: 0 (2-col), ., +
            ("0", 5, 0, 2, "black"), (".", 5, 2, 1, "black"), ("+", 5, 3, 1, "#848484"),
            # Row 6: X (2-col), = (2-col)
            ("X", 6, 0, 2, "#848484"), ("=", 6, 2, 2, "#848484")
        ]
        
        # Create buttons using grid
        for (text, row, col, colspan, bg_color) in button_config:
            btn = Button(self.root, text=text, font="lucida 20 bold",
                        bg=bg_color, fg="#FFFFFF", borderwidth=0,
                        command=lambda t=text: self.click_handler(t))
            btn.grid(row=row, column=col, columnspan=colspan, 
                    sticky="nsew", padx=5, pady=5, ipadx=10, ipady=20)
        
        # History section
        self.create_history_section()
        
        # Copyright section
        self.create_copyright_section()
    
    def create_history_section(self):
        # History frame
        history_frame = Frame(self.root)
        history_frame.grid(row=7, column=0, columnspan=4, sticky="nsew", pady=10)
        self.root.grid_rowconfigure(7, weight=1)
        
        Label(history_frame, text="History", font="lucida 30 bold", anchor="w").pack(
            side=LEFT, padx=100)
        
        # Clear button
        clear_btn = Button(history_frame, text="CLEAR", 
                          font="lucida 12 bold",
                          bg="lightgreen", fg="black",
                          command=self.clear_history)
        clear_btn.pack(side=RIGHT, anchor="e", 
                      padx=110, pady=10,
                      ipadx=40, ipady=6)
        
        # Scrollable history area
        history_container = Frame(self.root)
        history_container.grid(row=8, column=0, columnspan=4, sticky="nsew")
        self.root.grid_rowconfigure(8, weight=2)
        
        scrollbar = Scrollbar(history_container)
        scrollbar.pack(side=RIGHT, fill="y")
        
        self.history_canvas = Canvas(history_container, yscrollcommand=scrollbar.set,
                                    bg=self.root.cget('bg'), highlightthickness=0)
        self.history_canvas.pack(side=LEFT, fill="both", expand=True)
        
        scrollbar.config(command=self.history_canvas.yview)
        
        self.history_inner_frame = Frame(self.history_canvas)
        self.history_canvas.create_window((0, 0), window=self.history_inner_frame, anchor="nw")
        
        self.history_inner_frame.bind("<Configure>", 
            lambda e: self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all")))
        
        self.history_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def create_copyright_section(self):
        """Adds a professional copyright footer"""
        copyright_frame = Frame(self.root, bg="#f0f0f0")
        copyright_frame.grid(row=9, column=0, columnspan=4, sticky="nsew", pady=(10, 0))
        
        # Copyright text
        copyright_text = f"© 2023 Sayak's Calculator Project | Version 1.0 | {datetime.now().year}"
        Label(copyright_frame, text=copyright_text, 
             font=("Arial", 9), bg="#f0f0f0", fg="#555555").pack(pady=5)
        
        # Disclaimer
        Label(copyright_frame, 
             text="This software is provided 'as-is' without any warranties",
             font=("Arial", 8), bg="#f0f0f0", fg="#777777").pack()

    def _on_mousewheel(self, event):
        self.history_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def click_handler(self, text):
        self.screen.focus_set()
        
        try:
            if text == "=":
                if self.scvalue.get().isdigit():
                    value = int(self.screen.get())
                else:
                    expression = self.screen.get()
                    value = eval(expression)
                
                self.scvalue.set(value)
                self.history.append(f"{expression} = {value}")
                self.update_history()
                
            elif text == "AC":
                self.scvalue.set("")
            elif text == "X":
                current = self.scvalue.get()
                self.scvalue.set(current[:-1])
            else:
                current = self.scvalue.get()
                cursor_pos = self.screen.index(INSERT)
                self.scvalue.set(current[:cursor_pos] + text + current[cursor_pos:])
                self.screen.icursor(cursor_pos + 1)
                
            self.screen.update()
            
        except (ValueError, NameError, TypeError, SyntaxError):
            self.scvalue.set("Invalid Input")
        except ZeroDivisionError:
            self.scvalue.set("Can't divide by zero")

    def update_history(self):
        for widget in self.history_inner_frame.winfo_children():
            widget.destroy()
        
        for item in reversed(self.history):
            Label(self.history_inner_frame, text=item, font="ArialNarrow 13",
                 anchor="w", justify=LEFT).pack(fill="x", padx=5, pady=2)
        
        self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))
        self.history_canvas.yview_moveto(0)

    def clear_history(self):
        self.history = []
        self.update_history()

if __name__ == "__main__":
    root = Tk()
    # Enhanced icon loading with multiple fallbacks
    icon_loaded = False
    
    # Try Windows .ico first
    try:
        root.iconbitmap('assets/calculator.ico')
        icon_loaded = True
    except Exception as e:
        print(f"ICO load error: {e}")
    
    # Try PNG with Pillow fallback
    if not icon_loaded:
        try:
                     
            img = Image.open('assets/calculator.png')
            photo = ImageTk.PhotoImage(img)
            root.tk.call('wm', 'iconphoto', root._w, photo)
            icon_loaded = True
        except Exception as e:
            print(f"PNG load error: {e}")
    
    # Final fallback to built-in calculator icon (Windows only)
    if not icon_loaded and root._windowingsystem == 'win32':
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('myappid')
            root.iconbitmap(default='@calculator')  # Windows built-in
        except:
            pass
    calculator = Calculator(root)
    root.mainloop()