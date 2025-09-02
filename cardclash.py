import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json
import os
import random

print("Current working directory:", os.getcwd())

class Card:
    def __init__(self, name, elixir, rarity, type_, damage, hit_speed, hp):
        self.name = name
        self.elixir = elixir
        self.rarity = rarity
        self.type_ = type_
        self.damage = damage
        self.hit_speed = hit_speed
        self.hp = hp

class CardDatabase:
    def __init__(self):
        self.cards = self.load_cards()

    def load_cards(self):
        if not os.path.exists("cards.json"):
            return []
        with open("cards.json", "r") as f:
            data = json.load(f)
            return [Card(
                name=entry['name'],
                elixir=entry['elixir'],
                rarity=entry['rarity'],
                type_=entry['type'],
                damage=entry['damage'],
                hit_speed=entry['hit_speed'],
                hp=entry['hp']
            ) for entry in data]

    def get_card_by_name(self, name):
        for card in self.cards:
            if card.name == name: 
                return card
        return None

class ComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Clash: Clash Royale Comparator & Deck Builder")
        self.root.geometry("950x650")
        self.root.configure(bg="#1e1e2e")

        self.db = CardDatabase()
        self.deck = []

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Card Clash", font=("Clash", 24, "bold"), bg="#1e1e2e", fg="#f5f5f5")
        title.pack(pady=20)

        frame = tk.Frame(self.root, bg="#1e1e2e")
        frame.pack(pady=10)

        self.combo1 = ttk.Combobox(frame, values=[card.name for card in self.db.cards], state="readonly", width=30)
        self.combo2 = ttk.Combobox(frame, values=[card.name for card in self.db.cards], state="readonly", width=30)
        self.combo1.grid(row=0, column=0, padx=10, pady=5)
        self.combo2.grid(row=0, column=1, padx=10, pady=5)

        self.img_label1 = tk.Label(frame, bg="#1e1e2e")
        self.img_label1.grid(row=1, column=0, padx=10, pady=5)
        self.img_label2 = tk.Label(frame, bg="#1e1e2e")
        self.img_label2.grid(row=1, column=1, padx=10, pady=5)

        self.combo1.bind("<<ComboboxSelected>>", lambda e: self.show_card_image(self.combo1.get(), self.img_label1))
        self.combo2.bind("<<ComboboxSelected>>", lambda e: self.show_card_image(self.combo2.get(), self.img_label2))

        button_frame = tk.Frame(self.root, bg="#1e1e2e")
        button_frame.pack(pady=10)

        compare_btn = tk.Button(button_frame, text="Compare", command=self.compare_cards, bg="#8aadf4", fg="white", font=("Clash", 12), width=15)
        compare_btn.grid(row=0, column=0, padx=5)

        clear_btn = tk.Button(button_frame, text="Clear", command=self.clear, bg="#f38ba8", fg="white", font=("Clash", 12), width=15)
        clear_btn.grid(row=0, column=1, padx=5)

        add_deck_btn = tk.Button(button_frame, text="Add to Deck", command=self.add_to_deck, bg="#a6e3a1", fg="black", font=("Clash", 12), width=15)
        add_deck_btn.grid(row=0, column=2, padx=5)

        view_deck_btn = tk.Button(button_frame, text="View Deck", command=self.view_deck, bg="#f9e2af", fg="black", font=("Clash", 12), width=15)
        view_deck_btn.grid(row=0, column=3, padx=5)

        clear_deck_btn = tk.Button(button_frame, text="Clear Deck", command=self.clear_deck, bg="#eba0ac", fg="white", font=("Clash", 12), width=15)
        clear_deck_btn.grid(row=0, column=4, padx=5)

        # New Surprise button (separate from above row)
        surprise_btn = tk.Button(self.root, text="Surprise Me!", command=self.surprise_me, 
                         bg="#cba6f7", fg="black", font=("Clash", 12), width=20)
        surprise_btn.pack(pady=15)   # This will make it appear BELOW the comparison section

        # Create the comparison result frame (instead of text widget)
        self.result_frame = tk.Frame(self.root, bg="#2e2e3e", bd=2, relief="groove")
        self.result_frame.pack(pady=10, fill = "x", padx = 20)

        self.result_frame.grid_columnconfigure(0, weight=1)  # spacer
        self.result_frame.grid_columnconfigure(1, weight=0)
        self.result_frame.grid_columnconfigure(2, weight=0)
        self.result_frame.grid_columnconfigure(3, weight=0)
        self.result_frame.grid_columnconfigure(4, weight=1)  # spacer

        header_font = ("Clash", 12, "bold")
        tk.Label(self.result_frame, text="", bg="#2e2e3e").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.result_frame, text="Card 1", font=header_font, fg="#8aadf4", bg="#2e2e3e").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.result_frame, text="Stat", font=header_font, fg="white", bg="#2e2e3e").grid(row=0, column=2, padx=5, pady=5)
        tk.Label(self.result_frame, text="Card 2", font=header_font, fg="#8aadf4", bg="#2e2e3e").grid(row=0, column=3, padx=5, pady=5)

        self.stat_rows = {
            "elixir": 1,
            "rarity": 2,
            "type": 3,
            "damage": 4,
            "hit_speed": 5,
            "hp": 6
        }

        self.card1_stat_labels = {}
        self.card2_stat_labels = {}

        for stat, row in self.stat_rows.items():
            stat_name = stat.replace("_", " ").title()
            tk.Label(self.result_frame, text=stat_name, fg="white", bg="#2e2e3e", font=("Clash", 11)).grid(row=row, column=2, padx=5, pady=3)

            lbl1 = tk.Label(self.result_frame, text="", fg="white", bg="#2e2e3e", font=("Clash", 11))
            lbl1.grid(row=row, column=1, padx=5, pady=3)
            self.card1_stat_labels[stat] = lbl1

            lbl2 = tk.Label(self.result_frame, text="", fg="white", bg="#2e2e3e", font=("Clash", 11))
            lbl2.grid(row=row, column=3, padx=5, pady=3)
            self.card2_stat_labels[stat] = lbl2

    def show_card_image(self, card_name, label_widget):
        image_path = os.path.join(self.base_dir, "images", f"{card_name}.png")
        print(f"Trying to load image: {image_path}")

        if not os.path.isfile(image_path):
            print(f"Image file not found: {image_path}")
            label_widget.config(image="", text="Image\nnot found", fg="white",
                                font=("Clash", 10), justify="center")
            label_widget.image = None
            return

        try:
            image = Image.open(image_path)
            image = image.resize((100, 120), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            label_widget.config(image=photo, text="")
            label_widget.image = photo  # Keep reference!
        except Exception as e:
            print(f"Error loading image: {e}")
            label_widget.config(image="", text="Image\nnot found", fg="white",
                                font=("Clash", 10), justify="center")
            label_widget.image = None

    def compare_cards(self):
        name1 = self.combo1.get()
        name2 = self.combo2.get()

        # Clear previous results
        for stat in self.card1_stat_labels:
            self.card1_stat_labels[stat].config(text="", bg="#2e2e3e")
            self.card2_stat_labels[stat].config(text="", bg="#2e2e3e")

        if name1 == name2:
            messagebox.showinfo("Invalid Selection", "Please select two different cards.")
            return

        card1 = self.db.get_card_by_name(name1)
        card2 = self.db.get_card_by_name(name2)

        if not card1 or not card2:
            messagebox.showinfo("Invalid Selection", "Please select valid cards.")
            return

        def better_color(val1, val2, higher_is_better=True):
            if val1 == val2:
                return "#2e2e3e", "#2e2e3e"
            if (val1 > val2 and higher_is_better) or (val1 < val2 and not higher_is_better):
                return "#1ad626", "red"
            else:
                return "red", "#1ad626"

        # Elixir (lower better)
        c1_color, c2_color = better_color(card1.elixir, card2.elixir, higher_is_better=False)
        self.card1_stat_labels["elixir"].config(text=str(card1.elixir), bg=c1_color)
        self.card2_stat_labels["elixir"].config(text=str(card2.elixir), bg=c2_color)

        # Rarity order for comparison
        rarity_order = {"common": 1, "rare": 2, "epic": 3, "legendary": 4}
        r1 = rarity_order.get(card1.rarity.lower(), 0)
        r2 = rarity_order.get(card2.rarity.lower(), 0)
        c1_color, c2_color = better_color(r1, r2)
        self.card1_stat_labels["rarity"].config(text=card1.rarity.capitalize(), bg=c1_color)
        self.card2_stat_labels["rarity"].config(text=card2.rarity.capitalize(), bg=c2_color)

        # Type (no color)
        self.card1_stat_labels["type"].config(text=card1.type_.capitalize())
        self.card2_stat_labels["type"].config(text=card2.type_.capitalize())

        # Damage (higher better)
        c1_color, c2_color = better_color(card1.damage, card2.damage)
        self.card1_stat_labels["damage"].config(text=str(card1.damage), bg=c1_color)
        self.card2_stat_labels["damage"].config(text=str(card2.damage), bg=c2_color)

        # Hit Speed (lower better)
        c1_color, c2_color = better_color(card1.hit_speed, card2.hit_speed, higher_is_better=False)
        self.card1_stat_labels["hit_speed"].config(text=str(card1.hit_speed), bg=c1_color)
        self.card2_stat_labels["hit_speed"].config(text=str(card2.hit_speed), bg=c2_color)

        # HP (higher better)
        c1_color, c2_color = better_color(card1.hp, card2.hp)
        self.card1_stat_labels["hp"].config(text=str(card1.hp), bg=c1_color)
        self.card2_stat_labels["hp"].config(text=str(card2.hp), bg=c2_color)

    def clear(self):
        self.combo1.set("")
        self.combo2.set("")
        self.img_label1.config(image="", text="")
        self.img_label2.config(image="", text="")
        for stat in self.card1_stat_labels:
            self.card1_stat_labels[stat].config(text="", bg="#2e2e3e")
            self.card2_stat_labels[stat].config(text="", bg="#2e2e3e")

    def add_to_deck(self):
        selected = self.combo1.get()
        card = self.db.get_card_by_name(selected)
        if not card:
            messagebox.showwarning("Invalid", "Select a valid card to add to deck.")
            return

        if len(self.deck) >= 8:
            messagebox.showinfo("Deck Full", "Maximum of 8 cards allowed in deck.")
            return

        self.deck.append(card)
        messagebox.showinfo("Added", f"{card.name} added to deck.")

    def view_deck(self):
        if not self.deck:
            messagebox.showinfo("Empty Deck", "No cards in deck.")
            return

        deck_window = tk.Toplevel(self.root)
        deck_window.title("Your Deck")
        deck_window.geometry("600x400")

        deck_frame = tk.Frame(deck_window)
        deck_frame.pack(pady=10)

        total_elixir = 0
        for idx, card in enumerate(self.deck):
            try:
                image_path = os.path.join(self.base_dir, "images", f"{card.name}.png")
                image = Image.open(image_path)
                image = image.resize((60, 72), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                img_label = tk.Label(deck_frame, image=photo)
                img_label.image = photo
                img_label.grid(row=idx // 4 * 2, column=idx % 4, padx=5, pady=5)
            except Exception:
                img_label = tk.Label(deck_frame, text="No Image", width=8, height=5, bg="grey")
                img_label.grid(row=idx // 4 * 2, column=idx % 4, padx=5, pady=5)

            text_label = tk.Label(deck_frame, text=f"{card.name}\nElixir: {card.elixir}", bg="#f0f0f0", font=("Clash", 10), justify="center")
            text_label.grid(row=idx // 4 * 2 + 1, column=idx % 4, padx=5, pady=2)

            total_elixir += card.elixir

        avg_elixir = total_elixir / len(self.deck)
        avg_label = tk.Label(deck_window, text=f"Average Elixir Cost: {avg_elixir:.1f}", font=("Clash", 14))
        avg_label.pack(pady=10)

    def surprise_me(self):
        if not self.db.cards:
            messagebox.showwarning("No Cards", "Your database is empty.")
            return

        k = min(8, len(self.db.cards))  # random deck up to 8 cards
        self.deck = random.sample(self.db.cards, k)

        messagebox.showinfo("Surprise!", f"Built a random deck of {k} card(s).")
        self.view_deck()

        # Finally, add annotations with ChatGPT and push the code to GitHub

    def clear_deck(self):
        """Clears all cards from the deck."""
        if not self.deck:
            messagebox.showinfo("Deck Empty", "Your deck is already empty!")
            return
        self.deck.clear()
        messagebox.showinfo("Deck Cleared", "Your deck has been cleared.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ComparisonApp(root)
    root.mainloop()
