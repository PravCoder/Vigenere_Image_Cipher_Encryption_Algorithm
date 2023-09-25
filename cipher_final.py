import pygame
import random
import ast
import os
import numpy as np

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# CHANGE THIS TO THE IMAGE YOU ARE TRYING TO DECRYPT
CIPHER_IMG = pygame.image.load(os.path.join("cipher_images", "e10.png"))  
pygame.display.set_caption("VigenereCipherImageEncoder")
BLACK = (0, 0, 0)
RED = (255, 0, 0)


FPS = 60
grid = []
color_map = []

class Square:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 15, 15) 

class Encoder:
    def __init__(self, text, key):
        self.text = text
        self.key = key
        self.color_key = {}
        self.cipher_text = ""
        self.decrypted_text = ""
        self.decrypted_color_text = ""
        self.text_no_spaces = ""
        self.letters = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
        self.letter_indx = dict(zip(self.letters, range(len(self.letters)))) 
        self.indx_letter = dict(zip(range(len(self.letters)), self.letters))
        self.space_indicies = []  # stores the non-alphabet characters, each element is (char,indx)
        self.character_pairs = []  # stores the mapping of each text adn key character
        self.squares = []
    
    def generate_grid(self):
        for row in range(26):
            grid.append([])
    
        for i, row in enumerate(grid):
            j = i
            while len(row) < 26:
                grid[i].append(self.indx_letter[j])
                j += 1
        return grid

    def create_squares(self):
        for i in range(9):
            color_map.append([])
        rects = []
        for i, char in enumerate(self.cipher_text):
            s1 = Square(self.color_key[char], (50*i,100)) # y-coor=100
            rects.append(s1)

        x = 50
        y = 100
        for i, s in enumerate(rects):

            if (i+1)%10== 0:
                x = 50
                y += 50
                pygame.draw.rect(WIN, s.color, (x, y, 20, 20))
            elif i==0:
                pygame.draw.rect(WIN, s.color, (50, 100, 20, 20))
            else:
                x += 50
                pygame.draw.rect(WIN, s.color, (x, y, 20, 20))

        pygame.display.update()

    def generate_color_key(self):
        unique = ""
        temp_chars = {}  # char:cur-count
        for char in self.cipher_text:
                r = random.randint(0,256)
                g = random.randint(0,256)
                b = random.randint(0,256)
                if char in temp_chars:
                    self.color_key[char+str(temp_chars[char])] = (r,g,b)
                    temp_chars[char] += 1
                else:
                    self.color_key[char] = (r,g,b)
                    temp_chars[char] = 1
        return self.color_key

    def vigenere_encryption(self, text, key):  # equal to input
        self.clear()
        self.text = text
        self.key = key
        letters = "abcdefghijklmnopqrstuvwxyz"
        letter_indx = dict(zip(letters, range(len(letters))))

        for i, char in enumerate(self.text):    
                if char not in self.letters:  # if the character is non-aplphabet
                    self.space_indicies.append((char,i)) # add it to space-indicies
                else:
                    self.text_no_spaces += char  # else its a normal letter add it no-spaces-text

        while len(self.key) < len(self.text):  # for cycle matching make sure length of key is greater than length of text
            self.key += self.key
                                    
        for i, char in enumerate(self.text_no_spaces):
            self.character_pairs.append((char,self.key[i]))  # mapping each character in text to each char in key using corresponding index, (text-char, key-char)
        
        for pair in self.character_pairs:  # pair = (text-char,key-char)
            col = letter_indx[pair[0]]  # col = letter_indx-dict[text-char]
            row = letter_indx[pair[1]]  # row = letter_indx-dict[key-char]
            letter = grid[row][col]     # extracting encoded letter from grid using row/col indicies
            self.cipher_text += letter
        
        for char in self.space_indicies:  # char = (special-character, index)
            self.cipher_text = self.cipher_text[:char[1]] + char[0] + self.cipher_text[char[1]:]  # inserting specail-characters in string

        self.color_key = self.generate_color_key()
        color_key1 = []

        for key, value in self.color_key.items():
            color_key1.append((key,value))

        self.create_squares()
        return "Encrypted text: " + self.cipher_text + "\n" + "Color Key: " + str(self.color_key)
    
    def clear(self):
        self.text_no_spaces = ""
        self.cipher_text = ""
        self.key = ""
        self.text = ""
        self.space_indicies.clear()
        self.character_pairs.clear()

    def get_color_key(self):
        print("GET COLOR KEY: ")
        rgbs = []
        for x in range(0, 251, 50):
            print(WIN.get_at((x, 100)))

    def vigenere_decryption(self, key, ck):
        self.clear()
        self.key = key
        self.color_key = ast.literal_eval(ck)
        letters = "abcdefghijklmnopqrstuvwxyz"
        letter_indx = dict(zip(letters, range(len(letters)))) 
        indx_letter = dict(zip(range(len(letters)), letters))
        self.create_squares()

        """for i, color in enumerate(self.color_key.values()):
            if len(list(self.color_key.keys())[i]) > 1:
                self.cipher_text += list(self.color_key.keys())[i][0]
            else:
                self.cipher_text += list(self.color_key.keys())[i]"""
        self.decrypt_color_squares()

        for i, char in enumerate(self.cipher_text):
            if char not in letters:
                self.space_indicies.append((char, i))
            else:
                self.text_no_spaces += char

        while len(self.key) < len(self.cipher_text):
            self.key += self.key
    
        for i, char in enumerate(self.text_no_spaces):
            self.character_pairs.append((char,self.key[i]))

        for pair in self.character_pairs:
            row = letter_indx[pair[1]]
            for i, letter in enumerate(grid[row]):
                if letter == pair[0]:
                   self.decrypted_letter = indx_letter[i]
                   self.decrypted_text += self.decrypted_letter
    
        for char in self.space_indicies:
            self.decrypted_text = self.decrypted_text[:char[1]] + char[0] + self.decrypted_text[char[1]:]
        return "Decrypted text: " + self.decrypted_text

    def decrypt_color_squares(self):
        """for x in range(0, 501, 50):
            for y in range(0, 501, 50):
                rgb = (WIN.get_at((x, y))[0], WIN.get_at((x, y))[1], WIN.get_at((x, y))[2])
                for i, color in enumerate(self.color_key.values()):
                    if color == rgb and rgb != (0,0,0):
                        print(rgb)
                        self.cipher_text += list(self.color_key.keys())[i][0]"""

        for i, color in enumerate(self.color_key.values()):
            if len(list(self.color_key.keys())[i]) > 1:
                self.cipher_text += list(self.color_key.keys())[i][0]
            else:
                self.cipher_text += list(self.color_key.keys())[i]
        

        
        print("Cipher: " + self.cipher_text)

def import_cipher_img(file_name):
    CIPHER_IMG = pygame.image.load(os.path.join("cipher_images", file_name))


def main(desicion, text, cipher_text, key, color_key):
    WIN.fill((0,0,0))
    clock = pygame.time.Clock()
    run = True
    e1 = Encoder("","")
    e1.generate_grid()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                pass
                    
        if desicion == "e":
            print(e1.vigenere_encryption(text, key))
            desicion = ""
        if desicion == "d":
            desicion = ""
            WIN.blit(CIPHER_IMG, (0,0)) # blit the image before trying to get the RGB-values and decrypting it
            print(e1.vigenere_decryption(key,ck))
            pygame.display.update()
            #return

        #pygame.image.save(WIN, "e10.png")   # Uncomment this to save you encrypted image and change name of file

desicion = input("Do you want to encode or decode? ")
if desicion == "e":
    text = input("Enter text: ")
    key = input("Enter key: ")
    main(desicion,text,None,key,None)
if desicion == "d":
    key = input("Enter key: ")
    ck = input("Enter color-key: ")
    main(desicion,None,None,key,ck)
    print(CIPHER_IMG)
    WIN.blit(CIPHER_IMG, (0,0))
    pygame.display.update()


# TBD: a long encrypted messages to exceeds more than 1 row
# TBD: spaces and special characters?


# Plain Text: boy bye
# Key: hello
# Color Key: {'i': (176, 215, 155), 's': (220, 66, 103), 'j': (123, 141, 65), ' ': (178, 5, 201), 'm': (228, 2, 176), 'm2': (201, 158, 118), 'l': (184, 115, 237)}

# Plain Text: boy bye
# Key: hello
# ColorKey: 

# Plain Text: see ya
# Key: hello
# Color key: {'z': (180, 180, 101), 'i': (170, 122, 255), 'p': (242, 70, 229), ' ': (249, 225, 253), 'j': (220, 74, 99), 'o': (39, 26, 128)}


# {'z': (2, 47, 81), 'i': (85, 87, 202), 'p': (88, 146, 228), ' ': (203, 177, 230), 'j': (214, 105, 58), 'o': (198, 235, 114)}

"""
Enter text: yo this is my poem its fire i aint no lier
Enter key: hello
Encrypted text: fs eswz md xm wspx waw qtfl m ltba rz wwlv
Color Key: {'f': (172, 228, 124), 's': (63, 21, 70), ' ': (188, 250, 249), 'e': (139, 149, 224), 's1': (138, 119, 85), 'w': (182, 59, 217), 'z': (73, 49, 15), ' 1': (159, 112, 245), 'm': (99, 172, 224), 'd': (9, 131, 193), ' 2': (40, 181, 90), 'x': (226, 173, 207), 'm1': (149, 105, 202), ' 3': (99, 17, 186), 'w1': (26, 166, 54), 's2': (55, 170, 6), 'p': (61, 147, 87), 'x1': (65, 237, 163), ' 4': (118, 110, 229), 'w2': (236, 7, 220), 'a': (143, 174, 24), 'w3': (240, 49, 16), ' 5': (228, 168, 234), 'q': (2, 145, 126), 't': (4, 225, 66), 'f1': (141, 145, 116), 'l': (61, 119, 80), ' 6': (148, 151, 243), 'm2': (240, 177, 39), ' 7': (4, 152, 132), 'l1': (254, 217, 172), 't1': (113, 238, 256), 'b': (106, 50, 200), 'a1': (92, 68, 180), ' 8': (84, 80, 36), 'r': (55, 232, 47), 'z1': (254, 120, 103), ' 9': (149, 98, 206), 'w4': (147, 113, 156), 'w5': (80, 253, 59), 'l2': (109, 104, 154), 'v': (127, 147, 249)}
File: e10.png
"""