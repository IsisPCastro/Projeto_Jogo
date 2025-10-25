import pyxel
import random

class Personagem:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.cor = 5
        self.largura_mov = 29
        self.largura_atk = 32
        self.altura = 27
        self.largura = self.largura_mov
        self.dano = 5

        #Atributos de upgrades
        self.dano_base = 5
        self.up_dano = 2        #Valor que o dano aumenta por nível
        self.nivel_dano = 1     #Nível atual
        self.custo_dano = 90    #Custo inicial para upgrade

        #Variáveis para sprite
        self.contX = 0  
        self.contY = 0 
        self.x_mem = 0
        self.y_mem = 0

        #Variáveis para Ataque
        self.frame = 0
        self.frame_total = 4
        self.frame_delay = 2
        self.tick = 0
        self.atacando = False 
        self.direçao = 'direita'

    def animation(self, dx, dy):
        #Animação do personagem
        if not self.atacando:
            self.x_mem = self.contX * self.largura
            self.contX = (self.contX + 1) % 4

            if dy > 0: #Indo para baixo, linha 0
                self.contY = 0
            if dy < 0: #Indo para cima, linha 1
                self.contY = 1
            if dx > 0: #Indo para direita, linha 0
                self.contY = 2
                self.direçao = 'direita'
            if dx < 0: #Indo para esquerda, linha 1
                self.contY = 3
                self.direçao = 'esquerda'
            self.y_mem = self.contY * self.altura

        self.x = self.x + dx
        self.y = self.y + dy

    def move(self):
        dx = 0
        dy = 0

        if pyxel.btn(pyxel.KEY_RIGHT) and self.x <= (170 - 5):
            dx = 1
        if pyxel.btn(pyxel.KEY_LEFT) and self.x >= 5:
            dx = -1
        if pyxel.btn(pyxel.KEY_UP) and self.y >= 45:
            dy = -1
        if pyxel.btn(pyxel.KEY_DOWN) and self.y <= (100 - 20):
            dy = 1

        if dx != 0 or dy != 0:
            self.animation(dx, dy)

    def atacar(self):
        self.largura = self.largura_atk

        self.tick += 1
        if self.tick >= self.frame_delay:
            self.tick = 0
            self.frame += 1
            if self.frame >= self.frame_total:
                self.frame = 0

    def draw(self):
        sx = self.x 
        sy = self.y 

        if self.atacando:
            sprite_largura = self.largura_atk
            sprite_altura = self.altura

            #Coordenadas do frame atual
            u = self.frame * sprite_largura
            if self.direçao == 'direita':
                v = 4 * sprite_altura    #Linha 5 do sprite
            else:
                v = 5 * sprite_altura    #Linha 6 do sprite 
            sx -= 2
        
        else:
            sprite_largura = self.largura_mov
            sprite_altura = self.altura

            u = self.x_mem
            v = self.y_mem

            self.largura = self.largura_mov

        pyxel.blt(sx, sy, 1, u, v, sprite_largura, sprite_altura, 3)

class Inimigo:
    def __init__(self):
        self.x = 170
        self.y = random.randint(50, 100 - 27)
        self.largura = 24
        self.altura = 29
        self.frame = 0
        self.frame_total = 4
        self.delay = 6
        self.tick = 0
        self.vida = 10
        self.vida_max = 10
        self.moedas_recompensa = 5
        self.pontuaçao = 10

        #Variáveis para ataque
        self.atacando = False
        self.ataque_frame = 0
        self.ataque_framett = 4
        self.ataque_delay = 15
        self.ataque_tick = 0
        self.velocidade = 1
        self.dano = 5

        #Variáveis para dano
        self.hit = False
        self.hit_timer = 0     #contador de tempo piscando
        self.hit_duraçao = 10   #dura 10 frames piscando

        #Verifica se foi atingido
        self.atingido = False

    def revidar(self, dano):
        self.vida -= dano
        self.hit = True
        self.hit_timer = self.hit_duraçao
        if self.vida > 0:
            self.atacando = True
            self.ataque_tick = 0
            self.ataque_frame = 0


    def update(self, castelo):        
        #Controle do piscar
        if self.hit:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.hit = False
        
        #Movimento
        if not self.atacando:
            if self.x > castelo.x + castelo.largura:
                self.x -= self.velocidade 

                #Animação para avançar os frames
                self.tick += 1
                if self.tick >= self.delay:
                    self.tick = 0
                    self.frame = (self.frame + 1) % self.frame_total
            else:
                #Encosta no castelo
                self.atacando = True
                self.ataque_tick = 0
                self.ataque_frame = 0

        else:
            #Ataque animação
            self.ataque_tick += 1
            if self.ataque_tick >= self.ataque_delay:
                self.ataque_tick = 0
                self.ataque_frame = (self.ataque_frame + 1) % self.ataque_framett

                #Dano no castelo
                if self.x <= castelo.x + castelo.largura:
                    castelo.vida_atual -= self.dano


    def draw(self):                
        if self.atacando:
            img_x = 118 + self.ataque_frame * self.largura
            img_y = self.altura
        else:
            img_x = 118 + self.frame * self.largura
            img_y = 0

        pyxel.blt(self.x, self.y, 1, img_x, img_y, self.largura, self.altura, 3)

        #Barra de vida
        largura_barra = self.largura 
        altura_barra = 2
        barra_x = self.x 
        barra_y = self.y - 4 
        vida_atual = int(largura_barra * (self.vida / self.vida_max))

        pyxel.rect(barra_x, barra_y, largura_barra, altura_barra, 8)   #Fundo/borda
        pyxel.rect(barra_x, barra_y, vida_atual, altura_barra, 2)     #Barra proposcional a vida

class Inimigo_2:
    def __init__(self):
        self.x = 170
        self.y = random.randint(50, 100 - 27)
        self.largura = 27
        self.altura = 29
        self.frame = 0
        self.frame_total = 4
        self.delay = 6
        self.tick = 0
        self.vida = 20
        self.vida_max = 20
        self.moedas_recompensa = 10
        self.pontuaçao = 20

        #Variáveis para ataque
        self.atacando = False
        self.ataque_frame = 0
        self.ataque_framett = 4
        self.ataque_delay = 15
        self.ataque_tick = 0
        self.velocidade = 1
        self.dano = 10

        #Variáveis para dano
        self.hit = False
        self.hit_timer = 0     #contador de tempo piscando
        self.hit_duraçao = 10   #dura 10 frames piscando

        #Verifica se foi atingido
        self.atingido = False

    def revidar(self, dano):
        self.vida -= dano
        self.hit = True
        self.hit_timer = self.hit_duraçao
        if self.vida > 0:
            self.atacando = True
            self.ataque_tick = 0
            self.ataque_frame = 0


    def update(self, castelo):        
        #Controle do piscar
        if self.hit:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.hit = False
        
        #Movimento
        if not self.atacando:
            if self.x > castelo.x + castelo.largura:
                self.x -= self.velocidade 

                #Animação para avançar os frames
                self.tick += 1
                if self.tick >= self.delay:
                    self.tick = 0
                    self.frame = (self.frame + 1) % self.frame_total
            else:
                #Encosta no castelo
                self.atacando = True
                self.ataque_tick = 0
                self.ataque_frame = 0

        else:
            #Ataque animação
            self.ataque_tick += 1
            if self.ataque_tick >= self.ataque_delay:
                self.ataque_tick = 0
                self.ataque_frame = (self.ataque_frame + 1) % self.ataque_framett

                #Dano no castelo
                if self.x <= castelo.x + castelo.largura:
                    castelo.vida_atual -= self.dano


    def draw(self):                
        if self.atacando:
            img_x = 131 + self.ataque_frame * self.largura
            img_y = 140
        else:
            img_x = 131 + self.frame * self.largura
            img_y = 111

        pyxel.blt(self.x, self.y, 1, img_x, img_y, self.largura, self.altura, 3)

        #Barra de vida
        larg_barra = self.largura 
        alt_barra = 2
        barra_x = self.x 
        barra_y = self.y - 4 
        vida_atual = int(larg_barra * (self.vida / self.vida_max))

        pyxel.rect(barra_x, barra_y, larg_barra, alt_barra, 8)   #Fundo/borda
        pyxel.rect(barra_x, barra_y, vida_atual, alt_barra, 2)     #Barra proposcional a vida

class Inimigo_3:
    def __init__(self):
        self.x = 170
        self.y = random.randint(50, 100 - 27)
        self.largura = 56
        self.altura = 24
        self.frame = 0
        self.frame_total = 4
        self.delay = 6
        self.tick = 0
        self.vida = 30
        self.vida_max = 30
        self.moedas_recompensa = 20
        self.pontuaçao = 30 

        #Variáveis para ataque
        self.atacando = False
        self.ataque_frame = 0
        self.ataque_framett = 4
        self.ataque_delay = 15
        self.ataque_tick = 0
        self.velocidade = 1
        self.dano = 20

        #Variáveis para dano
        self.hit = False
        self.hit_timer = 0     #contador de tempo piscando
        self.hit_duraçao = 10   #dura 10 frames piscando

        #Verifica se foi atingido
        self.atingido = False

    def revidar(self, dano):
        self.vida -= dano
        self.hit = True
        self.hit_timer = self.hit_duraçao
        if self.vida > 0:
            self.atacando = True
            self.ataque_tick = 0
            self.ataque_frame = 0


    def update(self, castelo):        
        #Controle do piscar
        if self.hit:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.hit = False
        
        #Movimento
        if not self.atacando:
            if self.x > castelo.x + castelo.largura:
                self.x -= self.velocidade 

                #Animação para avançar os frames
                self.tick += 1
                if self.tick >= self.delay:
                    self.tick = 0
                    self.frame = (self.frame + 1) % self.frame_total
            else:
                #Encosta no castelo
                self.atacando = True
                self.ataque_tick = 0
                self.ataque_frame = 0

        else:
            #Ataque animação
            self.ataque_tick += 1
            if self.ataque_tick >= self.ataque_delay:
                self.ataque_tick = 0
                self.ataque_frame = (self.ataque_frame + 1) % self.ataque_framett

                #Dano no castelo
                if self.x <= castelo.x + castelo.largura:
                    castelo.vida_atual -= self.dano


    def draw(self):                
        if self.atacando:
            img_x = 15 + self.ataque_frame * self.largura
            img_y = 227
        else:
            img_x = 15 + self.frame * self.largura
            img_y = 201

        pyxel.blt(self.x, self.y, 2, img_x, img_y, self.largura, self.altura, 0)

        #Barra de vida
        larg_barra = self.largura 
        alt_barra = 2
        barra_x = self.x 
        barra_y = self.y - 4 
        vida_atual = int(larg_barra * (self.vida / self.vida_max))

        pyxel.rect(barra_x, barra_y, larg_barra, alt_barra, 8)   #Fundo/borda
        pyxel.rect(barra_x, barra_y, vida_atual, alt_barra, 2)     #Barra proporcional a vida

class Inimigos:   #Gerencia os inimigos
    def __init__(self, ordas):
        self.inimigos = []
        self.timer_spawn = 0
        self.ordas = ordas         

    def update(self, castelo):
        #Lista para devolver inimigos mortos
        mortos = []

        #Spawn dos inimigos
        if not self.ordas.terminou_orda:
            self.timer_spawn += 1
            if self.timer_spawn > 40:
                self.timer_spawn = 0
                self.ordas.qtd_spaw += 1

                #pega inimigo da orda atual
                novo = self.ordas.spawn_inimigo()
                self.inimigos.append(novo)

                #Verifica fim da orda
                if self.ordas.qtd_spaw >= self.ordas.qtd_max:
                    self.ordas.terminou_orda = True 

        #Atualiza inimigos
        for inimigo in self.inimigos[:]:
            inimigo.update(castelo) 
            if inimigo.vida <= 0:
                self.inimigos.remove(inimigo)
                mortos.append(inimigo)    #devolve para a classe jogo
        return mortos 
        
    def draw(self):
        for inimigo in self.inimigos:
            inimigo.draw()

class Moeda:
    def __init__(self, x, y, valor):
        self.x = x
        self.y = y 
        self.largura = 8
        self.altura = 8
        self.frame = 0
        self.framett = 4   #Total de frames no sprite
        self.delay = 5   #velocidade da animação
        self.tick = 0
        self.valor = valor 

    def update(self):
        #Animação
        self.tick += 1
        if self.tick >= self.delay:
            self.tick = 0
            self.frame = (self.frame + 1) % self.framett

    def draw(self):
        img_x = 218 + self.frame * 8   #posição inicial + avanço do frame
        img_y = 0
        pyxel.blt(self.x, self.y, 1, img_x, img_y, 8, 8, 3)

class Moedas:    #Gerencia as moedas
    def __init__(self):
        self.moedas = []

    def soma(self, x, y, valor):
        self.moedas.append(Moeda(x, y, valor))

    def update(self):
        for moeda in self.moedas:
            moeda.update()

    def draw(self):
        for moeda in self.moedas:
            moeda.draw()

class Ordas:
    def __init__(self):
        self.orda_atual = 1
        self.qtd_spaw = 0
        self.qtd_max = 10
        self.terminou_orda = False

    def proxima_orda(self):
        if self.terminou_orda:
            self.orda_atual += 1
            self.qtd_spaw = 0
            self.terminou_orda = False

            #Aumenta a dificuldade gradativamente
            if self.orda_atual == 2:
                self.qtd_max = 12
            elif self.orda_atual == 3:
                self.qtd_max = 12
            elif self.orda_atual == 4:
                self.qtd_max = 15
            elif self.orda_atual == 5:
                self.qtd_max = 15
            elif self.orda_atual == 6:
                self.qtd_max = 25
            elif self.orda_atual == 7:
                self.qtd_max = 35
            elif self.orda_atual == 8:
                self.qtd_max = 40
            
    def spawn_inimigo(self):
        todos = [Inimigo(), Inimigo_2(), Inimigo_3()]
        #Define qual inimigo nasce em cada orda
        if self.orda_atual == 1:
            return Inimigo()
        elif self.orda_atual == 2:
            return Inimigo()
        elif self.orda_atual == 3:
            return Inimigo_2()
        elif self.orda_atual == 4:
            return random.choice([Inimigo(), Inimigo_2()])
        elif self.orda_atual == 5:
            return Inimigo_3()
        elif self.orda_atual == 6:
            return random.choice([Inimigo(), Inimigo_3()])
        elif self.orda_atual == 7:
            return random.choice([Inimigo_2(), Inimigo_3()])
        elif self.orda_atual == 8:
            return random.choice(todos)

class Castelo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 27
        self.altura = 90
        self.cor = 13
        self.vida_max = 100
        self.vida_atual = self.vida_max

    def update(self):
        pass 

    def vida(self):
        #Barra de vida do castelo
            pyxel.rect(6, 6, 102, 5, 10)    #Borda

            #Calcula a largura proporcional
            largura = int((self.vida_atual / self.vida_max) * 100)

            #Desenha a barra de vida
            pyxel.rect(7, 7, largura, 3, 3)

    def draw(self):
        #Desenha a barreira invísel de colisão do castelo
        pyxel.rect(self.x, self.y, self.largura, self.altura, self.cor)

class Flecha:
    def __init__(self, x, y, direçao, alvo, dano):
        self.x = x
        self.y = y 
        self.direçao = direçao
        self.velocidade = 2 
        self.ativa = True 
        self.largura = 4
        self.altura = 2
        self.dano = dano 

        #Movimento na diagonal 
        dx = alvo.x - self.x 
        dy = alvo.y - self.y 

        passo = max(abs(dx), abs(dy), 1)  #Encontra o maior valor absoluto entre dx e dy

        self.dx_ajuste = dx / passo 
        self.dy_ajuste = dy / passo 

        self.dx = self.dx_ajuste * self.velocidade 
        self.dy = self.dy_ajuste * self.velocidade 

    def update(self, inimigos):
        self.x += self.dx 
        self.y += self.dy 

        #colisão da flecha no alvo
        for inimigo in inimigos:
            if (self.x < inimigo.x + inimigo.largura and 
                self.x + self.largura > inimigo.x and 
                self.y < inimigo.y + inimigo.altura and 
                self.y + self.altura > inimigo.y):
                inimigo.vida -= self.dano  
                if inimigo.vida <= 0:
                    self.ativa = False 
                    return inimigo    #Retorna o inimigo morto pela flecha
                else:
                    self.ativa = False 
                break 

        #Se sair da tela
        if self.x < -10 or self.x > 170 or self.y < -10 or self.y > 110:
            self.ativa = False 
        
        return None 

    def draw(self):
        if self.ativa:
            pyxel.rect(self.x, self.y, self.largura, self.altura, 7)

class Torre:
    def __init__(self, x, y):
        self.x = x 
        self.y = y 
        self.alcance = 60
        self.recarga = 50     #Tempo entre ataques
        self.timer = 0
        self.flechas = []
        self.direçao = 1

        #Atributos para upgrade
        self.dano_flecha = 6

        self.nivel_dano = 1         #Nível do dano
        self.custo_dano = 120       #Custo inicial
        self.up_dano = 2            #O quanto vai aumentar p/ nível

        #Controle da arqueira
        self.frame = 0
        self.frame_timer = 0
        self.delay = 6   #controla velocidade da animação
        self.atacando = False 

        #Sprites
        self.largura = 22
        self.altura = 26

        #Atributos de compra e update
        self.custo = 150
        self.comprada = False 

    def update(self, inimigos):
        if not self.comprada:    #Só funciona se adquirida
            return []
        
        self.timer += 1
        alvo = None 

        #Procurar inimigo no alcance
        menor_dist = 999
        for inimigo in inimigos:
            dx = abs(inimigo.x - self.x)
            dy = abs(inimigo.y - self.y)
            dist = dx + dy 
            if dist < menor_dist and dx < self.alcance:
                menor_dist = dist 
                alvo = inimigo 
                
        if alvo:
            if alvo.x > self.x:
                self.direçao = 1
            else:
                self.direçao = -1

            if self.timer >= self.recarga:
                self.atacando = True 
                self.timer = 0
                self.frame = 0   #Reinicia a animação
            
                #Flecha só sai no sprite de atirar
                self.flechas.append(Flecha(self.x, self.y, self.direçao, alvo, self.dano_flecha))

        inimigos_mortos = []

        #Atualiza as flechas
        for flecha in self.flechas[:]:
            inimigo_morto = flecha.update(inimigos)

            if inimigo_morto:
                inimigos_mortos.append(inimigo_morto)
            if not flecha.ativa:
                self.flechas.remove(flecha)

        #Animação arqueira
        if self.atacando:
            self.frame_timer += 1
            if self.frame_timer > 6:   #velocidade da animação
                self.frame = (self.frame + 1) % 4
                self.frame_timer = 0
                if self.frame == 0:
                    self.atacando = False  

        return inimigos_mortos   #Retorna a lista de inimigos mortos       

    def draw(self):
        if not self.comprada:   #Só aparece se adquirida
            return 
        #Torre fixa
        pyxel.blt(80, 38, 2, 172, 0, 26, 30, 0)

        #Sprites arqueira
        arqueira_x = self.x 
        arqueira_y = self.y - 22

        if self.atacando:
            frame_x = self.frame * 22
        else:
            frame_x = 0

        if self.direçao == 1:
            frame_y = 0
        else:
            frame_y = 26

        img_x = 118 + frame_x
        img_y = 58 + frame_y

        pyxel.blt(arqueira_x, arqueira_y, 1, img_x, img_y, 22, 26, 3) 

        #Desenhar flechas
        for flecha in self.flechas:
            flecha.draw()

class Jogo:
    def __init__(self):
        #Inicializa o jogo
        self.resetar()

        #Menu
        self.estado = 'menu'

        #Janela e título do jogo
        pyxel.init(170,100, title= 'Fight For Crystal', fps= 20)

        #Carregar imagens
        pyxel.images[0].load(0, 0, 'Menu do jogo.png')
        pyxel.images[1].load(0,0, 'Sprites.png')
        pyxel.images[2].load(0, 0, 'Backgrounds.png')

        #Habilita mouse
        pyxel.mouse(True)

        #Última linha
        pyxel.run(self.update, self.draw)

    def comprar_upgrade(self, upgrade_tipo):
        if upgrade_tipo == 'personagem_dano':
            alvo = self.p 
            custo = alvo.custo_dano 

            if self.coins >= custo:
                self.coins -= custo
                alvo.nivel_dano += 1 
                alvo.dano += alvo.up_dano

                #recálculo do custo
                alvo.custo_dano = int(custo * 1.5)

                self.msg_orda = f'Dano atual: {alvo.dano}'
                self.msg_timer = 60
            else:
                self.msg_orda = 'MOEDAS INSUFICIENTES!'
                self.msg_timer = 60 

        elif upgrade_tipo == 'torre_recarga':
            alvo = self.torre 
            custo = alvo.custo_recarga 

            if self.coins >= custo:
                self.coins -= custo 
                alvo.nivel_recarga += 1
                alvo.recarga -= alvo.up_recarga 

                alvo.custo_recarga = int(custo * 1.5)

                self.msg_orda = f'Recarga: {alvo.recarga}'
                self.msg_timer = 60
            else:
                self.msg_orda = 'MOEDAS INSUFICIENTES!'
                self.msg_timer = 60

        elif upgrade_tipo == 'torre_dano':
            alvo = self.torre
            custo = alvo.custo_dano

            if self.coins >= custo:
                self.coins -= custo 
                alvo.nivel_dano += 1
                alvo.dano_flecha += alvo.up_dano 

                alvo.custo_dano = int(custo * 1.5)

                self.msg_orda = f'Dano flecha: {alvo.dano_flecha}'
                self.msg_timer = 60
            else:
                self.msg_orda = 'MOEDAS INSUFICIENTES!'
                self.msg_timer = 60 

    def update_loja(self):
        #Permite sair da loja usando a tecla P
        if pyxel.btnp(pyxel.KEY_P):
            self.estado = 'jogando'
            return 
        
        #Coordenadas do mouse
        mouse_x = pyxel.mouse_x
        mouse_y = pyxel.mouse_y

        #Botão de compra
        btn_torre_x = 50
        btn_torre_y = 23
        btn_torre_larg = 75
        btn_torre_alt = 15

        #Botão upgrade Personagem
        btn_p_dano_x = 35
        btn_p_dano_y = 40
        btn_p_larg = 105
        btn_p_alt = 15 

        #Detecta clique do mouse
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #Compra da torre
            if (mouse_x >= btn_torre_x and 
                mouse_x <= btn_torre_x + btn_torre_larg and 
                mouse_y >= btn_torre_y and 
                mouse_y <= btn_torre_y + btn_torre_alt):
                if not self.torre.comprada:
                    custo = self.torre.custo
                    if self.coins >= custo:
                        self.coins -= custo 
                        self.torre.comprada = True 
                        self.msg_orda = f'TORRE ATIVADA! (-{custo} coins)'
                        self.msg_timer = 60
                    else:
                        self.msg_orda = 'MOEDAS INSUFICIENTES!'
                        self.msg_timer = 60

            #Clique upgrade personagem
            elif  (mouse_x >= btn_p_dano_x and mouse_x <= btn_p_dano_x + btn_p_larg and 
              mouse_y >= btn_p_dano_y and mouse_y <= btn_p_dano_y + btn_p_alt):
                self.comprar_upgrade('personagem_dano')

            #Botão upgrade dano Torre
            btn_tdano_x = 35
            btn_tdano_y = 60

            if self.torre.comprada:
                if (mouse_x >= btn_tdano_x and mouse_x <= btn_tdano_x + btn_torre_larg and 
                mouse_y >= btn_tdano_y and mouse_y <= btn_tdano_y + btn_torre_alt):
                    self.comprar_upgrade('torre_dano')
    
    def resetar(self):
        self.torre = Torre(80, 38)
        self.p = Personagem(60, 60)
        self.cast = Castelo(0, 50)
        self.ordas = Ordas()
        self.inimigos = Inimigos(self.ordas)
        self.moedas = Moedas()
        self.pontuaçao = 0
        self.coins = 0
        self.msg_orda = ''
        self.msg_timer = 0
        
        #Ataque com a espada
        self.atacando = False
        self.tempo_ataque = 0
        self.atingido = False    #Verifica se o inimigo levou dano no ataque, evitando ataque repetitivo e morte instantânea

    def update_jogando(self):
        self.p.move()
        mortos = self.inimigos.update(self.cast)
        self.inimigos.draw()
        self.torre.update(self.inimigos.inimigos)

        #Capturar mortes da torre e gerar moedas
        mortos_torre = self.torre.update(self.inimigos.inimigos)

        for inimigo_morto in mortos_torre:
            moeda_x = inimigo_morto.x + 7
            moeda_y = inimigo_morto.y + 3
            recompensa = inimigo_morto.moedas_recompensa
            self.moedas.soma(moeda_x, moeda_y, recompensa)
            self.pontuaçao += inimigo_morto.pontuaçao  

        #Clique do botão
        btn_loja_x = 5
        btn_loja_y = 85
        btn_loja_larg = 13
        btn_loja_alt = 13

        mouse_x = pyxel.mouse_x
        mouse_y = pyxel.mouse_y

        clicou = (mouse_x >= btn_loja_x and mouse_x <= btn_loja_x + btn_loja_larg and 
                  mouse_y >= btn_loja_y and mouse_y <= btn_loja_y + btn_loja_alt)
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and clicou:
            self.estado = 'loja'

        #Quando a orda acabar e todos morrerem, avança
        if self.ordas.terminou_orda and len(self.inimigos.inimigos) == 0:
            self.ordas.proxima_orda()
            self.msg_orda = f'ORDA {self.ordas.orda_atual} / 8'
            self.msg_timer = 60
             
        #Coletar moedas
        self.moedas.update()
        for moeda in self.moedas.moedas[:]:
            if (self.p.x < moeda.x + moeda.largura and
                self.p.x + self.p.largura > moeda.x and 
                self.p.y < moeda.y + moeda.altura and 
                self.p.y + self.p.altura > moeda.y):
                self.coins += moeda.valor 
                self.moedas.moedas.remove(moeda)
        
        #Colisão do personagem no castelo
        d_circ = self.p.x + (self.p.largura - 8) 
        d_cast = self.cast.x + self.cast.largura

        if d_circ <= d_cast + 5:
            self.p.x += 1

        #Ataques e colisões
        self.ataque()
        self.colisao_espada()

        #Game Over
        if self.cast.vida_atual <= 0:
            self.estado = 'game_over'
             
        #Vitória
        if self.ordas.orda_atual == 9 and len(self.inimigos.inimigos) == 0:
            self.estado = 'vitoria'
    
    def update(self):
        mouse_x = pyxel.mouse_x
        mouse_y = pyxel.mouse_y

        if self.estado == 'menu':
            #Botão Jogar
            btn_play_x = 52
            btn_play_y = 59
            btn_play_larg = 62
            btn_play_alt = 13 

            #Botão Como Jogar
            btn_help_x = 52
            btn_help_y = 73
            btn_help_larg = 62
            btn_help_alt = 13 

            #Clique dos botões
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if (mouse_x >= btn_play_x and mouse_x < btn_play_x + btn_play_larg and
                    mouse_y >= btn_play_y and mouse_y < btn_play_y + btn_play_alt):
                    self.resetar()
                    self.estado = 'jogando'

                if (mouse_x >= btn_help_x and mouse_x < btn_help_x + btn_help_larg and 
                    mouse_y >= btn_help_y and mouse_y < btn_help_y + btn_help_alt):
                    self.estado = 'como_jogar'

            if pyxel.btnp(pyxel.KEY_A):
                self.resetar()
                self.estado = 'jogando'

        elif self.estado == 'como_jogar':
            if pyxel.btnp(pyxel.KEY_X):
                self.estado = 'menu'
        
        elif self.estado == 'loja':
            self.update_loja()

        elif self.estado == 'jogando':
             self.update_jogando()
             
        elif self.estado == 'vitoria':
            if pyxel.btnp(pyxel.KEY_R):
                self.resetar()
                self.estado = 'jogando'
            if pyxel.btnp(pyxel.KEY_E):
                self.estado = 'menu'                

        elif self.estado == 'game_over':
            if pyxel.btnp(pyxel.KEY_R):
                self.resetar()
                self.estado = 'jogando'
            if pyxel.btnp(pyxel.KEY_E):
                self.estado = 'menu'
   
    def ataque(self):
        if pyxel.btn(pyxel.KEY_SPACE) and not self.atacando:
            self.atacando = True
            self.p.atacando = True 
            self.tempo_ataque = 10    #Dura 10 frames 

        if self.atacando:
            self.tempo_ataque -= 1
            self.p.atacar()      #atualiza frame do ataque
            if self.tempo_ataque <= 0:
                self.atacando = False
                self.p.atacando = False  
                self.p.frame = 0      #reseta o frame de ataque
                self.p.largura = self.p.largura_mov
                #Reseta inimigos para poder atingir de novo
                for inimigo in self.inimigos.inimigos:
                    inimigo.atingido = False 

    def colisao_espada(self):
        #Colisão da espada com inimigo
        if self.atacando:
            if self.p.direçao == 'direita':
                alcance_x = self.p.x + self.p.largura // 2
            else: #esquerda
                alcance_x = self.p.x - 12

            alcance_y = self.p.y
            
            for inimigo in self.inimigos.inimigos:
                if not inimigo.atingido:   #só aplica dano se ainda não atingido
                    if (alcance_x < inimigo.x + 12 and
                        alcance_x + 12 > inimigo.x and
                        alcance_y < inimigo.y + 12 and
                        alcance_y + 12 > inimigo.y):
                        inimigo.revidar(self.p.dano)
                        inimigo.atingido = True   #marca como atingido

                        if inimigo.vida <= 0:
                            moeda_x = inimigo.x + 10
                            moeda_y = inimigo.y + 3
                            recompensa = inimigo.moedas_recompensa
                            self.moedas.soma(moeda_x, moeda_y, recompensa) 
                            self.pontuaçao += inimigo.pontuaçao
    
    def draw_jogando(self):
        self.cast.draw()
        pyxel.blt(0, 0, 2, 0, 0, 170, 100)
        self.cast.vida()
        self.torre.draw()
        self.inimigos.draw()
        self.p.draw()
        self.moedas.draw()
        pyxel.text(120, 15, f"Pontos:{self.pontuaçao}", 10) 
        pyxel.text(120, 6, f" Coins:{self.coins}", 10)

        #Botão clicável
        btn_loja_x = 5
        btn_loja_y = 85
        sprite_u = 0
        sprite_v = 201
        btn_larg = 13
        btn_alt = 13

        pyxel.blt(btn_loja_x, btn_loja_y, 2, sprite_u, sprite_v, btn_larg, btn_alt, 0)
        
        #Mensagem de orda
        if self.msg_timer > 0:
            pyxel.text(69, 45, self.msg_orda, 0)   #sombra
            pyxel.text(70, 45, self.msg_orda, 8)   #texto
            self.msg_timer -= 1
            
    def draw_loja(self):
        self.draw_jogando()
        #Desenho da aba
        pyxel.rect(20, 10, 130, 85, 1)
        pyxel.text(55, 15, 'Loja de Batalha', 0)
        pyxel.text(56, 15, 'Loja de Batalha', 6)

        #Desenho do botão da torre
        btn_x = 50
        btn_y = 23
        btn_larg = 75
        btn_alt = 15
        cor_btn = 8 

        if not self.torre.comprada and self.coins >= self.torre.custo:
            cor_btn = 3    #Pode comprar
        elif self.torre.comprada:
            cor_btn = 13    #Já foi adquirida

        pyxel.rect(btn_x, btn_y, btn_larg, btn_alt, cor_btn)

        #Texto do botão
        if self.torre.comprada:
            texto = 'TORRE: ADQUIRIDA'
        else:
            texto = f'TORRE: {self.torre.custo} COINS'

        pyxel.text(btn_x + 5, btn_y + 5, texto, 0)

        #Desenho botão up dano Personagem
        btn_x = 35
        btn_y = 40
        btn_larg = 105
        btn_alt = 15

        cor_btn = 8
        if self.coins >= self.p.custo_dano:
            cor_btn = 3 

        pyxel.rect(btn_x, btn_y, btn_larg, btn_alt, cor_btn)
        texto = f'DANO P. (Lv {self.p.nivel_dano}): {self.p.custo_dano} Coins'
        pyxel.text(btn_x + 4, btn_y + 5, texto, 0)

        #Desenho botão up dano Torre
        if self.torre.comprada:
            btn_x_torre = 35
            btn_y_torre = 60 

            cor_btn_torre = 8
            if self.coins >= self.torre.custo_dano:
                cor_btn_torre = 3

            pyxel.rect(btn_x_torre, btn_y_torre, btn_larg, btn_alt, cor_btn_torre)

            texto_torre = f'DANO T. (Lv {self.torre.nivel_dano}): {self.torre.custo_dano} Coins'
            pyxel.text(btn_x_torre + 5, btn_y_torre + 5, texto_torre, 0)

        #Instrução de saída
        pyxel.text(55, 85, 'Press P | Return', 0)
        pyxel.text(56, 85, 'Press P | Return', 7)
    
    
    def draw(self):
        pyxel.cls(0)
        mouse_x = pyxel.mouse_x
        mouse_y = pyxel.mouse_y
        
        if self.estado == 'menu':
            pyxel.blt(0, 0, 0, 0, 0, 170, 100)
            #Botão Jogar
            btn_play_x = 52
            btn_play_y = 59
            btn_play_larg = 62
            btn_play_alt = 13 

            #Botão Como Jogar
            btn_help_x = 52
            btn_help_y = 73
            btn_help_larg = 62
            btn_help_alt = 13

            #Animação Hover (botão jogar)
            hover_play = (mouse_x >= btn_play_x and mouse_x < btn_play_x + btn_play_larg and
                        mouse_y >= btn_play_y and mouse_y < btn_play_y + btn_play_alt)

            play_v = 0
            if hover_play:
                play_v = 63

            pyxel.blt(btn_play_x, btn_play_y, 0, play_v, 202, btn_play_larg, btn_play_alt, 0)

            #Animação Hover (botão help)
            hover_help = (mouse_x >= btn_help_x and mouse_x < btn_help_x + btn_help_larg and 
                    mouse_y >= btn_help_y and mouse_y < btn_help_y + btn_help_alt)
            
            help_v = 0
            if hover_help:
                help_v = 63

            pyxel.blt(btn_help_x, btn_help_y, 0, help_v, 219, btn_help_larg, btn_help_alt, 0)

        elif self.estado == 'como_jogar':
            pyxel.cls(0)
            pyxel.text(65, 8, "COMO JOGAR", 7)
            pyxel.text(10, 20, "Use as setas para mover.", 10)
            pyxel.text(10, 30, "Barra de Espaco para atacar.", 10)
            pyxel.text(10, 40, "Loja de batalha | botao azul.", 10)
            pyxel.text(10, 50, "Voce deve proteger o castelo.", 10)
            pyxel.text(10, 60, "Nao deixe os inimigos passarem!", 10)
            pyxel.text(10, 70, "Adquira a Torre da Arqueira na loja!", 10)
            pyxel.text(50, 85, "PRESS X TO RETURN", 8)

        elif self.estado == 'jogando':
            self.draw_jogando()

        elif self.estado == 'loja':
            self.draw_loja()
        
        elif self.estado == 'game_over':
            pyxel.blt(0, 0, 2, 0, 100, 170, 100)

        elif self.estado == 'vitoria':
            pyxel.blt(0, 0, 0, 0, 102, 170, 100)
            pyxel.text(100, 85, f"Points:{self.pontuaçao}", 10)          

Jogo()