import pygame

letters = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
letter_indx = dict(zip(letters, range(len(letters))))
indx_letter = dict(zip(range(len(letters)), letters))
grid = [] 

class Letter:
    def __init__(self, letter):
        self.letter = letter

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
    text = input("Enter plaintext message: ") # SET THIS EQUAL TO PLAINTEXT TEXTBOX INPUT
    key = input("Enter key: ")                # SET THIS EQUAL T0 KEY TEXTBOX INPUT
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
        cipher_text = cipher_text[:char[1]] + char[0] + cipher_text[char[1]:]  # inserting specail-characters in string

    return "Encrypted text: " + cipher_text

def decode():
    cipher_text = input("Enter encrypted message: ")   # SET THIS EQUAL TO CIPHER-TEXT TEXTBOX INPUT
    key = input("Enter Key: ")                          # SET THIS EQUAL TO KEY TEXTBOX INPUT
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
    return "Decrypted text: " + decrypted_text


def main():
    generate_grid()
    run = True
    while run:
        desicion = input("Do you want to encode or decode? ")
        if desicion == "e":
            print(encode())
        if desicion == "d":
            print(decode())

main()