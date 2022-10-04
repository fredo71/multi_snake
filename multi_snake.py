from random import randint
from pygame.locals import *
import threading
import pygame
import sys
import os


#utile pour le passage en .exe
def resource_path0(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)



##var/lists global
size_screen = (1000, 1000)
hold_clic = False
fps = 30
plat_size = (30,30) #spawn des snkaes 7, 14, 21, 28
taille_case = 30 #pixels


plateau = {}
for y in range(plat_size[1]) :
    for x in range(plat_size[0]) :
        plateau[(x,y)] = "vide" #"nour" = nouriture, "p1r" = player 1 rouge, "p2b" = player 2 bleu.... 

nb_player = 1
snake = []
for k in range(nb_player) :
    snake.append({"taille" : 7, "position" : [(20-p, 7) for p in range(7)], "color" : "red", "direction" : "right"})
    
for k in range(len(snake)) :
    for p in range(len(snake[k]["position"])) :
        plateau[snake[k]["position"][p]] = "p1r"

print(plateau)

#######def var boolean boucles in game
main_loop = True #boucle de la fenêtre de jeu
bataille_loop = True #boucle du menu
watch_end_loop = False









####init pygame
pygame.init()
pygame.display.set_caption("multi snake")

#Ouverture de la fenêtre Pygame
window = pygame.display.set_mode(size_screen)
clock = pygame.time.Clock()


#fonts
font1 = pygame.font.SysFont("comicsansms", int(size_screen[0]/55))
font2 = pygame.font.SysFont("comicsansms", int(size_screen[0]/35))
font3 = pygame.font.SysFont("comicsansms", int(size_screen[0]/18))







snake_corps_p1 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/im_corps_snake_player1.png")).convert(), (30,30))










#####fonction auxilière

def conv_sizex(x):
    return int(size_screen[0]*x/1000)
def conv_sizey(y):
    return int(size_screen[1]*y/1000)






    






#threads
def anti_hold_clic():
    global hold_clic
    while main_loop :
        if pygame.mouse.get_pressed()[0] :
            hold_clic = True
            clock.tick(5)
            hold_clic = False
    sys.exit()
#def threads
thread_anti_hold_clic = threading.Thread(target=anti_hold_clic)
thread_anti_hold_clic.start()




def deplacement(snakee) :
    pass













#Boucle infinie
while main_loop:
    
    

    while bataille_loop : #boucle du menu

		#Limitation de vitesse de la boucle
        clock.tick(fps) # 30 fps

        #events clavier
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si un de ces événements est de type QUIT
                main_loop = False
                bataille_loop = False
            elif  event.type == KEYUP and event.key ==  K_d and plateau[(snake[0]["position"][0][0]-1, snake[0]["position"][0][1])] == "vide": #ajouter les limites
                snake[0]["direction"] = "left"
            elif  event.type == KEYUP and event.key ==  K_q and plateau[(snake[0]["position"][0][0]+1, snake[0]["position"][0][1])] == "vide":
                snake[0]["direction"] = "right"
            elif  event.type == KEYUP and event.key ==  K_z and plateau[(snake[0]["position"][0][0], snake[0]["position"][0][1]-1)] == "vide":
                snake[0]["direction"] = "up"
            elif  event.type == KEYUP and event.key ==  K_s and plateau[(snake[0]["position"][0][0]-1, snake[0]["position"][0][1]+1)] == "vide":
                snake[0]["direction"] = "down"

        for k in range(len(snake)) :
            deplacement(snake[k])
    
        #affichage des serpents 
        for k in range(len(snake)) :
            for p in range(len(snake[k]["position"])) :
                window.blit(snake_corps_p1, (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
        
        pygame.display.flip()
    


    while watch_end_loop :


		#Limitation de vitesse de la boucle
        clock.tick(fps) # 30 fps

        #events clavier
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si un de ces événements est de type QUIT
                main_loop = False
                watch_end_loop = False
        
        pygame.display.flip()


""" touche affilié à quelle player :
zqsd = player 1
flèche = player 2



"""
        