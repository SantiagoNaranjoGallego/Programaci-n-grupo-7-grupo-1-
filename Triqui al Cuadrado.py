import pygame

pygame.init()

Ancho = 574
Alto = 624
Ancho_juego = (474)
Alto_juego = (Ancho_juego)

azul_claro = (204, 236, 255)
verde = (63, 155, 76)
negro = (0, 0, 0)
blanco = (255, 255, 255)
rojo = (240, 73, 89)
azul_os = (70, 127, 244)

ventana = pygame.display.set_mode((Ancho, Alto))
pygame.display.set_caption('TRIQUI AL CUADRADO')
ventana.fill((azul_claro))

matriz_completa = []
for i in range(3):
    matriz_completa.append([])
    for j in range(3):
        matriz_completa[i].append([])
        for k in range(3):
            matriz_completa[i][j].append([])
            for l in range(3):
                matriz_completa[i][j][k].append(0)

matriz_grande = []
for i in range(3):
    matriz_grande.append([])
    for j in range(3):
        matriz_grande[i].append(0)

matriz_pequeña = []
for i in range(3):
    matriz_pequeña.append([])
    for j in range(3):
        matriz_pequeña[i].append(0)


def actualizar_ventana(ventana,turno):
    ventana.fill((azul_claro))
    pygame.draw.rect(ventana, negro, (50, 100, 474, 474))
    if turno == "uno":
        tex = "azul"
        color = azul_os
    else:
        tex = "rojo"
        color = rojo

    letra = pygame.font.SysFont("Impact", 50)
    texto = letra.render("TRIQUI AL CUADRADO", True, negro)
    ventana.blit(texto, (87,25))
    letra = pygame.font.SysFont("Impact", 25)
    texto = letra.render("Turno de "+tex, True, color)
    ventana.blit(texto, (220,580))
    pygame.display.update()
    
    for fila in range(3):
        for columna in range(3):
            x = 53 + 157 * columna
            y = 103 + 157*fila
            pygame.draw.rect(ventana, verde, (x, y, 154, 154))
            for hor in range(3):
                for ver in range(3):
                    pygame.draw.rect(ventana, blanco, (x + 52*ver, y + 52*hor, 50, 50))
                    c = matriz_completa[fila][columna][hor][ver]
                    if c == 1:
                        pygame.draw.circle(ventana, azul_os, [
                                           x + 52*ver + 25, y + 52*hor+25], 15, 5, draw_top_right=True)
                        pygame.draw.circle(ventana, azul_os, [
                                           x + 52*ver + 25, y + 52*hor+25], 15, 5, draw_top_left=True)
                        pygame.draw.circle(ventana, azul_os, [
                                           x + 52*ver + 25, y + 52*hor+25], 15, 5, draw_bottom_left=True)
                        pygame.draw.circle(ventana, azul_os, [
                                           x + 52*ver + 25, y + 52*hor+25], 15, 5, draw_bottom_right=True)
                    elif c == 2:
                        pygame.draw.line(ventana, rojo, [
                                         x + 52*ver + 10, y + 52*hor+10], [x + 52*ver + 40, y + 52*hor+40], 5)
                        pygame.draw.line(ventana, rojo, [
                                         x + 52*ver + 40, y + 52*hor+10], [x + 52*ver + 10, y + 52*hor+40], 5)

    pygame.display.update()

def validar_triqui(tabla, turno):
    if turno == "uno":
        valor = 1
    else:
        valor = 2
    # Primeras dos condiciones // Fila-columna
    for x in range(3):
        if tabla[x][0] == tabla[x][1] == tabla[x][2] == valor:
            return True
        elif tabla[0][x] == tabla[1][x] == tabla[2][x] == valor:
            return True

    # Diagonal principal
    c1 = 0
    c2 = 0
    for x in range(3):
        for y in range(3):
            if tabla[x][y] == valor:
                if x == y:
                    c1 += 1
                if x+y == 2:
                    c2 += 1
    if c1 == 3 or c2 == 3:
        return True
    else:
        return False

def actualizar_juego(turno, pos, pj):
    if pos[0] <= 207:
        col = 0
    elif pos[0] >= 210 and pos[0] <= 364:
        col = 1
    else:
        col = 2

    if pos[1] <= 257:
        fila = 0
    elif pos[1] >= 260 and pos[1] <= 414:
        fila = 1
    else:
        fila = 2
    colval = False
    filaval = False
    for f in range(3):
        for c in range(3):
            x = 53 + 157 * c
            y = 103 + 157*f
            for fi in range(3):
                for ci in range(3):
                    if pos[0] >= x + 52*ci and pos[0] <= x + 52*ci+50:
                        col_i = ci
                        colval = True
                    if pos[1] >= y + 52*fi and pos[1] <= y + 52*fi+50:
                        fila_i = fi
                        filaval = True
                    if colval and filaval:
                        break
                if colval and filaval:
                    break

    if not colval or not filaval:
        return(turno, 5, 5, pj, False)

    casilla = matriz_completa[fila][col][fila_i][col_i]
    if casilla == 0:
        if turno == "uno":
            s = 1
            matriz_completa[fila][col][fila_i][col_i] = s
        else:
            s = 2
            matriz_completa[fila][col][fila_i][col_i] = s
    else:
        return(turno, fila_i, col_i, pj, False)

    for i in range(3):
        for j in range(3):
            matriz_pequeña[i][j] = matriz_completa[fila][col][i][j]

    if validar_triqui(matriz_pequeña, turno):
        matriz_grande[fila][col] = s
    if validar_triqui(matriz_grande, turno):
        return(turno, fila, col,False, True)

    else:
        if matriz_grande[fila_i][col_i] == 0:
            if turno == "uno":
                return ("dos", fila_i, col_i, False, False)
            else:
                return ("uno", fila_i, col_i, False, False)
        else:
            if turno == "uno":
                return ("dos", fila_i, col_i, True, False)
            else:
                return ("uno", fila_i, col_i, True, False)

def gano(turno):
    if turno == "uno":
        tex = "azul"
        color = azul_os
    else:
        tex = "rojo"
        color = rojo
    pygame.draw.rect(ventana, azul_claro, (0,0, 574, 624))

    letra = pygame.font.SysFont("Impact", 60)
    texto = letra.render("GANÓ "+tex.upper(), True, color)
    texto1 = texto.get_rect()
    ventana.blit(texto, (150,250))
    pygame.display.update()

def var_casillas_invalidas(p):
    for a in range(3):
        for b in range(3):
            if p[0] >= (53+157*b) and p[0] <= (53+157*b+157):
                if p[1] >= (103+157*a) and p[1] <= (103+157*a+157):
                    if matriz_grande[a][b] != 0:
                        return False
                    else:
                        return True

# Ciclo para cerrar programa
def main():
    turno = "uno"
    pj = True
    ganador = False
    f = 5
    c = 5
    actualizar_ventana(ventana,turno)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    p = pygame.mouse.get_pos()  # (x,y)
                    if pj:
                        if p[0] > 53 and p[0] < 521 and p[1] > 103 and p[1] < 571:
                            if var_casillas_invalidas(p):
                                t, f, c, pj, ganador = actualizar_juego(turno, p, pj)
                                turno = t
                                actualizar_ventana(ventana,turno)
                    else:
                        for a in range(3):
                            for b in range(3):
                                if a == f and b == c:
                                    if p[0] >= (53+157*c) and p[0] <= (53+157*c+157):
                                        if p[1] >= (103+157*f) and p[1] <= (103+157*f+157):
                                            if var_casillas_invalidas(p):
                                                t, f, c, pj, ganador = actualizar_juego(turno, p, pj)
                                                turno = t
                                                actualizar_ventana(ventana,turno)
                    if ganador:
                        gano(turno)

main()
