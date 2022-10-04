from random import choice, randint
from pygame.locals import *
import threading
import pygame






##var/lists global
size_screen = (1200, 1000)
hold_clic = False
fps = 1
plat_size = (10,10)


plateau = {}
for y in range(plat_size[1]) :
    for x in range(plat_size[0]) :
        plateau[(x,y)] = "vide"


print(plateau)



#######def var boolean boucles in game
main_loop = True #boucle de la fenêtre de jeu
bataille_loop = True #boucle du menu
watch_end_loop = False








exit()

####init pygame
pygame.init()
pygame.display.set_caption("brain test")

#Ouverture de la fenêtre Pygame
window = pygame.display.set_mode(size_screen)
clock = pygame.time.Clock()


#fonts
font1 = pygame.font.SysFont("comicsansms", int(size_screen[0]/55))
font2 = pygame.font.SysFont("comicsansms", int(size_screen[0]/35))
font3 = pygame.font.SysFont("comicsansms", int(size_screen[0]/18))














#####fonction auxilière

def conv_sizex(x):
    return int(size_screen[0]*x/1920)
def conv_sizey(y):
    return int(size_screen[1]*y/1080)






    






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