from random import choice,randint
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

taille_plat = 30


def conv_sizex(x):
    return int(size_screen[0]*x/(here_taille_screeny))
def conv_sizey(y):
    return int(size_screen[1]*y/(here_taille_screeny))
taille_screenx, taille_screeny = pyautogui.size()
here_taille_screeny = (int((0.83333*taille_screeny)/taille_plat)+1)*taille_plat

##var/lists global
size_screen = (here_taille_screeny, here_taille_screeny)
hold_clic = False
fps = 100
taille_case = int((0.83333*taille_screeny)/taille_plat)+1 #pixels
plat_size = (taille_plat,taille_plat) #spawn des snake 7, 14, 21, 28
nb_case_a_mourir = 2
case_mur = []
custom_plateau = True
taille_depart = 7
bloc_bonnus = []
comande = [[q,d,z,s],[]]

vitesse_snake1 = 35
vitesse_snake2 = 35
inc_vitess_snake1 = 0
inc_vitess_snake2 = 0


plateau = {}
for y in range(plat_size[1]) :
    for x in range(plat_size[0]) :
        plateau[(x,y)] = "vide" #"nourriture" = nouriture, "p0" = player 1 rouge, "p1" = player 2 bleu....
nb_player = 2
snake = []
for k in range(nb_player) :
    snake.append({"position" : [(int(taille_plat/1.5)-p, int(taille_plat/4.29)*(k+1)) for p in range(taille_depart)], "direction" : "right", "mort" : False})
for k in range(len(snake)) :
    for p in range(len(snake[k]["position"])) :
        plateau[snake[k]["position"][p]] = "p"+str(k)

#######def var boolean boucles in game
main_loop = True #boucle de la fenêtre de jeu
bataille_loop = True #boucle du menu
remake_game_loop = False









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





icon = pygame.image.load(resource_path0("./assets/images/icon.png"))
pygame.display.set_icon(icon)
snake_tete_p1 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p1_tete_snake.png")).convert_alpha(), (conv_sizex(taille_case),conv_sizey(taille_case)))
L_snake_tete_p1 = [snake_tete_p1, pygame.transform.rotate(snake_tete_p1, 90), pygame.transform.rotate(snake_tete_p1, 180), pygame.transform.rotate(snake_tete_p1, 270)] #droite, haut, gauche, bas
snake_queue_p1 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p1_queue_snake.png")).convert_alpha(), (conv_sizex(taille_case),conv_sizey(taille_case)))
L_snake_queue_p1 = [snake_queue_p1, pygame.transform.rotate(snake_queue_p1, 90), pygame.transform.rotate(snake_queue_p1, 180), pygame.transform.rotate(snake_queue_p1, 270)] #droite, haut, gauche, bas
snake_corps_p1 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p1_corps_snake.png")).convert_alpha(), (conv_sizex(taille_case),conv_sizey(taille_case)))
L_snake_corps_p1 = [snake_corps_p1, pygame.transform.rotate(snake_corps_p1, 90)] #droite, haut, gauche, bas
snake_corner_p1 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p1_corner_snake.png")).convert_alpha(), (conv_sizex(taille_case),conv_sizey(taille_case)))
L_snake_corner_p1 = [snake_corner_p1, pygame.transform.rotate(snake_corner_p1, 90), pygame.transform.rotate(snake_corner_p1, 180), pygame.transform.rotate(snake_corner_p1, 270)] #droite, haut, gauche, bas


snake_tete_p2 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p2_tete_snake.png")).convert_alpha(), (conv_sizex(taille_case),conv_sizey(taille_case)))
L_snake_tete_p2 = [snake_tete_p2, pygame.transform.rotate(snake_tete_p2, 90), pygame.transform.rotate(snake_tete_p2, 180), pygame.transform.rotate(snake_tete_p2, 270)] #droite, haut, gauche, bas
snake_queue_p2 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p2_queue_snake.png")).convert_alpha(), (conv_sizex(taille_case),conv_sizey(taille_case)))
L_snake_queue_p2 = [snake_queue_p2, pygame.transform.rotate(snake_queue_p2, 90), pygame.transform.rotate(snake_queue_p2, 180), pygame.transform.rotate(snake_queue_p2, 270)] #droite, haut, gauche, bas
snake_corps_p2 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p2_corps_snake.png")).convert_alpha(), (conv_sizex(taille_case),conv_sizey(taille_case)))
L_snake_corps_p2 = [snake_corps_p2, pygame.transform.rotate(snake_corps_p2, 90)] #droite, haut, gauche, bas
snake_corner_p2 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/p2_corner_snake.png")).convert_alpha(), (conv_sizex(taille_case),conv_sizey(taille_case)))
L_snake_corner_p2 = [snake_corner_p2, pygame.transform.rotate(snake_corner_p2, 90), pygame.transform.rotate(snake_corner_p2, 180), pygame.transform.rotate(snake_corner_p2, 270)] #droite, haut, gauche, bas





mur_im = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/snake_image/mur.png")).convert_alpha(), (conv_sizex(taille_case),conv_sizex(taille_case)))

im_portal1 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/autre/portal1.png")).convert_alpha(), (conv_sizex(taille_case),conv_sizex(taille_case)))
im_portal2 = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/autre/portal2.png")).convert_alpha(), (conv_sizex(taille_case),conv_sizex(taille_case)))
L_portal = []
time_portal_apaire = 1000
inc_time_portal_apaire = 0

im_nourriture_listes = ["humberger", "pizza", "gigot", "riz"]
im_nourriture_bdd = []
for foods in im_nourriture_listes :
    im_nourriture_bdd.append(pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/autre/foods/"+foods+".png")).convert_alpha(), (conv_sizex(taille_case),conv_sizex(taille_case))))

nourriture = []

bg_in_game = pygame.transform.scale(pygame.image.load(resource_path0("./assets/images/background/bg_in_game.png")).convert(), size_screen)










#####fonction auxilière






def deplacement(ind_snake) :
    global snake, L_portal
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
        if plateau[(snake[ind_snake]["position"][0][0]+depx, snake[ind_snake]["position"][0][1]+depy)] not in ["vide", "nourriture", "portal"] : #si le serpent va mourir
            return False
        elif plateau[(snake[ind_snake]["position"][0][0]+depx, snake[ind_snake]["position"][0][1]+depy)] == "nourriture" : #si le serpent va manger
            snake[ind_snake]["position"].insert(0, (snake[ind_snake]["position"][0][0]+depx, snake[ind_snake]["position"][0][1]+depy))
            plateau[snake[ind_snake]["position"][0]] = "p"+str(ind_snake)
            nourriture.pop([nourriture[k][1] for k in range(len(nourriture))].index((snake[ind_snake]["position"][0][0], snake[ind_snake]["position"][0][1])))

            add_nourriture(True)
        elif plateau[(snake[ind_snake]["position"][0][0]+depx, snake[ind_snake]["position"][0][1]+depy)] == "portal" :
            for k in range(2) :
                tamp = snake[ind_snake]["position"][0]
                tamp2 = snake[ind_snake]["position"][len(snake[ind_snake]["position"])-1]
                if k == 0 :
                    snake[ind_snake]["position"][0] = (snake[ind_snake]["position"][0][0]+depx, snake[ind_snake]["position"][0][1]+depy)
                else :
                    if [L_portal[k][1] for k in range(2)].index((snake[ind_snake]["position"][0][0], snake[ind_snake]["position"][0][1])) == 0 :
                        var_here = 1
                    else :
                        var_here = 0
                    snake[ind_snake]["position"][0] = L_portal[var_here][1]
                for k in range(1,len(snake[ind_snake]["position"])) :
                    snake[ind_snake]["position"][k], tamp = tamp, snake[ind_snake]["position"][k]
                plateau[tamp2] = "vide"

            for p in range(len(snake[ind_snake]["position"])) :
                plateau[snake[ind_snake]["position"][p]] = "p"+str(ind_snake)
            L_portal = []

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



def add_nourriture(add_vitesse):
    global plateau, vitesse_snake1, vitesse_snake2, nourriture, inc_vitess_snake1, inc_vitess_snake2
    if add_vitesse :
        vitesse_snake1-=1
        vitesse_snake2-=1
        inc_vitess_snake1 = 0
        inc_vitess_snake2 = 0
    L_tamp = []
    for x in range(plat_size[0]) :
        for y in range(plat_size[1]) :
            if plateau[(x,y)] == "vide" :
                L_tamp.append((x, y))
    if len(L_tamp) == 0 :
        print("jeu fini ou c'est cassé")
    else :
        if len(nourriture)<3:
            tamp = choice(L_tamp)
            plateau[tamp] = "nourriture"
            nourriture.append([choice(im_nourriture_bdd), tamp])
    return add_nourriture
def retourne (snakee):
    snakee.reverse()
    return snakee


def cherche_dirrection (snakee) :
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
# def anti_hold_clic():
#     global hold_clic
#     while main_loop :
#         if pygame.mouse.get_pressed()[0] :
#             hold_clic = True
#             clock.tick(5)
#             hold_clic = False
#     sys.exit()
# #def threads
# thread_anti_hold_clic = threading.Thread(target=anti_hold_clic)
# thread_anti_hold_clic.start()


def create_custom_plateau(plateau):
    shape_list = [[(0,0),(-1,0),(1,0)],[(0,0),(-1,0),(0,1)],[(0,0),(0,-1),(0,1)],[(0,0),(0,-1),(1,0)]]
    shape_num = [2,2,1,1]
    for m in range (len(shape_list)):
        shape=shape_list[m]
        for k in range (shape_num[m]):
            x=randint(0,plat_size[0])
            y=randint(0,plat_size[0])
            st = add_shape(shape,(x,y),plateau)
            if not st :
                k=k-1





def add_shape(shape,coord,plateau):
    global snake
    for k in range (0,len(shape)):
        pt=(coord[0]+shape[k][0],coord[1]+shape[k][1])
        for i in range (0,len(snake)):
            if pt in snake[i]["position"]:
                return False



    for k in range (0,len(shape)):
        pt=(coord[0]+shape[k][0],coord[1]+shape[k][1])
        plateau[pt]='mur'
        case_mur.append(pt)

    return True


def ajout_portal() :
    global inc_time_portal_apaire, L_portal
    if len(L_portal) == 0 :
        remake = False
    else :
        remake = True
    if remake :
        plateau[L_portal[0][1]] = "vide"
        plateau[L_portal[1][1]] = "vide"
        L_portal = []
    inc_time_portal_apaire = 0
    for k in range(2) :
        L_tamp = []
        for x in range(plat_size[0]) :
            for y in range(plat_size[1]) :
                if plateau[(x,y)] == "vide" :
                    L_tamp.append((x, y))
        if len(L_tamp) == 0 :
            print("jeu fini ou c'est cassé")
        else :
            tamp = choice(L_tamp)
            plateau[tamp] = "portal"
            if k == 0 :
                im_portal = im_portal1
            else :
                im_portal = im_portal2
            L_portal.append([im_portal, tamp])


def bonus_food(coordone):
    global plateau ,nourriture ,taille_plat
    for k in range(10):
        tamp  = (coordone[0] + randint(0,10), coordone[1] +randint(0,10))
        if 0<tamp[0]<taille_plat and 0<tamp[1]<taille_plat :
            if plateau[tamp] == "vide" :
                plateau[tamp] = "nourriture"
                nourriture.append([choice(im_nourriture_bdd), tamp])







#Boucle infinie
while main_loop:
    if remake_game_loop :
        case_mur = []
        nourriture = []
        L_portal = []
        plateau = {}
        inc_time_portal_apaire = 0
        inc_vitess_snake1 = 0
        inc_vitess_snake2 = 0
        vitesse_snake1 = 35
        vitesse_snake2 = 35
        for y in range(plat_size[1]) :
            for x in range(plat_size[0]) :
                plateau[(x,y)] = "vide" #"nourriture" = nouriture, "p0" = player 1 rouge, "p1" = player 2 bleu....
        snake = []
        for k in range(nb_player) :
            snake.append({"position" : [(int(taille_plat/1.5)-p, int(taille_plat/4.29)*(k+1)) for p in range(taille_depart)], "direction" : "right", "mort" : False})
        for k in range(len(snake)) :
            for p in range(len(snake[k]["position"])) :
                plateau[snake[k]["position"][p]] = "p"+str(k)

    while remake_game_loop :
        clock.tick(fps) # 30 fps

        #events clavier
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si un de ces événements est de type QUIT
                main_loop = False
                bataille_loop = False
            if  event.type == KEYUP :
                bataille_loop = True
                remake_game_loop = False



        window.blit(bg_in_game, (0,0))


        #affichage des serpents
        for k in range(len(snake)) :
            for p in range(len(snake[k]["position"])) :
                if snake[k]["mort"] :
                    if k == 0 :
                        window.blit(mur_im, (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                    elif k == 1 :
                        window.blit(mur_im, (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                else :
                    if k == 0 :
                        if p == 0 :
                            cube1_x =snake[k]["position"][0][0]
                            cube2_x =snake[k]["position"][1][0]
                            cube1_y =snake[k]["position"][0][1]
                            cube2_y =snake[k]["position"][1][1]

                            if cube1_x-cube2_x <0:
                                direct = "left"
                            elif cube1_x-cube2_x >0:
                                direct = "right"
                            elif cube1_y-cube2_y <0:
                                direct = "up"
                            else:
                                direct = "down"
                            if direct == "right" :
                                window.blit(L_snake_tete_p1[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "up" :
                                window.blit(L_snake_tete_p1[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "left" :
                                window.blit(L_snake_tete_p1[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "down" :
                                window.blit(L_snake_tete_p1[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                        elif p == len(snake[k]["position"])-1 :
                            cube1_x =snake[k]["position"][-1][0]
                            cube2_x =snake[k]["position"][-2][0]
                            cube1_y =snake[k]["position"][-1][1]
                            cube2_y =snake[k]["position"][-2][1]

                            if cube1_x-cube2_x <0:
                                direct = "left"
                            elif cube1_x-cube2_x >0:
                                direct = "right"
                            elif cube1_y-cube2_y <0:
                                direct = "up"
                            else:
                                direct = "down"
                            if direct == "left" :
                                window.blit(L_snake_queue_p1[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "down" :
                                window.blit(L_snake_queue_p1[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "right" :
                                window.blit(L_snake_queue_p1[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "up" :
                                window.blit(L_snake_queue_p1[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                        else :
                            self_x, self_y = snake[k]["position"][p][0], snake[k]["position"][p][1]
                            avant_x =snake[k]["position"][p-1][0]
                            apres_x =snake[k]["position"][p+1][0]
                            avant_y =snake[k]["position"][p-1][1]
                            apres_y =snake[k]["position"][p+1][1]

                            if self_y == apres_y == avant_y :
                                window.blit(L_snake_corps_p1[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif self_x == apres_x == avant_x :
                                window.blit(L_snake_corps_p1[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y < avant_y and self_x < apres_x) or (self_y < apres_y and self_x < avant_x) :
                                window.blit(L_snake_corner_p1[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y > avant_y and self_x < apres_x) or (self_y > apres_y and self_x < avant_x) :
                                window.blit(L_snake_corner_p1[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y > avant_y and self_x > apres_x) or (self_y > apres_y and self_x > avant_x) :
                                window.blit(L_snake_corner_p1[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y < avant_y and self_x > apres_x) or (self_y < apres_y and self_x > avant_x) :
                                window.blit(L_snake_corner_p1[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))


                    elif k == 1 :
                        if p == 0 :
                            cube1_x =snake[k]["position"][0][0]
                            cube2_x =snake[k]["position"][1][0]
                            cube1_y =snake[k]["position"][0][1]
                            cube2_y =snake[k]["position"][1][1]

                            if cube1_x-cube2_x <0:
                                direct = "left"
                            elif cube1_x-cube2_x >0:
                                direct = "right"
                            elif cube1_y-cube2_y <0:
                                direct = "up"
                            else:
                                direct = "down"
                            if direct == "right" :
                                window.blit(L_snake_tete_p2[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "up" :
                                window.blit(L_snake_tete_p2[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "left" :
                                window.blit(L_snake_tete_p2[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "down" :
                                window.blit(L_snake_tete_p2[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                        elif p == len(snake[k]["position"])-1 :
                            cube1_x =snake[k]["position"][-1][0]
                            cube2_x =snake[k]["position"][-2][0]
                            cube1_y =snake[k]["position"][-1][1]
                            cube2_y =snake[k]["position"][-2][1]

                            if cube1_x-cube2_x <0:
                                direct = "left"
                            elif cube1_x-cube2_x >0:
                                direct = "right"
                            elif cube1_y-cube2_y <0:
                                direct = "up"
                            else:
                                direct = "down"
                            if direct == "left" :
                                window.blit(L_snake_queue_p2[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "down" :
                                window.blit(L_snake_queue_p2[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "right" :
                                window.blit(L_snake_queue_p2[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "up" :
                                window.blit(L_snake_queue_p2[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                        else :
                            self_x, self_y = snake[k]["position"][p][0], snake[k]["position"][p][1]
                            avant_x =snake[k]["position"][p-1][0]
                            apres_x =snake[k]["position"][p+1][0]
                            avant_y =snake[k]["position"][p-1][1]
                            apres_y =snake[k]["position"][p+1][1]

                            if self_y == apres_y == avant_y :
                                window.blit(L_snake_corps_p2[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif self_x == apres_x == avant_x :
                                window.blit(L_snake_corps_p2[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y < avant_y and self_x < apres_x) or (self_y < apres_y and self_x < avant_x) :
                                window.blit(L_snake_corner_p2[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y > avant_y and self_x < apres_x) or (self_y > apres_y and self_x < avant_x) :
                                window.blit(L_snake_corner_p2[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y > avant_y and self_x > apres_x) or (self_y > apres_y and self_x > avant_x) :
                                window.blit(L_snake_corner_p2[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y < avant_y and self_x > apres_x) or (self_y < apres_y and self_x > avant_x) :
                                window.blit(L_snake_corner_p2[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))

        pygame.display.flip()











    if bataille_loop :
        if(custom_plateau):
            create_custom_plateau(plateau)
        add_nourriture(False)(False)(False)
        ajout_portal()
    while bataille_loop : #boucle du menu      ########\\\\\\\\\\\\\rajouter de la nourriture si elle est mangée

		#Limitation de vitesse de la boucle
        clock.tick(fps) # 30 fps

        #events clavier
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == KEYUP and event.key ==  K_a: #temp
                print("yeeepee")
                bonus_food(snake[0]["position"][0])
            if event.type == QUIT or keys[K_LSHIFT] and keys[K_ESCAPE] :     #Si un de ces événements est de type QUIT
                main_loop = False
                bataille_loop = False
            try :
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
                if  event.type == KEYUP and event.key ==  K_v and vitesse_snake1 > 1:
                    vitesse_snake1-=1
                    inc_vitess_snake1 = 0
            except :
                pass








        for k in range(len(snake)) :
            if k == 0 :
                if inc_vitess_snake1 == vitesse_snake1 :
                    p = "pass"
                    inc_vitess_snake1 = 0
                else :
                    inc_vitess_snake1+=1
                    p = "pass_pas"
            elif k == 1 :
                if inc_vitess_snake2 == vitesse_snake2 :
                    p = "pass"
                    inc_vitess_snake2 = 0
                else :
                    inc_vitess_snake2+=1
                    p = "pass_pas"
            else :
                p = "pass_pas"

            if p == "pass" :
                if snake[k]["mort"] == False :
                    tamp = deplacement(k)
                if tamp == False :
                    try :
                        for p in range(nb_case_a_mourir) :
                            plateau[snake[k]["position"][0]] = "mur"
                            case_mur.append(snake[k]["position"][0])
                            snake[k]["position"].pop(0)
                        snake[k]["position"] = retourne(snake[k]["position"])
                        snake[k]["direction"] = cherche_dirrection(snake[k]["position"])
                    except :
                        snake[k]["mort"] = True

        if inc_time_portal_apaire == time_portal_apaire or len(L_portal) == 0:
            ajout_portal()
        else :
            inc_time_portal_apaire+=1

        window.blit(bg_in_game, (0,0))
        for p in range(len(case_mur)) :
            window.blit(mur_im, (case_mur[p][0]*taille_case, case_mur[p][1]*taille_case, case_mur[p][0]*taille_case+taille_case, case_mur[p][1]*taille_case+taille_case))

        if len(L_portal) != 0 :
            for k in range(2) :
                window.blit(L_portal[k][0], (L_portal[k][1][0]*taille_case, L_portal[k][1][1]*taille_case, L_portal[k][1][0]*taille_case+taille_case, L_portal[k][1][1]*taille_case+taille_case))

        #affichage des serpents
        for k in range(len(snake)) :
            for p in range(len(snake[k]["position"])) :
                if snake[k]["mort"] :
                    if k == 0 :
                        window.blit(mur_im, (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                    elif k == 1 :
                        window.blit(mur_im, (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                else :
                    if k == 0 :
                        if p == 0 :
                            cube1_x =snake[k]["position"][0][0]
                            cube2_x =snake[k]["position"][1][0]
                            cube1_y =snake[k]["position"][0][1]
                            cube2_y =snake[k]["position"][1][1]

                            if cube1_x-cube2_x <0:
                                direct = "left"
                            elif cube1_x-cube2_x >0:
                                direct = "right"
                            elif cube1_y-cube2_y <0:
                                direct = "up"
                            else:
                                direct = "down"
                            if direct == "right" :
                                window.blit(L_snake_tete_p1[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "up" :
                                window.blit(L_snake_tete_p1[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "left" :
                                window.blit(L_snake_tete_p1[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "down" :
                                window.blit(L_snake_tete_p1[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                        elif p == len(snake[k]["position"])-1 :
                            cube1_x =snake[k]["position"][-1][0]
                            cube2_x =snake[k]["position"][-2][0]
                            cube1_y =snake[k]["position"][-1][1]
                            cube2_y =snake[k]["position"][-2][1]

                            if cube1_x-cube2_x <0:
                                direct = "left"
                            elif cube1_x-cube2_x >0:
                                direct = "right"
                            elif cube1_y-cube2_y <0:
                                direct = "up"
                            else:
                                direct = "down"
                            if direct == "left" :
                                window.blit(L_snake_queue_p1[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "down" :
                                window.blit(L_snake_queue_p1[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "right" :
                                window.blit(L_snake_queue_p1[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "up" :
                                window.blit(L_snake_queue_p1[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                        else :
                            self_x, self_y = snake[k]["position"][p][0], snake[k]["position"][p][1]
                            avant_x =snake[k]["position"][p-1][0]
                            apres_x =snake[k]["position"][p+1][0]
                            avant_y =snake[k]["position"][p-1][1]
                            apres_y =snake[k]["position"][p+1][1]

                            if self_y == apres_y == avant_y :
                                window.blit(L_snake_corps_p1[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif self_x == apres_x == avant_x :
                                window.blit(L_snake_corps_p1[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y < avant_y and self_x < apres_x) or (self_y < apres_y and self_x < avant_x) :
                                window.blit(L_snake_corner_p1[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y > avant_y and self_x < apres_x) or (self_y > apres_y and self_x < avant_x) :
                                window.blit(L_snake_corner_p1[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y > avant_y and self_x > apres_x) or (self_y > apres_y and self_x > avant_x) :
                                window.blit(L_snake_corner_p1[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y < avant_y and self_x > apres_x) or (self_y < apres_y and self_x > avant_x) :
                                window.blit(L_snake_corner_p1[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))


                    elif k == 1 :
                        if p == 0 :
                            cube1_x =snake[k]["position"][0][0]
                            cube2_x =snake[k]["position"][1][0]
                            cube1_y =snake[k]["position"][0][1]
                            cube2_y =snake[k]["position"][1][1]

                            if cube1_x-cube2_x <0:
                                direct = "left"
                            elif cube1_x-cube2_x >0:
                                direct = "right"
                            elif cube1_y-cube2_y <0:
                                direct = "up"
                            else:
                                direct = "down"
                            if direct == "right" :
                                window.blit(L_snake_tete_p2[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "up" :
                                window.blit(L_snake_tete_p2[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "left" :
                                window.blit(L_snake_tete_p2[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "down" :
                                window.blit(L_snake_tete_p2[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                        elif p == len(snake[k]["position"])-1 :
                            cube1_x =snake[k]["position"][-1][0]
                            cube2_x =snake[k]["position"][-2][0]
                            cube1_y =snake[k]["position"][-1][1]
                            cube2_y =snake[k]["position"][-2][1]

                            if cube1_x-cube2_x <0:
                                direct = "left"
                            elif cube1_x-cube2_x >0:
                                direct = "right"
                            elif cube1_y-cube2_y <0:
                                direct = "up"
                            else:
                                direct = "down"
                            if direct == "left" :
                                window.blit(L_snake_queue_p2[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "down" :
                                window.blit(L_snake_queue_p2[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "right" :
                                window.blit(L_snake_queue_p2[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif direct == "up" :
                                window.blit(L_snake_queue_p2[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                        else :
                            self_x, self_y = snake[k]["position"][p][0], snake[k]["position"][p][1]
                            avant_x =snake[k]["position"][p-1][0]
                            apres_x =snake[k]["position"][p+1][0]
                            avant_y =snake[k]["position"][p-1][1]
                            apres_y =snake[k]["position"][p+1][1]

                            if self_y == apres_y == avant_y :
                                window.blit(L_snake_corps_p2[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif self_x == apres_x == avant_x :
                                window.blit(L_snake_corps_p2[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y < avant_y and self_x < apres_x) or (self_y < apres_y and self_x < avant_x) :
                                window.blit(L_snake_corner_p2[0], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y > avant_y and self_x < apres_x) or (self_y > apres_y and self_x < avant_x) :
                                window.blit(L_snake_corner_p2[1], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y > avant_y and self_x > apres_x) or (self_y > apres_y and self_x > avant_x) :
                                window.blit(L_snake_corner_p2[2], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))
                            elif (self_y < avant_y and self_x > apres_x) or (self_y < apres_y and self_x > avant_x) :
                                window.blit(L_snake_corner_p2[3], (snake[k]["position"][p][0]*taille_case, snake[k]["position"][p][1]*taille_case, snake[k]["position"][p][0]*taille_case+taille_case, snake[k]["position"][p][1]*taille_case+taille_case))

        #affichage nourriture
        for foods in nourriture :
            window.blit(foods[0], (foods[1][0]*taille_case, foods[1][1]*taille_case, foods[1][0]*taille_case+taille_case, foods[1][1]*taille_case+taille_case))

        end_game = True
        for mort in range(nb_player) :
            if snake[mort]["mort"] == False :
                end_game = False
        if end_game :
            remake_game_loop = True
            bataille_loop = False



        pygame.display.flip()






""" touche affilié à quelle player :
zqsd = player 1
sourie : {mouse_up, clic gauche, mouse_doawn, clic droit} = player 2
flèche directionnel = player 3
jn,; ou ijkl = player 4
"""
exit()