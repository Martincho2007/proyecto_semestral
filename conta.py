import pygame
import sys

def main():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Agua Limpia - Crónica Trágica")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont(None, 28)

    # Cargar sonidos de voz por personaje
    sonidos_voz = {
        "Sukuna": pygame.mixer.Sound("asriel_voice.wav"),
        "Martín": pygame.mixer.Sound("sans_voice_1.wav"),
        "Dailyn": pygame.mixer.Sound("toriel_voice.wav"),
    }

    estado = {
        "confianza_comunidad": 0,
        "accion_urgente": 0,
        "errores": 0
    }

    escenas_imagenes = [
        pygame.transform.smoothscale(pygame.image.load("imagen-inicio.jfif").convert(), (ANCHO, ALTO)),
        pygame.transform.smoothscale(pygame.image.load("inicio-lancha.jpg").convert(), (ANCHO, ALTO)),
        pygame.transform.smoothscale(pygame.image.load("imagen-desarrollo.jpg").convert(), (ANCHO, ALTO)),
        pygame.transform.smoothscale(pygame.image.load("desarrollo-2.jpg").convert(), (ANCHO, ALTO)),
        pygame.transform.smoothscale(pygame.image.load("zona-industrial.jfif").convert(), (ANCHO, ALTO)),
        pygame.transform.smoothscale(pygame.image.load("agua-negra.jfif").convert(), (ANCHO, ALTO))
    ]

    retratos = {
        "Sukuna": pygame.transform.scale(pygame.image.load("sukuna_inicio.png").convert_alpha(), (300, 360)),
        "Martín": pygame.transform.scale(pygame.image.load("martin.png").convert_alpha(), (300, 360)),
        "Dailyn": pygame.transform.scale(pygame.image.load("dailyn.png").convert_alpha(), (300, 360)),
    }

    escenas = [
        {
            "imagen": 0,
            "personaje": "Sukuna",
            "texto": "El informe es peor de lo esperado. Químicos ilegales están en el agua.",
            "opciones": [
                {"texto": "1. Exponer públicamente a la empresa", "efecto": lambda: estado.update({"confianza_comunidad": estado["confianza_comunidad"] + 30})},
                {"texto": "2. Investigar en secreto primero", "efecto": lambda: estado.update({"accion_urgente": estado["accion_urgente"] + 1})}
            ]
        },
        {
            "imagen": 1,
            "personaje": "Martín",
            "texto": "Un niño enfermó por beber del río. No hay tiempo.",
            "opciones": [
                {"texto": "1. Contener químicamente la zona", "efecto": lambda: estado.update({"accion_urgente": estado["accion_urgente"] + 1})},
                {"texto": "2. Llamar a los medios", "efecto": lambda: estado.update({"confianza_comunidad": estado["confianza_comunidad"] + 20})}
            ]
        },
        {
            "imagen": 2,
            "personaje": "Dailyn",
            "texto": "La comunidad culpa al equipo por no actuar antes.",
            "opciones": [
                {"texto": "1. Asumir responsabilidad", "efecto": lambda: estado.update({"confianza_comunidad": estado["confianza_comunidad"] + 30})},
                {"texto": "2. Culpar al gobierno", "efecto": lambda: estado.update({"errores": estado["errores"] + 1})}
            ]
        },
        {
            "imagen": 3,
            "personaje": "Sukuna",
            "texto": "Los peces están muriendo río abajo. ¿Actuamos sin permiso?",
            "opciones": [
                {"texto": "1. Usar drones y lanzar neutralizante", "efecto": lambda: estado.update({"accion_urgente": estado["accion_urgente"] + 1})},
                {"texto": "2. Esperar al consejo ambiental", "efecto": lambda: estado.update({"errores": estado["errores"] + 1})}
            ]
        },
        {
            "imagen": 4,
            "personaje": "Martín",
            "texto": "La empresa ha cerrado el acceso al río. Dicen que es una 'zona de seguridad'.",
            "opciones": [
                {"texto": "1. Entrar a escondidas con ayuda local", "efecto": lambda: estado.update({"confianza_comunidad": estado["confianza_comunidad"] + 20, "accion_urgente": estado["accion_urgente"] + 1})},
                {"texto": "2. Esperar una orden judicial", "efecto": lambda: estado.update({"errores": estado["errores"] + 1})}
            ]
        },
        {
            "imagen": 5,
            "personaje": "Dailyn",
            "texto": "El agua negra llegó al pueblo. Los niños están en peligro.",
            "opciones": [
                {"texto": "1. Evacuar por cuenta propia", "efecto": lambda: estado.update({"accion_urgente": estado["accion_urgente"] + 1})},
                {"texto": "2. Buscar ayuda del gobierno", "efecto": lambda: estado.update({"errores": estado["errores"] + 1})}
            ]
        },
        {
            "imagen": 0,
            "personaje": "Sukuna",
            "texto": "Hicimos lo que pudimos... pero no sé si fue suficiente.",
            "opciones": None
        }
    ]

    finales = {
        "malo": "El desastre se expandió. La comunidad te culpa. Hay muertes y desplazamiento forzado.",
        "bueno": "Salvaste a parte del pueblo. Pero hubo pérdidas irreparables, y la flora local desapareció.",
        "verdadero": "Actuaste con firmeza y humanidad. El río fue restaurado, pero solo tras un doloroso sacrificio."
    }

    def evaluar_final():
        if estado["errores"] >= 3:
            return "malo"
        elif estado["accion_urgente"] >= 3 and estado["confianza_comunidad"] >= 50:
            return "verdadero"
        else:
            return "bueno"

    def mostrar_dialogo_typewriter(texto, y, personaje, saltar=False):
        lineas = []
        while len(texto) > 60:
            corte = texto[:60].rfind(" ")
            if corte == -1: corte = 60
            lineas.append(texto[:corte])
            texto = texto[corte+1:]
        lineas.append(texto)
        for i, linea in enumerate(lineas):
            render_text = ""
            for letra in linea:
                render_text += letra
                render = fuente.render(render_text, True, (255, 255, 255))
                pantalla.fill((0, 0, 0), (40, y + i * 28, 720, 28))  # Limpia línea
                pantalla.blit(render, (40, y + i * 28))
                if not saltar and letra.strip() != "":
                    sonidos_voz[personaje].play()
                pygame.display.flip()
                if not saltar:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            sonidos_voz[personaje].stop()
                            return True  # Saltar animación si se presiona una tecla
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    pygame.time.wait(20)
            sonidos_voz[personaje].stop()
        return False

    def dibujar_cuadro_dialogo():
        alto = 150
        cuadro = pygame.Surface((ANCHO - 40, alto))
        cuadro.set_alpha(200)
        cuadro.fill((0, 0, 0))
        pantalla.blit(cuadro, (20, ALTO - alto - 20))

    escena_actual = 0
    en_juego = True
    mostrar_typewriter = True

    while en_juego:
        escena = escenas[escena_actual]
        pantalla.blit(escenas_imagenes[escena["imagen"]], (0, 0))

        if escena["personaje"] in retratos:
            pantalla.blit(retratos[escena["personaje"]], (20, ALTO - 360 - 20))

        dibujar_cuadro_dialogo()
        # Nombre del personaje (sin efecto typewriter)
        render_nombre = fuente.render(f"{escena['personaje']}:", True, (255, 255, 255))
        pantalla.blit(render_nombre, (40, ALTO - 140))

        # Texto principal con efecto typewriter
        if mostrar_typewriter:
            saltar = mostrar_dialogo_typewriter(escena["texto"], ALTO - 110, escena["personaje"])
            mostrar_typewriter = False if not saltar else True
        else:
            # Si ya se mostró, muestra el texto completo sin animación ni sonido
            lineas = []
            texto = escena["texto"]
            while len(texto) > 60:
                corte = texto[:60].rfind(" ")
                if corte == -1: corte = 60
                lineas.append(texto[:corte])
                texto = texto[corte+1:]
            lineas.append(texto)
            for i, linea in enumerate(lineas):
                render = fuente.render(linea, True, (255, 255, 255))
                pantalla.blit(render, (40, ALTO - 110 + i * 28))

        # Opciones centradas y con borde blanco
        if escena["opciones"]:
            num_opciones = len(escena["opciones"])
            for i, opcion in enumerate(escena["opciones"]):
                texto = fuente.render(opcion["texto"], True, (0, 0, 0))
                # Borde blanco
                for dx in [-2, 0, 2]:
                    for dy in [-2, 0, 2]:
                        if dx != 0 or dy != 0:
                            rect = texto.get_rect(center=(ANCHO // 2 + dx, ALTO - 40 + i * 30 + dy))
                            pantalla.blit(fuente.render(opcion["texto"], True, (255, 255, 255)), rect)
                rect = texto.get_rect(center=(ANCHO // 2, ALTO - 40 + i * 30))
                pantalla.blit(texto, rect)

        avanzar = False
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_juego = False
            elif evento.type == pygame.KEYDOWN:
                # Detener cualquier sonido de voz cuando se avanza de diálogo
                for snd in sonidos_voz.values():
                    snd.stop()
                if escena["opciones"]:
                    if evento.key == pygame.K_1:
                        escena["opciones"][0]["efecto"]()
                        escena_actual += 1
                        mostrar_typewriter = True
                        avanzar = True
                    elif evento.key == pygame.K_2 and len(escena["opciones"]) > 1:
                        escena["opciones"][1]["efecto"]()
                        escena_actual += 1
                        mostrar_typewriter = True
                        avanzar = True
                else:
                    escena_actual += 1
                    mostrar_typewriter = True
                    avanzar = True

                if escena_actual >= len(escenas):
                    final = evaluar_final()
                    pantalla.fill((0, 0, 0))
                    render = fuente.render("FIN DEL JUEGO", True, (255, 255, 255))
                    pantalla.blit(render, (ANCHO // 2 - render.get_width() // 2, 200))
                    lineas = []
                    texto = finales[final]
                    while len(texto) > 60:
                        corte = texto[:60].rfind(" ")
                        if corte == -1: corte = 60
                        lineas.append(texto[:corte])
                        texto = texto[corte+1:]
                    lineas.append(texto)
                    for i, linea in enumerate(lineas):
                        render = fuente.render(linea, True, (255, 255, 255))
                        pantalla.blit(render, (40, 240 + i * 28))
                    render = fuente.render("Presiona ESC para salir o R para reiniciar", True, (255, 255, 255))
                    pantalla.blit(render, (40, 300))
                    pygame.display.flip()
                    esperando = True
                    while esperando:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                esperando = False
                                en_juego = False
                            elif e.type == pygame.KEYDOWN:
                                if e.key == pygame.K_ESCAPE:
                                    esperando = False
                                    en_juego = False
                                elif e.key == pygame.K_r:
                                    estado = {"confianza_comunidad": 0, "accion_urgente": 0, "errores": 0}
                                    escena_actual = 0
                                    mostrar_typewriter = True
                                    esperando = False

        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()