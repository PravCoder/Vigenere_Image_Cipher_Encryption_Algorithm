import pygame
import random
import ast
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CIPHER_IMG = pygame.image.load(os.path.join("cipher_images", "encrypted.png"))
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
            s1 = Square(self.color_key[char], (50*i+5,100)) # y-coor=100
            rects.append(s1)

        for s in rects: # y coordinate=
            pygame.draw.rect(WIN, s.color, (s.pos[0], s.pos[1], 20, 20))
        pygame.display.update()

    def generate_color_key(self):
        unique = ""
        for char in self.cipher_text:
                r = random.randint(0,256)
                g = random.randint(0,256)
                b = random.randint(0,256)
                if char in self.color_key.keys():
                    self.color_key[char+"2"] = (r,g,b)
                else:
                    self.color_key[char] = (r,g,b)
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

    def vigenere_decryption(self, key, ck):
        self.clear()
        self.key = key
        self.color_key = ast.literal_eval(ck)
        letters = "abcdefghijklmnopqrstuvwxyz"
        letter_indx = dict(zip(letters, range(len(letters)))) 
        indx_letter = dict(zip(range(len(letters)), letters))
        self.create_squares()

        for i, color in enumerate(self.color_key.values()):
            if len(list(self.color_key.keys())[i]) > 1:
                self.cipher_text += list(self.color_key.keys())[i][0]
            else:
                self.cipher_text += list(self.color_key.keys())[i]

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


def import_cipher_img(file_name):
    CIPHER_IMG = pygame.image.load(os.path.join("cipher_images", file_name))
    #CIPHER_IMG_SCALE = pygame.transform.scale(CIPHER_IMG_IMPORT, (SCREEN_WIDTH, SCREEN_HEIGHT))
    #CIPHER_IMG = pygame.transform.rotate(CIPHER_IMG_SCALE, 0)
    print(CIPHER_IMG)


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
            print(e1.vigenere_decryption(key,ck))
            desicion = ""
            WIN.blit(CIPHER_IMG, (0,0))
            pygame.display.update()
            #return

        #pygame.image.save(WIN, "encrypted.png")

desicion = input("Do you want to encode or decode? ")
if desicion == "e":
    text = input("Enter text: ")
    key = input("Enter key: ")
    main(desicion,text,None,key,None)
if desicion == "d":
    key = input("Enter key: ")
    ck = input("Enter color-key: ")
    main(desicion,None,None,key,ck)
    #import_cipher_img("encrypted.png")
    print(CIPHER_IMG)
    WIN.blit(CIPHER_IMG, (0,0))
    pygame.display.update()
    #WIN.get_at((x, y))


# Plain Text: boy bye
# Key: hello
# Color Key: {'i': (176, 215, 155), 's': (220, 66, 103), 'j': (123, 141, 65), ' ': (178, 5, 201), 'm': (228, 2, 176), 'm2': (201, 158, 118), 'l': (184, 115, 237)}