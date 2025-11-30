import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, simpledialog
from MG_utils import mg_distance_mg, mg_random_color_mg
from MG_shapes import MGShape
from PIL import Image, ImageGrab

class MGApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("app")
        self.root.geometry("1200x800")
        self.draw_color = "#000000"
        self.line_width = 3
        self.shapes = []
        self.current_shape = None
        self.last_x = 0
        self.last_y = 0
        self.mode_var = tk.StringVar(value="Rajzolás")
        self.text_to_place = None
        self.eraser_preview_id = None
        self.start_x = None
        self.start_y = None
        self._build_ui()

    def _build_ui(self):
        top1 = ttk.Frame(self.root)
        top1.pack(side="top", fill="x")

        ttk.Button(top1, text="Törlés", command=self.clear_canvas).pack(side="left", padx=4, pady=4)
        ttk.Button(top1, text="Vissza", command=self.undo).pack(side="left", padx=4, pady=4)
        ttk.Button(top1, text="Véletlen szín", command=self.random_color).pack(side="left", padx=4, pady=4)
        ttk.Button(top1, text="Színválasztó", command=self.choose_color).pack(side="left", padx=4, pady=4)

        self.color_preview = tk.Label(top1, width=2, background=self.draw_color)
        self.color_preview.pack(side="left", padx=6)

        ttk.Button(top1, text="Radír mód", command=self.use_eraser).pack(side="left", padx=4, pady=4)
        ttk.Button(top1, text="Szöveg bevitele", command=self.start_text_input).pack(side="left", padx=4, pady=4)
        ttk.Button(top1, text="Mentés (PS)", command=self.save_canvas).pack(side="left", padx=4)
        ttk.Button(top1, text="Mentés (PNG)", command=self.save_png).pack(side="left", padx=4)

        top2 = ttk.Frame(self.root)
        top2.pack(side="top", fill="x")

        ttk.Label(top2, text="Mód").pack(side="left", padx=4)
        mode_box = ttk.Combobox(
            top2, textvariable=self.mode_var,
            values=["Rajzolás", "Téglalap", "Négyzet", "Kör", "Vonal"],
            width=12, state="readonly"
        )
        mode_box.pack(side="left", padx=4)

        ttk.Label(top2, text="Vonalvastagság").pack(side="left", padx=4)
        self.width_var = tk.IntVar(value=self.line_width)
        ttk.Spinbox(top2, from_=1, to=50, textvariable=self.width_var, width=5, command=self.change_width).pack(side="left", padx=4)

        ttk.Label(top2, text="Stílus").pack(side="left", padx=4)
        self.line_style_var = tk.StringVar(value="Teli")
        ttk.Combobox(
            top2, textvariable=self.line_style_var,
            values=["Teli", "Szaggatott", "Pontozott"],
            width=12, state="readonly"
        ).pack(side="left", padx=4)

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self.on_button_down)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_up)
        self.canvas.bind("<Motion>", self.on_mouse_move_for_eraser)

        bottom = ttk.Frame(self.root)
        bottom.pack(side="bottom", fill="x")
        self.coord_label = ttk.Label(bottom, text="x: 0  y: 0  hossz: 0")
        self.coord_label.pack(side="left", padx=4, pady=4)

    def run(self):
        self.root.mainloop()

    def start_text_input(self):
        txt = simpledialog.askstring("Szöveg bevitele", "Add meg a szöveget:")
        if txt:
            self.text_to_place = txt
            self.mode_var.set("Szöveg")

    def on_button_down(self, event):
        mode = self.mode_var.get()

        if mode == "Szöveg" and self.text_to_place:
            self.canvas.create_text(
                event.x, event.y,
                text=self.text_to_place,
                fill=self.draw_color, font=("Arial", 20)
            )
            self.text_to_place = None
            self.mode_var.set("Rajzolás")
            return

        if mode in ["Téglalap", "Négyzet", "Kör", "Vonal"]:
            self.start_x = event.x
            self.start_y = event.y
            return

        self.current_shape = MGShape(self.draw_color, self.line_width)
        self.current_shape.add_point((event.x, event.y))
        self.last_x = event.x
        self.last_y = event.y

    def on_move(self, event):
        mode = self.mode_var.get()

        if mode in ["Téglalap", "Négyzet", "Kör", "Vonal"]:
            self.canvas.delete("preview")
            if mode == "Téglalap":
                self.canvas.create_rectangle(
                    self.start_x, self.start_y, event.x, event.y,
                    outline=self.draw_color, width=self.line_width, tag="preview"
                )
            elif mode == "Négyzet":
                s = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
                ex = self.start_x + (s if event.x > self.start_x else -s)
                ey = self.start_y + (s if event.y > self.start_y else -s)
                self.canvas.create_rectangle(
                    self.start_x, self.start_y, ex, ey,
                    outline=self.draw_color, width=self.line_width, tag="preview"
                )
            elif mode == "Kör":
                self.canvas.create_oval(
                    self.start_x, self.start_y, event.x, event.y,
                    outline=self.draw_color, width=self.line_width, tag="preview"
                )
            elif mode == "Vonal":
                self.canvas.create_line(
                    self.start_x, self.start_y, event.x, event.y,
                    fill=self.draw_color, width=self.line_width, tag="preview"
                )
            return

        if not self.current_shape:
            return

        x, y = event.x, event.y
        style = self.line_style_var.get()
        dash = None
        if style == "Szaggatott":
            dash = (10, 5)
        elif style == "Pontozott":
            dash = (2, 4)

        self.canvas.create_line(
            self.last_x, self.last_y, x, y,
            fill=self.draw_color, width=self.line_width,
            smooth=True, dash=dash
        )

        self.current_shape.add_point((x, y))
        self.last_x = x
        self.last_y = y

        length = mg_distance_mg(self.current_shape.points[0], (x, y))
        self.coord_label.config(text=f"x: {x}  y: {y}  hossz: {length:.1f}")

    def on_button_up(self, event):
        mode = self.mode_var.get()
        self.canvas.delete("preview")

        if mode == "Téglalap":
            self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline=self.draw_color, width=self.line_width
            )
            return

        if mode == "Négyzet":
            s = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
            ex = self.start_x + (s if event.x > self.start_x else -s)
            ey = self.start_y + (s if event.y > self.start_y else -s)
            self.canvas.create_rectangle(
                self.start_x, self.start_y, ex, ey,
                outline=self.draw_color, width=self.line_width
            )
            return

        if mode == "Kör":
            self.canvas.create_oval(
                self.start_x, self.start_y, event.x, event.y,
                outline=self.draw_color, width=self.line_width
            )
            return

        if mode == "Vonal":
            self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y,
                fill=self.draw_color, width=self.line_width
            )
            return

        if self.current_shape:
            self.shapes.append(self.current_shape)
            self.current_shape = None

    def on_mouse_move_for_eraser(self, event):
        if self.draw_color != "#ffffff":
            if self.eraser_preview_id:
                self.canvas.delete(self.eraser_preview_id)
            return

        r = self.line_width * 2
        if self.eraser_preview_id:
            self.canvas.delete(self.eraser_preview_id)
        self.eraser_preview_id = self.canvas.create_oval(
            event.x - r, event.y - r,
            event.x + r, event.y + r,
            outline="#888888", width=1
        )

    def clear_canvas(self):
        self.canvas.delete("all")
        self.shapes = []

    def undo(self):
        self.canvas.delete("all")

    def random_color(self):
        self.draw_color = mg_random_color_mg()
        self.color_preview.config(background=self.draw_color)

    def choose_color(self):
        c = colorchooser.askcolor()
        if c and c[1]:
            self.draw_color = c[1]
            self.color_preview.config(background=self.draw_color)

    def use_eraser(self):
        self.draw_color = "#ffffff"
        self.color_preview.config(background=self.draw_color)

    def change_width(self):
        self.line_width = self.width_var.get()

    def save_canvas(self):
        f = filedialog.asksaveasfilename(defaultextension=".ps")
        if f:
            self.canvas.postscript(file=f)
            messagebox.showinfo("Mentve", "PostScript fájl mentve.")

    def save_png(self):
        f = filedialog.asksaveasfilename(defaultextension=".png")
        if not f:
            return
        self.root.update()
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = x + self.canvas.winfo_width()
        h = y + self.canvas.winfo_height()
        ImageGrab.grab((x, y, w, h)).save(f)
