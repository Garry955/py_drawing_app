# 🖌️ py_drawing_app  
Egyszerű Python rajzoló alkalmazás Tkinter felhasználásával.  
A projekt célja egy könnyen használható grafikus szerkesztő létrehozása, amely az egér mozgásával rajzol egy vászonra.

---

## 👤 Hallgató
**Név:** Marosy Gergő
**Neptunkód:** T70ALL
**Tantárgy:** Szkript nyelvek – Python

---

# 📌 Projekt futtatása:

MacOS: Terminálban a projekt mappából a következő paranccsal: python3 main.py
       Vagy.. VSCode-ban:

            Nyisd meg a projekt mappát.
            Nyisd meg a main.py fájlt.
            A jobb felső sarokban a Run ▶ gombbal futtasd.
            Vagy a felső menüben:
            Run → Run Without Debugging

Windows/Linux: Terminálban a projekt mappából a következő paranccsal: python main.py

# 📌 Feladat leírása

A projekt egy egyszerű, moduláris felépítésű Python alkalmazás, amely lehetővé teszi:

- vonalak rajzolását az egérrel  
- a rajz visszavonását (Undo)  
- a teljes vászon törlését  
- véletlenszerű szín választását  
- a rajz mentését PostScript formátumban  
- vonalvastagság beállítását  


# 📌 Program összetétele:

- **modulok** → `math`, `random`, `tkinter`, `math`
- **saját modul** → `MG_utils.py`
- **saját függvény** → `mg_distance_mg`
- **saját osztály** → `MGShape` a `MG_shapes.py` modulban
- grafikus felület → `Tkinter`
- eseménykezelés → egérkattintások és egérmozgás kezelése a vásznon
- projekt GitHubon → verziókövetéssel

---

# 🗂️ Projekt felépítése

---

# 🔧 Modulok és funkciók

## 1️⃣ `main.py`
A program belépési pontja.  
Feladata az alkalmazás elindítása a `MGApp` példányával.

---

## 2️⃣ `app.py`
A grafikus alkalmazás fő modulja.  
Tartalmazza:

### ✔ MGApp osztály
Felelős:
- az ablak létrehozásáért (`root`)
- a rajzvászon (Canvas) megjelenítéséért
- a gombok, vezérlők, eseménykezelők kezeléséért

### Fő funkciók:
- `on_button_down` – rajzolás kezdete
- `on_move` – folytonos rajzolás egérmozgásra
- `on_button_up` – rajzolás befejezése
- `clear_canvas` – vászon törlése
- `undo` – utolsó vonal eltávolítása
- `random_color` – véletlenszerű szín választása
- `change_width` – vonalvastagság beállítása
- `start_text_input` – szöveg bevitele
- `on_mouse_move_for_eraser`,`use_eraser`  – radírozás funkció
- `choose_color` – színválasztó paletta
- `save_canvas` – mentés PostScript formátumban
- `save_png` – mentés PNG formátumban

---

## 3️⃣ `MG_utils.py` (Saját modul – **MG** monogram kötelező!)
Tartalmazza a saját függvényeket:

- `mg_distance_mg(p1, p2)`  
  Két pont távolságát számítja (math.hypot).  

- `mg_angle_mg(p1, p2)`  
  Két pont közötti szög fokban (math.atan2).  

- `mg_length_sqrt_mg(dx, dy)`  
  Egy vektor hosszát számítja (math.sqrt).  

- `mg_random_color_mg()`  
  Véletlenszerű hex szín előállítása.

---

## 4️⃣ `MG_shapes.py` (Saját osztály modul – **MG**)
Tartalmazza a projekt saját osztályát:

### ✔ `MGShape` osztály
Feladata:
- a rajzolt vonal pontjainak tárolása
- a vonal kirajzolása a vászonra (`draw_on`)
- a teljes vonal hosszának számítása (`length`)
- a súlypont meghatározása (`centroid`)
- bounding box előállítása (`bounding_box`)

---

# 🎨 Grafikus felület

A program a Python beépített `tkinter` modulját használja:

- `Canvas` objektum a rajzoláshoz  
- `Button`, `Spinbox`, `Label` a kezelőfelülethez  
- események:
  - `<Button-1>`
  - `<B1-Motion>`
  - `<ButtonRelease-1>`

---

# 🖱️ Eseménykezelés

A rajzolás folyamata:

| Esemény | Funkció |
|--------|---------|
| Egér lenyomása | új MGShape létrehozása |
| Egér mozgatása | vonal folytatása, megjelenítés a canvas-on |
| Egér felengedése | a kész vonal eltárolása |

---

# 💾 Mentés

A rajz menthető **PostScript (.ps)** és **PNG (.png)** formátumban


