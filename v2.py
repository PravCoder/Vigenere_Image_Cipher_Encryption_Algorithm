# LIBRARIES IMPORT
from tkinter import *

letters = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"

letter_indx = dict(zip(letters, range(len(letters))))
indx_letter = dict(zip(range(len(letters)), letters))
grid = [] 
text = ""
cipher_text = ""
key = ""
final = ""

def generate_grid():
    for row in range(26):
        grid.append([])
    
    for i, row in enumerate(grid):
        j = i
        while len(row) < 26:
            grid[i].append(indx_letter[j])
            j += 1
            
    return grid

def encode():
    global text
    global key
    letters = "abcdefghijklmnopqrstuvwxyz"
    letter_indx = dict(zip(letters, range(len(letters)))) 
    cipher_text = ""   # stores finial encoded-text
    text_no_spaces = ""  # stores the plaintext with no spaces
    space_indicies = []  # stores the non-alphabet characters, each element is (char,indx)
    character_pairs = []  # stores the mapping of each text adn key character

    for i, char in enumerate(text):    
        if char not in letters:  # if the character is non-aplphabet
            space_indicies.append((char,i)) # add it to space-indicies
        else:
            text_no_spaces += char  # else its a normal letter add it no-spaces-text

    while len(key) < len(text):  # for cyclle matching make sure length of key is greater than length of text
        key += key
                               
    for i, char in enumerate(text_no_spaces):
        character_pairs.append((char,key[i]))  # mapping each character in text to each char in key using corresponding index, (text-char, key-char)
  
    for pair in character_pairs:  # pair = (text-char,key-char)
        col = letter_indx[pair[0]]  # col = letter_indx-dict[text-char]
        row = letter_indx[pair[1]]  # row = letter_indx-dict[key-char]
        letter = grid[row][col]     # extracting encoded letter from grid using row/col indicies
        cipher_text += letter
    
    for char in space_indicies:  # char = (special-character, index)
        cipher_text = cipher_text[:char[1]] + char[0] + cipher_text[char[1]:]  # inserting special-characters in string

    return "Encrypted text: " + cipher_text

def decode():
    global cipher_text
    global key
    og_key=  key
    letters = "abcdefghijklmnopqrstuvwxyz"
    letter_indx = dict(zip(letters, range(len(letters)))) 
    indx_letter = dict(zip(range(len(letters)), letters))
    text_no_spaces = ""
    decrypted_text = ""
    character_pairs = []
    non_alpha_indicies = []

    for i, char in enumerate(cipher_text):
        if char not in letters:
            non_alpha_indicies.append((char, i))
        else:
            text_no_spaces += char

    while len(key) < len(cipher_text):
        key += key
    
    for i, char in enumerate(text_no_spaces):
        character_pairs.append((char,key[i]))

    for pair in character_pairs:
        row = letter_indx[pair[1]]
        for i, letter in enumerate(grid[row]):
            if letter == pair[0]:
                decrypted_letter = indx_letter[i]
                decrypted_text += decrypted_letter
    
    for char in non_alpha_indicies:
        decrypted_text = decrypted_text[:char[1]] + char[0] + decrypted_text[char[1]:]
    return decrypted_text


  
root = Tk()
root.title("Vigenere Encode / Decode")
root.geometry("1280x720")
root.resizable(width=False, height=False)

def decodeScreen():    
    for widget in root.winfo_children():
        widget.destroy()
    titleLabel = Label(text = "VIGENERE DECODER", font = ("SofiaPro-SemiBold", 15))
    titleLabel.place(anchor = CENTER, x = "640", y = "30")
    textLabel = Label(text = "Enter the text you want to decode and its key.", font = ("Montserrat", 10))
    textLabel.place(anchor = CENTER, x = "640", y = "100")
    decodeLabel = Label(text = "TEXT TO DECODE", font = ("Montserrat", 10))
    decodeLabel.place(anchor = CENTER, x = "640", y = "180")
    entryBox1 = Entry(width = "60")
    entryBox1.place(x = "640", y = "200", anchor = CENTER)
    def setCipher(arg):
        global cipher_text
        cipher_text = entryBox1.get()
        entryBox1.delete(0, END)
    entryBox1.bind("<Return>", setCipher)
    keyLabel = Label(text = "KEY", font = ("Montserrat", 10))
    keyLabel.place(anchor = CENTER, x = "640", y = "280")
    entryBox2 = Entry(width = "60")
    entryBox2.place(x = "640", y = "300", anchor = CENTER)
    def setKey(arg):
        global key
        key = entryBox2.get()
        entryBox2.delete(0, END)
    entryBox2.bind("<Return>", setKey)
    def finish():
        decode()
        decodeLabel = Label(text = "ORIGINAL TEXT", font = ("SofiaPro-SemiBold", 10))
        decodeLabel.place(anchor = CENTER, x = "640", y = "480")
        decodeInfo = Label(text = cipher_text, font = ("Montserrat", 10))
        decodeInfo.place(anchor = CENTER, x = "640", y = "500")
        keyLabel = Label(text = "KEY", font = ("SofiaPro-SemiBold", 10))
        keyLabel.place(anchor = CENTER, x = "640", y = "530")
        keyInfo = Label(text = key, font = ("Montserrat", 10))
        keyInfo.place(anchor = CENTER, x = "640", y = "550")
        decodedLabel = Label(text = "DECODED TEXT", font = ("SofiaPro-SemiBold", 10))
        decodedLabel.place(anchor = CENTER, x = "640", y = "580")
        decodedInfo = Label(text = decode(), font = ("Montserrat", 10))
        decodedInfo.place(anchor = CENTER, x = "640", y = "600")
        root.update()
    finish = Button(text = "FINISH", font="SofiaPro-SemiBold", width = "5", height = "1", command = finish)
    finish.place(x = "640", y = "400", anchor = CENTER)

    # Back Button
    back = Button(text = "BACK", font="SofiaPro-SemiBold", width = "5", height = "1", command = backScreen)
    back.place(x = "1200", y = "670", anchor = CENTER)

def encodeScreen():
    for widget in root.winfo_children():
        widget.destroy()
    titleLabel = Label(text = "VIGENERE ENCODER", font = ("SofiaPro-SemiBold", 15))
    titleLabel.place(anchor = CENTER, x = "640", y = "30")
    textLabel = Label(text = "Input what you want to encode and a key.", font = ("Montserrat", 10))
    textLabel.place(anchor = CENTER, x = "640", y = "100")
    decodeLabel = Label(text = "TEXT TO ENCODE", font = ("Montserrat", 10))
    decodeLabel.place(anchor = CENTER, x = "640", y = "180")
    def setText(arg):
        global text
        text = entryBox1.get()
        entryBox1.delete(0, END)
    entryBox1 = Entry(width = "60")
    entryBox1.place(x = "640", y = "200", anchor = CENTER)
    entryBox1.bind("<Return>", setText)

    keyLabel = Label(text = "KEY", font = ("Montserrat", 10))
    keyLabel.place(anchor = CENTER, x = "640", y = "280")
    def setKey(arg):
        global key
        key = entryBox2.get()
        entryBox2.delete(0, END)
    entryBox2 = Entry(width = "60")
    entryBox2.place(x = "640", y = "300", anchor = CENTER)
    entryBox2.bind("<Return>", setKey)
    def finish():
        decode()
        decodeLabel = Label(text = "TEXT", font = ("SofiaPro-SemiBold", 10))
        decodeLabel.place(anchor = CENTER, x = "640", y = "480")
        decodeInfo = Label(text = text, font = ("Montserrat", 10))
        decodeInfo.place(anchor = CENTER, x = "640", y = "500")
        keyLabel = Label(text = "KEY", font = ("SofiaPro-SemiBold", 10))
        keyLabel.place(anchor = CENTER, x = "640", y = "530")
        keyInfo = Label(text = key, font = ("Montserrat", 10))
        keyInfo.place(anchor = CENTER, x = "640", y = "550")
        decodedLabel = Label(text = "ENCRYPTED TEXT", font = ("SofiaPro-SemiBold", 10))
        decodedLabel.place(anchor = CENTER, x = "640", y = "580")
        decodedInfo = Label(text = encode(), font = ("Montserrat", 10))
        decodedInfo.place(anchor = CENTER, x = "640", y = "600")
    finish = Button(text = "FINISH", font="SofiaPro-SemiBold", width = "5", height = "1", command = finish)
    finish.place(x = "640", y = "400", anchor = CENTER)
    # Back Button
    back = Button(text = "BACK", font="SofiaPro-SemiBold", width = "5", height = "1", command = backScreen)
    back.place(x = "1200", y = "670", anchor = CENTER)
    
def backScreen():
    for widget in root.winfo_children():
        widget.destroy()
    titleLabel = Label(text = "VIGENERE ENCODER / DECODER", font = ("SofiaPro-SemiBold", 15))
    titleLabel.place(anchor = CENTER, x = "640", y = "30")
    textLabel = Label(text = "Choose an option.", font = ("Montserrat", 10))
    textLabel.place(anchor = CENTER, x = "640", y = "100")
    decode = Button(text = "DECODE", font="SofiaPro-SemiBold", width = "50", height = "3", command = decodeScreen)
    decode.place(x = "640", y = "200", anchor = CENTER)
    encode = Button(text = "ENCODE", font="SofiaPro-SemiBold", width = "50", height = "3", command = encodeScreen)
    encode.place(x = "640", y = "300", anchor = CENTER)
    
def gui():
    # UI START
    # UI Title Label
    titleLabel = Label(text = "VIGENERE ENCODER / DECODER", font = ("SofiaPro-SemiBold", 15))
    titleLabel.place(anchor = CENTER, x = "640", y = "30")
    textLabel = Label(text = "Choose an option.", font = ("Montserrat", 10))
    textLabel.place(anchor = CENTER, x = "640", y = "100")
    # Buttons :')
    decode = Button(text = "DECODE", font="SofiaPro-SemiBold", width = "50", height = "3", command = decodeScreen)
    decode.place(x = "640", y = "200", anchor = CENTER)
    encode = Button(text = "ENCODE", font="SofiaPro-SemiBold", width = "50", height = "3", command = encodeScreen)
    encode.place(x = "640", y = "300", anchor = CENTER)
    root.mainloop()

def main():
    generate_grid()
    gui()

main()









# Enter message: hello
# Enter key: asd
# hwolg

# THIS WORKS