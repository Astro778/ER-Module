import customtkinter as ctk
from Guideline import Guidelines
from PIL import Image
import subprocess

class Attribute:
    """Classe che rappresenta un attributo di un'entità."""
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.tag = f"attribute_{len(canvas.find_all())}"
        
        self.primary_key = False
        self.secondary_key = False

        self.canvas.tag_bind(self.tag, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.on_drag)

        if self.primary_key:
            self.canvas.create_line(x, y, x, y + 20, tags=(self.tag, "attribute"))
            self.canvas.create_aa_circle(
                x, y + 20, 5, 
                fill="black", 
                tags=(self.tag, "attribute")
            )

        elif self.secondary_key:
            self.canvas.create_line(x, y, x, y + 20, tags=(self.tag, "attribute"))
            self.canvas.create_aa_circle(
                x, y + 20, 5,
                fill="grey",
                tags=(self.tag, "attribute"))
        else:
            self.canvas.create_line(x, y, x, y + 20, tags=(self.tag, "attribute"))
            self.canvas.create_aa_circle(
                x, y + 20, 5,
                fill="white",
                tags=(self.tag, "attribute"))

    def on_press(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.canvas.move(self.tag, dx, dy)
        self.last_x = event.x
        self.last_y = event.y

class Entity:
    """Classe che rappresenta un'entità nel diagramma ER."""
    def __init__(self, canvas, x1, y1, x2, y2, text="Entità"):
        self.canvas = canvas
        self.tag = f"entity_{len(canvas.find_all())}"

        # Crea il rettangolo e il testo associati all'entità
        self.canvas.create_rectangle(
            x1 - 70, y1 - 70, x2, y2, fill="lightblue", outline="black", tags=(self.tag, "entity")
        )
        self.canvas.create_text(
            ((x1 + x2) - 70)  // 2, ((y1 + y2) - 70) // 2, text=text, fill="black", tags=(self.tag, "entity")
        )

        # Associa gli eventi di trascinamento
        self.canvas.tag_bind(self.tag, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.on_drag)
        #self.canvas.tag_bind(self.tag, "<ButtonPress-1>", self.on_click_outside)

        # Variabili per tracciare la posizione del mouse
        self.last_x = 0
        self.last_y = 0

    def on_press(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.canvas.move(self.tag, dx, dy)
        self.last_x = event.x
        self.last_y = event.y

    def on_click_outside(self, event):
        pass

class Relationship:
    """Classe che rappresenta una relazione nel diagramma ER."""
    def __init__(self, canvas, x, y, size=100):
        self.canvas = canvas
        self.tag = f"relationship_{len(canvas.find_all())}"

        # Coordinate del rombo (relazione)
        x1, y1 = x, y - size // 2
        x2, y2 = x + size // 2, y
        x3, y3 = x, y + size // 2
        x4, y4 = x - size // 2, y

        # Crea il rombo (relazione)
        self.canvas.create_polygon(
            x1, y1, x2, y2, x3, y3, x4, y4,
            fill="white", outline="black", width=2, tags=(self.tag, "relationship")
        )

        # Linee con frecce
        self.canvas.create_line(x4, y4, x4 - 50, y4, arrow="last", tags=(self.tag, "relationship"))
        self.canvas.create_line(x2, y2, x2 + 50, y2, arrow="last", tags=(self.tag, "relationship"))

        # Associa gli eventi di trascinamento
        self.canvas.tag_bind(self.tag, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.on_drag)

        # Variabili per tracciare la posizione del mouse
        self.last_x = 0
        self.last_y = 0

    def on_press(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.canvas.move(self.tag, dx, dy)
        self.last_x = event.x
        self.last_y = event.y

class Generalization:
    def __init__(self, canvas, x, y, super_entity_name, sub_entity_names):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.super_entity_name = super_entity_name
        self.sub_entity_names = sub_entity_names

        # Tag per identificare tutti gli elementi della generalizzazione
        self.tag = f"generalization_{len(canvas.find_all())}"

        # Dimensioni aggiornate
        rect_width = 160
        rect_height = 80
        spacing = 200  # Distanza tra super-entità e sotto-entità

        # Disegna la super-entità
        self.super_entity = self.canvas.create_rectangle(
            x, y, x + rect_width, y + rect_height, fill="#D3D3D3", outline="black", tags=self.tag
        )
        self.super_entity_text = self.canvas.create_text(
            x + rect_width // 2, y + rect_height // 2, text=super_entity_name, font=("Arial", 16), tags=self.tag
        )

        # Disegna le linee e le sotto-entità
        self.sub_entities = []
        self.lines = []
        for i, sub_entity_name in enumerate(sub_entity_names):
            sub_x = x - (len(sub_entity_names) - 1) * spacing // 2 + (i * spacing)
            sub_y = y + rect_height + 100

            # Linea di collegamento
            line = self.canvas.create_line(
                x + rect_width // 2, y + rect_height, sub_x + rect_width // 2, sub_y,
                fill="black", width=3, tags=self.tag
            )
            self.lines.append(line)

            # Sotto-entità
            sub_entity = self.canvas.create_rectangle(
                sub_x, sub_y, sub_x + rect_width, sub_y + rect_height,
                fill="#ADD8E6", outline="black", tags=self.tag
            )
            sub_entity_text = self.canvas.create_text(
                sub_x + rect_width // 2, sub_y + rect_height // 2, text=sub_entity_name, font=("Arial", 16), tags=self.tag
            )

            self.sub_entities.append((sub_entity, sub_entity_text))

        # Associa gli eventi di trascinamento
        self.canvas.tag_bind(self.tag, "<ButtonPress-1>", self.on_press)
        self.canvas.tag_bind(self.tag, "<B1-Motion>", self.on_drag)

        # Variabili per tracciare la posizione del mouse
        self.last_x = 0
        self.last_y = 0

    def on_press(self, event):
        """Registra la posizione del mouse al momento del click."""
        self.last_x = event.x
        self.last_y = event.y

    def on_drag(self, event):
        """Sposta tutti gli elementi della generalizzazione."""
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        self.canvas.move(self.tag, dx, dy)
        self.last_x = event.x
        self.last_y = event.y

class ERDesignerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.guide = Guidelines()  # Avvio della finestra di guida
        self.title("ER Model Designer")
        self.geometry("1400x1000")
        self.resizable(False, False)

        # Layout
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.sidebar.pack(side="left", fill="y")

        self.canvas = ctk.CTkCanvas(self, bg="white", highlightthickness=0)
        self.canvas.pack(side="right", fill="both", expand=True)

        # Icona dei pulsanti
        self.file_image = ctk.CTkImage(Image.open("images\\folder.png"), size=(40, 40))
        self.guida_image = ctk.CTkImage(Image.open("images\\information-book.png"), size=(40, 40))

        # Pulsante "File"
        self.file_button = ctk.CTkButton(
            self.sidebar,
            text="",
            image=self.file_image,
            fg_color="transparent",
            width=0,
            height=0
        )
        self.file_button.pack(pady=0, padx=0)
        self.file_button.place(x=0, y=0)
        # Pulsante "Guida"
        self.guida_button = ctk.CTkButton(
            self.sidebar,
            text="",
            image=self.guida_image,
            fg_color="transparent",
            width=0,
            height=0,
            command=self.open_guide
        )
        self.guida_button.pack(pady=0, padx=0)
        self.file_button.place(x=20, y=0)
        # Pulsanti per aggiungere entità e relazioni
        self.add_entity_button = ctk.CTkButton(
            self.sidebar,
            text="Aggiungi Entita'",
            fg_color="#4CAF50",  
            hover_color="#45a049",  
            width=200,
            height=100,
            corner_radius=15,  
            font=("Arial", 14, "bold"),  
            command=self.add_entity 
        )
        self.add_entity_button.pack(pady=100, padx=10)

        self.add_relationship_button = ctk.CTkButton(
            self.sidebar,
            text="Aggiungi Relazione",
            fg_color="#2196F3",  
            hover_color="#1E88E5", 
            width=200,
            height=100,
            corner_radius=15,  
            font=("Arial", 14, "bold"),  
            command=self.add_relationship 
        )
        self.add_relationship_button.pack(pady=10, padx=10)
        
        # Pulsanti per aggiungere generalizzazioni
        self.add_generalization_button = ctk.CTkButton(
            self.sidebar,
            text="Aggiungi Generalizzazione",
            fg_color="#FF9800",  
            hover_color="#F57C00", 
            width=200,
            height=100,
            corner_radius=15,  
            font=("Arial", 14, "bold"),  
            command=self.add_generalization 
        )
        self.add_generalization_button.pack(pady=100, padx=10)

        self.add_attribute_button = ctk.CTkButton(
            self.sidebar,
            text="Aggiungi Attributo",
            fg_color="#FF9800",  
            hover_color="#F57C00", 
            width=200,
            height=100,
            corner_radius=15,  
            font=("Arial", 14, "bold"),  
            command=self.add_attribute 
        )
        self.add_attribute_button.pack(pady=100, padx=10)

    def add_attribute(self):
        Attribute(self.canvas, 100, 100)

    def add_entity(self):
        Entity(self.canvas, 100, 100, 200, 200)

    def add_relationship(self):
        Relationship(self.canvas, 150, 150)

    def add_generalization(self):
        # Ottieni i dati dall'utente
        super_entity_name = ctk.CTkInputDialog(text="Nome della super-entità:", title="Super Entità").get_input()
        sub_entity_names = []

        for i in range(2):  # Supponiamo due sotto-entità per semplicità
            name = ctk.CTkInputDialog(text=f"Nome della sotto-entità {i+1}:", title="Sotto Entità").get_input()
            if name:
                sub_entity_names.append(name)

        # Controlla che tutti i nomi siano validi
        if super_entity_name and sub_entity_names:
            # Posizioni iniziali
            x, y = 300, 100  # Modifica le coordinate se necessario

            # Crea la generalizzazione
            Generalization(self.canvas, x, y, super_entity_name, sub_entity_names)
        else:
            ctk.CTkMessagebox.show_error(title="Errore", message="Inserisci nomi validi per tutte le entità!")

    def open_guide(self):
        try:
            subprocess.Popen(["python", "Guideline.py"])
        except Exception as e:
            print(f"Errore durante l'apertura della guida: {e}")

if __name__ == "__main__":
    app = ERDesignerApp()
    app.mainloop()