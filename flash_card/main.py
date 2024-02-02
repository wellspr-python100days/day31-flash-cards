import pandas as pd
import tkinter as tk
import random

BACKGROUND_COLOR = "#B1DDC6"

#Open words list
try:
    print("Looking for practice file...")
    words_list = pd.read_csv("data/words_to_practice.csv")
    print("Opening practice file.")
except:
    print("No practice file found. ")
    words_list = pd.read_csv("data/french_words.csv")
    print("Opening default file")

french_words = words_list.French.to_list()
english_words = words_list.English.to_list()
words_dict = { entry.French: entry.English for (index, entry) in words_list.iterrows() }
print(f"Words count: {len(french_words)}")

timer = None
word = ""

def right():
    global french_words
    french_words = [french_word for french_word in french_words if french_word != word]
    print(word, len(french_words))
    next_card()


def wrong():
    next_card()


def next_card():
    global word, timer

    if timer:
        window.after_cancel(timer)

    word = random.choice(french_words)
    translation = words_dict[word]
    
    create_card(word)
    
    timer = window.after(3000, flip_card, translation)


def create_card(word):
    canvas.itemconfig(canvas_image, image=img_card_front)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=word, fill="black")


def flip_card(translation):
    canvas.itemconfig(canvas_image, image=img_card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=translation, fill="white")

#================
window = tk.Tk()
window.title("Flash Cards Learning")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

img_card_front = tk.PhotoImage(file="images/card_front.png")
img_card_back = tk.PhotoImage(file="images/card_back.png")
img_right = tk.PhotoImage(file="images/right.png")
img_wrong = tk.PhotoImage(file="images/wrong.png")

canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
canvas_image = canvas.create_image(400, 263)

title_text = canvas.create_text(400, 150, font=("Arial", 30, "italic"))
word_text = canvas.create_text(400, 263, font=("Arial", 45, "bold"))

button_wrong = tk.Button(
    image=img_wrong, 
    bg=BACKGROUND_COLOR, 
    highlightcolor=BACKGROUND_COLOR, 
    highlightthickness=0,
    command=wrong
)
button_right = tk.Button(
    image=img_right, 
    bg=BACKGROUND_COLOR, 
    highlightcolor=BACKGROUND_COLOR, 
    highlightthickness=0,
    command=right
)

button_wrong.grid(column=0, row=1)
button_right.grid(column=1, row=1)

next_card()

window.mainloop()

print("Saving words to practice....")

df = pd.DataFrame({
    "French": [word for word in french_words],
    "English": [words_dict[word] for word in french_words]
})

df.to_csv("data/words_to_practice.csv", index=False)
print("Bye.")