from random import randint, choice
from pygame.locals import *
import threading
import pygame
import sys
import os
import pyautogui



#utile pour le passage en .exe
def resource_path0(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def conv_sizex(x):
    return int(size_screen[0]*x/(0.83333*taille_screeny))
def conv_sizey(y):
    return int(size_screen[1]*y/(0.83333*taille_screeny))
taille_screenx, taille_screeny = pyautogui.size()

##var/lists global
size_screen = (0.83333*taille_screeny, 0.83333*taille_screeny)
hold_clic = False
fps = 3
plat_size = (30,30) #spawn des snake 7, 14, 21, 28
taille_case = 30 #pixels
nourriture_coord = None


plateau = {}
for y in range(plat_size[1]) :
    for x in range(plat_size[0]) :
        plateau[(x,y)] = "vide" #"nourriture" = nouriture, "p0" = player 1 rouge, "p1" = player 2 bleu....

nb_player = 2
snake = []
for k in range(nb_player) :
    snake.append({"position" : [(20-p, 7*(k+1)) for p in range(7)], "direction" : "right", "mort" : False})
for k in range(len(snake)) :
    for p in range(len(snake[k]["position"])) :
        plateau[snake[k]["position"][p]] = "p"+str(k)


#######def var boolean boucles in game
main_loop = True #boucle de la fenêtre de jeu
menu_loop = True #boucle du menu du jeu
menu_local_game = False #boucle affichant le menu du mode de jeu local (avec choix du nombre de joueur)
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






snake_corps_p1 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p1_corps_snake.png")).convert_alpha(), (conv_sizex(30),conv_sizey(30)))
snake_corps_p1_mort = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p1_corps_snake_mort.png")).convert_alpha(), (conv_sizex(30),conv_sizex(30)))
snake_corps_p2 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p2_corps_snake.png")).convert_alpha(), (conv_sizex(30),conv_sizex(30)))
snake_corps_p2_mort = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p2_corps_snake_mort.png")).convert_alpha(), (conv_sizex(30),conv_sizex(30)))


im_nourriture = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/autre/food.png")).convert_alpha(), (conv_sizex(30),conv_sizex(30)))

bg_in_game = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/background/bg_in_game.png")).convert(), size_screen)










#####fonction auxilière






def deplacement(ind_snake) :
    global snake
    #test si serpent va mourir
    try :
        depx, depy = 0,0
        if snake[ind_snake]["direction"] == "right" :
            depx = 1
        elif snake[ind_snake]["direction"] == "left" :
            depx = -1
        elif snake[ind_snake]["direction"] == "up" :
            depy = -1
        elif snake[ind_snake]["direction"] == "down" :
            depy = 1
        if plateau[(snake[ind_snake]["position"][0][0]+depx, snake[ind_snake]["position"][0][1]+depy)] not in ["vide", "nourriture"] : #si le serpent va mourir
            return False
        elif plateau[(snake[ind_snake]["position"][0][0]+depx, snake[ind_snake]["position"][0][1]+depy)] == "nourriture" : #si le serpent va manger
            snake[ind_snake]["position"].insert(0, (snake[ind_snake]["position"][0][0]+depx, snake[ind_snake]["position"][0][1]+depy))
            plateau[snake[ind_snake]["position"][0]] = "p"+str(ind_snake)
            add_nourriture()
        else : #si le serpent se déplace simplement
            tamp = snake[ind_snake]["position"][0]
            tamp2 = snake[ind_snake]["position"][len(snake[ind_snake]["position"])-1]
            snake[ind_snake]["position"][0] = (snake[ind_snake]["position"][0][0]+depx, snake[ind_snake]["position"][0][1]+depy)
            for k in range(1,len(snake[ind_snake]["position"])) :
                snake[ind_snake]["position"][k], tamp = tamp, snake[ind_snake]["position"][k]

            for p in range(len(snake[ind_snake]["position"])) :
                plateau[snake[ind_snake]["position"][p]] = "p"+str(ind_snake)
            plateau[tamp2] = "vide"
    except :
        return False
    return True



def add_nourriture():
    global plateau, nourriture_coord
    L_tamp = []
    for x in range(plat_size[0]) :
        for y in range(plat_size[1]) :
            if plateau[(x,y)] == "vide" :
                L_tamp.append((x, y))
    if len(L_tamp) == 0 :
        print("jeu fini ou c'est cassé")
    else :
        tamp = choice(L_tamp)
        plateau[tamp] = "nourriture"
        nourriture_coord = tamp

def retourne (snakee):
    for k in range (len(snakee)):
        new_snakee= []
        new_snakee.append(snakee[len(snakee)-k])


def cherche_dirrection (snakee) :
    cube1 =snakee[0]
    cube2 =snakee[1]
    cube1_x =snakee[0][0]
    cube2_x =snakee[1][0]
    cube1_y =snakee[0][1]
    cube2_y =snakee[1][1]

    if cube1_x-cube2_x <0:
        direction = "left"
    elif cube1_x-cube2_x >0:
        direction = "right"
    elif cube1_y-cube2_y <0:
        direction = "up"
    else:
        direction = "down"
    return direction

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


    if bataille_loop :
        add_nourriture()
    while bataille_loop : #boucle du menu      ########\\\\\\\\\\\\\rajouter de la nourriture si elle est mangée

		#Limitation de vitesse de la boucle
        clock.tick(fps) # 30 fps

        #events clavier
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si un de ces événements est de type QUIT
                main_loop = False
                bataille_loop = False
            if nb_player >= 1 and snake[0]["mort"] == False :
                if  event.type == KEYUP and event.key ==  K_q and plateau[(snake[0]["position"][0][0]-1, snake[0]["position"][0][1])] == "vide": #ajouter les limites
                    snake[0]["direction"] = "left"
                elif  event.type == KEYUP and event.key ==  K_d and plateau[(snake[0]["position"][0][0]+1, snake[0]["position"][0][1])] == "vide":
                    snake[0]["direction"] = "right"
                elif  event.type == KEYUP and event.key ==  K_z and plateau[(snake[0]["position"][0][0], snake[0]["position"][0][1]-1)] == "vide":
                    snake[0]["direction"] = "up"
                elif  event.type == KEYUP and event.key ==  K_s and plateau[(snake[0]["position"][0][0], snake[0]["position"][0][1]+1)] == "vide":
                    snake[0]["direction"] = "down"

#joueur deux
            if nb_player >= 2 and snake[1]["mort"] == False :
                if  event.type == KEYUP and event.key ==  K_k and plateau[(snake[1]["position"][0][0]-1, snake[1]["position"][0][1])] == "vide": #ajouter les limites
                    snake[1]["direction"] = "left"
                elif  event.type == KEYUP and event.key ==  K_m and plateau[(snake[1]["position"][0][0]+1, snake[1]["position"][0][1])] == "vide":
                    snake[1]["direction"] = "right"
                elif  event.type == KEYUP and event.key ==  K_o and plateau[(snake[1]["position"][0][0], snake[1]["position"][0][1]-1)] == "vide":
                    snake[1]["direction"] = "up"
                elif  event.type == KEYUP and event.key ==  K_l and plateau[(snake[1]["position"][0][0], snake[1]["position"][0][1]+1)] == "vide":
                    snake[1]["direction"] = "down"









        for k in range(len(snake)) :
            if snake[k]["mort"] == False :
                tamp = deplacement(k)
            if tamp == False :
                snake[k]["mort"] = True
                for c in snake[k]["position"] :
                    plateau[c] = "snake_dead"

        window.blit(bg_in_game, (0,0))


        #affichage des serpents
        for k in range(len(snake)) :
            for p in range(len(snake[k]["position"])) :
                if snake[k]["mort"] :
                    if k == 0 :
                        window.blit(snake_corps_p1_mort, (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                    elif k == 1 :
                        window.blit(snake_corps_p2_mort, (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                else :
                    if k == 0 :
                        window.blit(snake_corps_p1, (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                    elif k == 1 :
                        window.blit(snake_corps_p2, (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
        #affichage nourriture
        window.blit(im_nourriture, (nourriture_coord[0]*taille_case, nourriture_coord[1]*taille_case, nourriture_coord[0]*taille_case+taille_case, nourriture_coord[1]*taille_case+taille_case))

        pygame.display.flip()



    while watch_end_loop :


		#Limitation de vitesse de la boucle
        clock.tick(fps) # 30 fps
        X, Y = pygame.mouse.get_pos()
        if conv_sizex(780) < X < conv_sizex(1143) and  conv_sizey(900) < Y < conv_sizey(1018) : #clic sur quitter
            survole_quitter = True
            if pygame.mouse.get_pressed()[0] and hold_clic == False : #clic avec le clic gauche
                pass

        #events clavier
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si un de ces événements est de type QUIT
                main_loop = False
                watch_end_loop = False

        pygame.display.flip()


""" touche affilié à quelle player :
zqsd = player 1
sourie : {mouse_up, clic gauche, mouse_doawn, clic droit} = player 2
flèche directionnel = player 3
jn,; ou ijkl = player 4
"""
exit()