################################################# Importando librerías necesarias########################################################
import pygame
import math
import random


pygame.init()

width, height = 980,800

win = pygame.display.set_mode((width,height))
pygame.display.set_caption('Juego del Ahorcado')


class juego:
    def __init__(self):
        self.hangman_status = 0
        self.words =  [('Recall','Métrica tp/(tp+fn)'),('Python','Lenguaje POO'),('Pandas','Python y tablas de datos'),('Datos','Pueden ser numéricos o categóricos')] 
        self.guessed = []
        self.word , self.pistas = random.choice(self.words)
        self.word = self.word.upper()

    def fronts(self):
        # fronts
        letter_front = pygame.font.SysFont('comicsans',40)
        word_front = pygame.font.SysFont('comicsans',60)
        title_front = pygame.font.SysFont('comicsans',45)
        return letter_front,word_front,title_front

    def letterLocation(self):
        radius = 25
        gap = 10
        letters = []
        startx = round((width-(radius*2+gap)*13)/2)
        starty = 650
        a = 65  
        for i in range(26):
            x = startx + gap +((radius*2+gap)*(i%13))
            y = starty +((i//13)*(gap+radius*2))
            letters.append([x,y,chr(a+i),True])
        return letters

    def loadimages(self):
        images = []
        for i in range(1,8):
            image = pygame.image.load(f'images/{i}.png')
            images.append(image)
        return images
  
    def messageState(self,mensaje):
        pygame.time.delay(1000)
        win.fill((210, 180, 140))
        _,word_front,_ = self.fronts()
        text = word_front.render(mensaje,1,(0,0,0))
        win.blit(text,(width/2-text.get_width()/2,height/2-text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(3000)

    
    def drawing(self):
        letter_front,word_front,title_front= self.fronts()
        images = self.loadimages()
        letters = self.letterLocation()
        win.fill((210, 180, 140))
    
        ########## Creando la pista ################
        text = title_front.render(f'Pista:{self.pistas}',1,(0, 0, 0))
        win.blit(text,(31,11))
    
        # Creando cada _ para adivinar la letra
        display_word = ''
        for letter in self.word:
            if letter in self.guessed:
                display_word+= letter+ ' '
            else:
                display_word+='_ '
        text = word_front.render(display_word,1,(0,0,0))
        win.blit(text,(425,417))
    
        # Creando los botones de cada letra
        for letter in letters:
            x, y,ltr,visible = letter
            if visible:
                pygame.draw.circle(win, (255, 255, 0),(x,y),25,3)
                text = letter_front.render(ltr,1,(0,0,0))
                win.blit(text,(x-text.get_width()/2,y-text.get_height()/2))
    
        win.blit(images[self.hangman_status],(40,54)) 
        pygame.display.update()
    
    def juegar(self):
        clock = pygame.time.Clock()
        run = True 
        letters = self.letterLocation()
        while run:
            clock.tick(60)
            self.drawing()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x,m_y = pygame.mouse.get_pos()
                    #print(m_x,m_y)
                    for letter in letters:
                        x,y,ltr,visible = letter
                        if visible:
                            dis = math.sqrt((x-m_x)**2+(y-m_y)**2)
                            if dis < 25:
                                #print(ltr)
                                #letter[3] = False
                                self.guessed.append(ltr)
                                if ltr not in self.word:
                                    self.hangman_status +=1
            won = True
            for letter in self.word:
                if letter not in self.guessed:
                    won=False
                    break 
            if won:
                self.messageState('¡Ganaste! :)')  
                self.hangman_status = 0 
                self.guessed = []
                self.word , self.pistas = random.choice(self.words)
                self.word = self.word.upper()       
            if self.hangman_status == 6:
                self.messageState('¡Perdiste! :(')
                self.hangman_status = 0 
                self.guessed = []
                self.word , self.pistas = random.choice(self.words)
                self.word = self.word.upper()


juegoHorcado = juego()

juegoHorcado.juegar()
                