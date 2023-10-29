from tkinter import *
import pandas
import random
from tkinter import messagebox
BACKGROUND_COLOR = "#B1DDC6"

try:
    word_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    print("file not found")
    word_data = pandas.read_csv("data/french_words.csv")
except IndexError:
    print("french words empty")
    word_data = pandas.read_csv("data/french_words.csv")
finally:
    word_dict = {row.French: row.English for (index, row) in word_data.iterrows()}

if len(word_dict) == 0:
    word_data = pandas.read_csv("data/french_words.csv")
    word_dict = {row.French: row.English for (index, row) in word_data.iterrows()}
# -----------------------------------------------------------------------
# Random word on press


def pick_new_word():
    # generates a new card from the dictionary, restarts timer and then flips card after 3 seconds
    global rand_word
    rand_word = random.choice(list(word_dict.keys()))
    canvas.itemconfig(word_text, text=f"{rand_word}")
    canvas.itemconfig(language_text, text="French")
    canvas.itemconfig(canvas_image, image=card_front)
    window.after(3000, flip_card)


def flip_card():
    # flips card to reveal english translation
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(language_text, text="English")
    canvas.itemconfig(word_text, text=f"{word_dict[rand_word]}")


def know_word():
    # user was correct, remove word from list of words that can show up again, shuffles new card
    global word_data
    global word_dict
    word_data = word_data[word_data.French != rand_word]
    del word_dict[rand_word]
    try:
        word_data.to_csv("data/words_to_learn.csv", index=False)
    except FileNotFoundError:
        word_data.to_csv("data/french_words.csv", index=False)
    finally:
        print(f"deleted {rand_word}")
        finished_cards()
        pick_new_word()


def dont_know_word():
    # user does not know the word, add the word to a words_to_learn csv file, shuffles new card
    finished_cards()
    word_df = word_data[word_data.French == rand_word]
    print(word_df)
    try:
        with open("data/words_to_learn.csv") as file:
            print("")
    except FileNotFoundError:
        print("not found")
        word_df.to_csv("data/words_to_learn.csv", index=False)
    else:
        word_df.to_csv("data/words_to_learn.csv", mode='a', index=False, header=False)
    finally:
        finished_cards()
        pick_new_word()


def finished_cards():
    if len(word_dict) == 0:
        messagebox.showinfo(title="Congrats!", message="You finished your flash cards")
        quit()


# --------------------------------UI--------------------------------------
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(height=526, width=800)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)

language_text = canvas.create_text(400, 150, text="French", fill="black", font=("Ariel", 40, "italic"))
rand_word = random.choice(list(word_dict.keys()))
word_text = canvas.create_text(400, 263, text=f"{rand_word}", fill="black", font=("Ariel", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# buttons

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=dont_know_word)
wrong_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=know_word)
right_button.grid(row=1, column=1)

# -----------------------------------------------------------------------
window.after(3000, flip_card)
window.mainloop()
