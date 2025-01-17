import customtkinter as ctk
import json

class GuideText:
    def __init__(self, file_path):
        with open(file_path, "r") as file:
            self.data = json.load(file)

    def get_text(self, key):
        return self.data.get(key, f"Errore: la chiave '{key}' non è presente nel file JSON.")

class Guidelines(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.guide = GuideText("json/idx.json")
        self.title("Come funzionano gli elementi?")
        self.geometry("1000x900")
        self.resizable(False, False)

        self.configure(bg="#f0f0f0")

        # Bottone per 'Attributo'
        self.attribute_guide = self.create_button("Attributo", "#A9A9A9", self.on_attribute_guide_click)
        self.attribute_guide.place(x=30, y=40)

        # Bottone per 'Entita'
        self.entity_guide = self.create_button("Entita'", "#4CAF50", self.on_entity_guide_click)
        self.entity_guide.place(x=30, y=220)

        # Bottone per 'Associazione'
        self.relationship_guide = self.create_button("Associazione", "#2196F3", self.on_relationship_guide_click)
        self.relationship_guide.place(x=30, y=400)

        # Bottone per 'Generalizzazione'
        self.generalization_button = self.create_button("Generalizzazione", "#FF9800", self.on_generalization_guide_click)
        self.generalization_button.place(x=30, y=580)

        # Variabili di stato per i bottoni cliccati
        self.button_clicked = {"attributo": False, "entita": False, "associazione": False, "generalizzazione": False}

        self.guide_text_label = None

    def create_button(self, text, color, command):
        return ctk.CTkButton(
            self,
            text=text,
            fg_color=color,
            hover_color="#808080",
            width=150,
            height=150,
            corner_radius=15,
            font=("Arial", 14, "bold"),
            command=command
        )

    def on_attribute_guide_click(self):
        if not self.button_clicked["attributo"]:
            self.button_clicked["attributo"] = True
            self.show_guide_text("attributo")

    def on_entity_guide_click(self):
        if not self.button_clicked["entita"]:
            self.button_clicked["entita"] = True
            self.show_guide_text("entita")

    def on_relationship_guide_click(self):
        if not self.button_clicked["associazione"]:
            self.button_clicked["associazione"] = True
            self.show_guide_text("associazione")

    def on_generalization_guide_click(self):
        if not self.button_clicked["generalizzazione"]:
            self.button_clicked["generalizzazione"] = True
            self.show_guide_text("generalizzazione")

    def show_guide_text(self, key):
        text = self.guide.get_text(key)

        # Rimuovi il testo precedente se presente
        if self.guide_text_label:
            self.guide_text_label.place_forget()

        # Crea una nuova label per il testo
        self.guide_text_label = ctk.CTkLabel(self, text=text, width=800, height=200, anchor="w", font=("Arial", 12))

        # Posiziona il testo accanto al bottone
        y_position = self.get_button_y_position(key)
        self.guide_text_label.place(x=250, y=y_position)

    def get_button_y_position(self, key):
        # Ritorna la posizione verticale del bottone in base al bottone cliccato
        positions = {
            "attributo": 40,
            "entita": 220,
            "associazione": 400,
            "generalizzazione": 580
        }
        return positions.get(key, 40)

if __name__ == "__main__":
    app = Guidelines()
    app.mainloop()
