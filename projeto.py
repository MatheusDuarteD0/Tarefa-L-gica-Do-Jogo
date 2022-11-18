import pygame
# from pygame import *
from random import randint, choice
from pygame import display
from pygame.transform import scale
from pygame.image import load
from pygame.sprite import Sprite, Group, GroupSingle, groupcollide
from pygame import event
from pygame.locals import QUIT, KEYUP, K_SPACE
from pygame.time import Clock

pygame.init()
disparo = 0
tamanho = 800, 600  # variável que absorve o tamanho do plano em X e Y
superficie = display.set_mode((tamanho))  # variável que absorve a contrução do plano.
display.set_caption('O  Homem Aranha')  # funcão que escreve o nome da janela.

defaultFont = pygame.font.SysFont("Roboto", 30)

gameOverScreen = False
gameOverScreenText1 = defaultFont.render("Você Perdeu", True, "Black")
gameOverScreenText2 = defaultFont.render("Pressione Espaço Para Jogar Novamente", True, "Black")
gameOverScreenTextRect1 = gameOverScreenText1.get_rect(center=(400,100))
gameOverScreenTextRect2 = gameOverScreenText2.get_rect(center=(400,500))

victoryScreen = False
victoryScreenText1 = defaultFont.render("Parabéns, Você Venceu", True, "Black")
victoryScreenText2 = defaultFont.render("Pressione Espaço Para Jogar Novamente", True, "Black")
victoryScreenTextRect1 = victoryScreenText1.get_rect(center=(400,100))
victoryScreenTextRect2 = victoryScreenText2.get_rect(center=(400,500))

gameActive = True

fundo = scale(load('images/cidade.jpg'),
              tamanho)  # como a imagem é maior que o plano, usamos a função SCALE para transformar a imagem no tamanho do plano.


class HomemAranha(Sprite):  # criamos o primeiro sprint que irá compor o jogo, o objeto principal.
    def __init__(self, teia):
        super().__init__()  # defino essa função será usada em outras classes como herança.

        self.image = load('images/homemaranha_small.png')  # carrego a imagem e em seguida tranfiro para uma variável.
        self.rect = self.image.get_rect(center=(100,300))  # uso a função get_rect na imagem, onde irá me permitir o movimento no plano.
        self.velocidade = 2
        self.teia = teia
        self.lifeHearts = []
        self.remainingHearts = 3


    def update(self):

        keys = pygame.key.get_pressed()  # recebe o movimento

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > tamanho[1]:
            self.rect.bottom = tamanho[1]

    def soltarTeia(self):
        if len(self.teia) < 15:
            self.teia.add(
                Teia(*self.rect.center)
            )

    def initializeLifeHearts(self):
        self.remainingHearts = 3
        for i in range(3):
            self.lifeHearts.append(LifeHeart(lifeHeartsGroup, (80 * (i + 1), 510)))

    def damageSpider(self):
        self.lifeHearts[self.remainingHearts - 1].kill()
        self.remainingHearts -= 1
        self.lifeHearts.pop()

class LifeHeart(Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)

        self.image = pygame.image.load("images/heart.png")
        self.rect = self.image.get_rect(topright=pos)



class Teia(Sprite):  # criamos o segundo sprint que irá compor o jogo.
    def __init__(self, x, y):
        super().__init__()

        self.image = load('images/teia_small.png')
        self.rect = self.image.get_rect(
            center=(x, y)
        )

    def update(self):
        self.rect.x += 1
        if self.rect.x > tamanho[0]:
            self.kill()





# class Inimigo(Sprite):  # criamos o segundo sprint que irá compor o jogo.
#     def __init__(self):
#         super().__init__()
#
#         self.image = load('images/inimigo_1.png')
#         self.rect = self.image.get_rect(
#             center=(800, randint(10, 500))  # retorna posição aleatoria.
#         )
#
#     def update(self):
#         self.rect.x -= 0.1


class Inimigo(Sprite):  # criamos o segundo sprint que irá compor o jogo.
    def __init__(self, spider):
        super().__init__()

        self.image = load('images/inimigo_1.png')
        self.rect = self.image.get_rect(
            center=(900, randint(10, 500))  # retorna posição aleatoria.
        )
        self.spider = spider

    def update(self):
        self.rect.x -= 1

        if self.rect.left < 0:
            self.kill()
            self.spider.damageSpider()




class Chefao(Sprite):  # criamos o segundo sprint que irá compor o jogo.
    def __init__(self, spider):
        super().__init__()

        self.image = load('images/inimigo_2.png')
        self.rect = self.image.get_rect(
            center=(800, 300)  # retorna posição aleatoria.
        )
        self.spider = spider

    def update(self):
        self.rect.x -= 0.1

        if self.rect.left <= 0:
            self.spider.damageSpider()




# Espaço do display
grupo_inimigo = Group()
grupo_chefao = Group()
grupo_teia = Group()
homem_aranha = HomemAranha(grupo_teia)
grupo_aranha = GroupSingle(homem_aranha)
lifeHeartsGroup = Group()
grupo_chefao.add(Chefao(homem_aranha))

# grupo_inimigo.add(Inimigo())


round = 0
morte = 0
clock = Clock()


homem_aranha.initializeLifeHearts()

while True:

    clock.tick(120)

    for evento in event.get():
        if evento.type == QUIT:
            pygame.quit()

        if gameActive:
            if evento.type == KEYUP:
                if evento.key == K_SPACE:
                    homem_aranha.soltarTeia()
        else:
            if evento.type == KEYUP:
                if evento.key == K_SPACE:
                    gameActive = True
                    victoryScreen = False
                    gameOverScreen = False
                    resposta = False
                    homem_aranha.lifeHearts.clear()
                    lifeHeartsGroup.empty()
                    homem_aranha.initializeLifeHearts()
                    grupo_inimigo.empty()
                    # homem_aranha.remainingHearts = 3
                    homem_aranha.rect.center = (100,300)
                    grupo_teia.empty()
                    morte = 0
                    grupo_chefao.empty()
                    grupo_chefao.add(Chefao(homem_aranha))

    if gameActive:
        if round % 120 == 0:
            grupo_inimigo.add(Inimigo(homem_aranha))

        superficie.blit(fundo, (
            0, 0))  # Faço o Bit Blit na imagem no ponto 0,0 do plano definimo, com isso consigo inserir a imagem no jogo.
        grupo_aranha.draw(superficie)  # Desenhar o objeto no plano

        if morte < 6:
            grupo_inimigo.draw(superficie)
            grupo_inimigo.update()
            disparo = 0
        else:
            grupo_inimigo.empty()

            grupo_chefao.draw(superficie)
            grupo_chefao.update()

        grupo_teia.draw(superficie)
        lifeHeartsGroup.draw(superficie)
        grupo_aranha.update()
        grupo_teia.update()



        if groupcollide(grupo_teia, grupo_inimigo, True, True):
            morte += 1

        if groupcollide(grupo_aranha, grupo_inimigo, False, True) or groupcollide(grupo_aranha, grupo_chefao, False, False):
            homem_aranha.lifeHearts[homem_aranha.remainingHearts - 1].kill()
            homem_aranha.remainingHearts -= 1
            homem_aranha.lifeHearts.pop()

        # if :
        #     homem_aranha.lifeHearts[homem_aranha.remainingHearts - 1].kill()
        #     homem_aranha.remainingHearts -= 1
        #     homem_aranha.lifeHearts.pop()

        if homem_aranha.remainingHearts == 0:
            gameActive = False
            gameOverScreen = True


        if disparo == 10:
            resposta = True
        else:
            resposta = False

        if groupcollide(grupo_teia, grupo_chefao, True, resposta):

            if resposta:
                gameActive = False
                victoryScreen = True

            disparo += 1

    else:
        if gameOverScreen:
            superficie.fill("#EB494F")
            superficie.blit(gameOverScreenText1, gameOverScreenTextRect1)
            superficie.blit(gameOverScreenText2, gameOverScreenTextRect2)
        elif victoryScreen:
            superficie.fill("#EB494F")
            superficie.blit(victoryScreenText1, victoryScreenTextRect1)
            superficie.blit(victoryScreenText2, victoryScreenTextRect2)


    round += 1
    display.update()  # a função update atualiza os frames.