from manim import *
import numpy as np


class VerletSMRScene(Scene):
    """Animacion didactica del metodo de Verlet para un sistema masa-resorte-amortiguador."""

    def construct(self):
        self.camera.background_color = "#101418"

        self.presentar_titulo()
        self.presentar_modelo_fisico()
        self.despejar_aceleracion()
        self.presentar_taylor()
        self.sumar_expansiones()
        self.formula_verlet()
        self.primer_paso_euler()
        self.simulacion_verlet()

    def mostrar_paso(self, titulo_texto, ecuaciones, colores=None, escala=0.85):
        """Muestra un bloque ordenado con titulo y ecuaciones centradas."""
        titulo = Text(titulo_texto, font_size=34, color=BLUE_C)
        titulo.to_edge(UP)

        grupo_ecuaciones = VGroup()
        for indice, tex in enumerate(ecuaciones):
            ecuacion = MathTex(tex, font_size=42)
            if colores and indice in colores:
                for fragmento, color in colores[indice]:
                    ecuacion.set_color_by_tex(fragmento, color)
            grupo_ecuaciones.add(ecuacion)

        grupo_ecuaciones.arrange(DOWN, buff=0.55)
        grupo_ecuaciones.scale(escala)
        grupo_ecuaciones.move_to(ORIGIN)

        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.6)
        self.play(LaggedStart(*[Write(eq) for eq in grupo_ecuaciones], lag_ratio=0.25), run_time=2.0)
        self.wait(1.2)
        self.play(FadeOut(VGroup(titulo, grupo_ecuaciones), shift=UP * 0.15), run_time=0.7)

    def presentar_titulo(self):
        titulo = Text("Metodo de Verlet", font_size=56, color=BLUE_C)
        subtitulo = Text("Sistema masa-resorte-amortiguador", font_size=30, color=GRAY_B)
        subtitulo.next_to(titulo, DOWN, buff=0.35)

        self.play(FadeIn(titulo, scale=0.95), FadeIn(subtitulo, shift=UP * 0.2), run_time=1.2)
        self.wait(1.0)
        self.play(FadeOut(VGroup(titulo, subtitulo), shift=UP * 0.2), run_time=0.7)

    def presentar_modelo_fisico(self):
        self.mostrar_paso(
            "1. Modelo fisico",
            [
                r"m\,x''(t)+b\,x'(t)+k\,x(t)=F(t)",
                r"\text{masa}+\text{amortiguamiento}+\text{resorte}=\text{fuerza externa}",
            ],
            colores={
                0: [
                    ("m", YELLOW),
                    ("b", ORANGE),
                    ("k", GREEN),
                    ("F", BLUE_C),
                ]
            },
        )

    def despejar_aceleracion(self):
        self.mostrar_paso(
            "2. Aceleracion instantanea",
            [
                r"a(t)=x''(t)",
                r"a(t)=\frac{F(t)-b\,v(t)-k\,x(t)}{m}",
            ],
            colores={
                1: [
                    ("F(t)", BLUE_C),
                    ("b", ORANGE),
                    ("v(t)", RED_C),
                    ("k", GREEN),
                    ("x(t)", YELLOW),
                    ("m", YELLOW),
                ]
            },
        )

    def presentar_taylor(self):
        self.mostrar_paso(
            "3. Expansiones de Taylor",
            [
                r"x(t+\Delta t)=x(t)+v(t)\Delta t+\frac{1}{2}a(t)\Delta t^2+\cdots",
                r"x(t-\Delta t)=x(t)-v(t)\Delta t+\frac{1}{2}a(t)\Delta t^2-\cdots",
            ],
            colores={
                0: [("+v(t)", RED_C), ("a(t)", BLUE_C)],
                1: [("-v(t)", RED_C), ("a(t)", BLUE_C)],
            },
            escala=0.78,
        )

    def sumar_expansiones(self):
        titulo = Text("4. Sumamos y se cancela la velocidad", font_size=32, color=BLUE_C)
        titulo.to_edge(UP)

        adelante = MathTex(
            r"x(t+\Delta t)=x(t)",
            r"+v(t)\Delta t",
            r"+\frac{1}{2}a(t)\Delta t^2+\cdots",
            font_size=36,
        )
        atras = MathTex(
            r"x(t-\Delta t)=x(t)",
            r"-v(t)\Delta t",
            r"+\frac{1}{2}a(t)\Delta t^2-\cdots",
            font_size=36,
        )
        suma = MathTex(
            r"x(t+\Delta t)+x(t-\Delta t)=2x(t)+a(t)\Delta t^2",
            font_size=40,
        )
        cancelacion = MathTex(
            r"+v(t)\Delta t\;-\;v(t)\Delta t=0",
            font_size=38,
            color=RED_C,
        )

        adelante[1].set_color(RED_C)
        atras[1].set_color(RED_C)
        suma.set_color_by_tex("a(t)", BLUE_C)

        ecuaciones = VGroup(adelante, atras).arrange(DOWN, buff=0.35)
        ecuaciones.move_to(UP * 0.75)
        cancelacion.next_to(ecuaciones, DOWN, buff=0.55)
        suma.next_to(cancelacion, DOWN, buff=0.65)

        marcas = VGroup(
            Cross(adelante[1].copy(), stroke_color=RED_C, stroke_width=6),
            Cross(atras[1].copy(), stroke_color=RED_C, stroke_width=6),
        )

        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.6)
        self.play(Write(adelante), Write(atras), run_time=1.5)
        self.play(Create(marcas), Write(cancelacion), run_time=1.2)
        self.play(Write(suma), run_time=1.1)
        self.wait(1.3)
        self.play(FadeOut(VGroup(titulo, ecuaciones, marcas, cancelacion, suma), shift=UP * 0.15), run_time=0.7)

    def formula_verlet(self):
        titulo = Text("5. Formula de Verlet", font_size=34, color=BLUE_C)
        titulo.to_edge(UP)

        ecuacion_intermedia = MathTex(
            r"x(t+\Delta t)+x(t-\Delta t)=2x(t)+a(t)\Delta t^2",
            font_size=38,
        )
        ecuacion_final = MathTex(
            r"x(t+\Delta t)=2x(t)-x(t-\Delta t)+a(t)\Delta t^2",
            font_size=42,
        )
        ecuacion_final.set_color_by_tex("x(t+\\Delta t)", YELLOW)
        ecuacion_final.set_color_by_tex("a(t)", BLUE_C)

        grupo = VGroup(ecuacion_intermedia, ecuacion_final).arrange(DOWN, buff=0.75).move_to(ORIGIN)

        self.play(FadeIn(titulo, shift=DOWN * 0.2), Write(ecuacion_intermedia), run_time=1.1)
        self.play(TransformMatchingTex(ecuacion_intermedia.copy(), ecuacion_final), run_time=1.3)
        self.wait(1.4)
        self.play(FadeOut(VGroup(titulo, grupo), shift=UP * 0.15), run_time=0.7)

    def primer_paso_euler(self):
        self.mostrar_paso(
            "6. Primer paso con Euler",
            [
                r"x_1=x_0+v_0\Delta t+\frac{1}{2}a_0\Delta t^2",
                r"a_0=\frac{F_0-b\,v_0-k\,x_0}{m}",
                r"\text{Despues, Verlet usa } x_{n-1}\text{ y }x_n\text{ para calcular }x_{n+1}.",
            ],
            colores={
                0: [("x_1", YELLOW), ("v_0", RED_C), ("a_0", BLUE_C)],
                1: [("F_0", BLUE_C), ("b", ORANGE), ("k", GREEN)],
            },
            escala=0.8,
        )

    def simulacion_verlet(self):
        titulo = Text("7. Simulacion con Verlet", font_size=34, color=BLUE_C)
        titulo.to_edge(UP)

        # Parametros del sistema masa-resorte-amortiguador.
        masa = 1.0
        amortiguamiento = 0.35
        constante_resorte = 5.0
        dt = 0.045
        pasos = 170
        x0 = 1.45
        v0 = 0.0

        posiciones, velocidades, aceleraciones = self.calcular_verlet(
            masa,
            amortiguamiento,
            constante_resorte,
            dt,
            pasos,
            x0,
            v0,
        )

        indice = ValueTracker(0)
        origen_pared = LEFT * 4.2 + DOWN * 0.35
        escala_x = 1.15

        pared = self.crear_pared(origen_pared)
        piso = Line(LEFT * 4.55 + DOWN * 1.28, RIGHT * 4.55 + DOWN * 1.28, color=GRAY_D)
        guia = DashedLine(LEFT * 3.4 + DOWN * 0.35, RIGHT * 3.6 + DOWN * 0.35, color=GRAY_E, dash_length=0.15)
        equilibrio = DashedLine(DOWN * 1.1, UP * 0.35, color=GREEN_C, dash_length=0.12).shift(DOWN * 0.35)
        etiqueta_equilibrio = Text("equilibrio", font_size=20, color=GREEN_C).next_to(equilibrio, DOWN, buff=0.1)

        def obtener_indice():
            return int(np.clip(round(indice.get_value()), 0, len(posiciones) - 1))

        def centro_masa():
            return RIGHT * (posiciones[obtener_indice()] * escala_x) + DOWN * 0.35

        resorte = always_redraw(
            lambda: self.crear_resorte(origen_pared + RIGHT * 0.18, centro_masa() + LEFT * 0.47)
        )
        bloque = always_redraw(
            lambda: RoundedRectangle(
                width=0.92,
                height=0.72,
                corner_radius=0.08,
                fill_color=YELLOW,
                fill_opacity=0.9,
                stroke_color=WHITE,
                stroke_width=2,
            ).move_to(centro_masa())
        )
        sombra = always_redraw(
            lambda: Ellipse(
                width=0.85,
                height=0.12,
                fill_color=BLACK,
                fill_opacity=0.35,
                stroke_opacity=0,
            ).move_to(centro_masa() + DOWN * 0.46)
        )

        formula = MathTex(
            r"x_{n+1}=2x_n-x_{n-1}+a_n\Delta t^2",
            font_size=34,
        ).to_corner(UL).shift(DOWN * 0.75)
        formula.set_color_by_tex("a_n", BLUE_C)

        parametros = MathTex(
            r"m=1,\quad b=0.35,\quad k=5,\quad F(t)=0",
            font_size=30,
        ).next_to(formula, DOWN, aligned_edge=LEFT, buff=0.25)

        n_valor = Integer(0, font_size=28)
        x_valor = DecimalNumber(posiciones[0], num_decimal_places=2, include_sign=True, font_size=28)
        v_valor = DecimalNumber(velocidades[0], num_decimal_places=2, include_sign=True, font_size=28)
        a_valor = DecimalNumber(aceleraciones[0], num_decimal_places=2, include_sign=True, font_size=28)

        n_valor.add_updater(lambda mob: mob.set_value(obtener_indice()))
        x_valor.add_updater(lambda mob: mob.set_value(posiciones[obtener_indice()]))
        v_valor.add_updater(lambda mob: mob.set_value(velocidades[obtener_indice()]))
        a_valor.add_updater(lambda mob: mob.set_value(aceleraciones[obtener_indice()]))

        lectura = VGroup(
            VGroup(MathTex(r"n=", font_size=28), n_valor).arrange(RIGHT, buff=0.08),
            VGroup(MathTex(r"x_n=", font_size=28), x_valor).arrange(RIGHT, buff=0.08),
            VGroup(MathTex(r"v_n\approx", font_size=28), v_valor).arrange(RIGHT, buff=0.08),
            VGroup(MathTex(r"a_n=", font_size=28), a_valor).arrange(RIGHT, buff=0.08),
        )
        lectura.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        lectura.to_corner(UR).shift(DOWN * 0.8)

        escena_mecanica = VGroup(pared, piso, guia, equilibrio, etiqueta_equilibrio, sombra, resorte, bloque)

        self.play(FadeIn(titulo, shift=DOWN * 0.2), run_time=0.6)
        self.play(
            FadeIn(escena_mecanica, shift=UP * 0.2),
            Write(formula),
            Write(parametros),
            FadeIn(lectura),
            run_time=1.5,
        )
        self.play(indice.animate.set_value(len(posiciones) - 1), run_time=8.0, rate_func=linear)
        self.wait(0.8)
        self.play(
            FadeOut(VGroup(titulo, escena_mecanica, formula, parametros, lectura), shift=UP * 0.15),
            run_time=0.9,
        )

    def calcular_verlet(self, masa, amortiguamiento, constante_resorte, dt, pasos, x0, v0):
        """Calcula posiciones usando Verlet con velocidad aproximada por diferencia finita."""
        posiciones = np.zeros(pasos)
        velocidades = np.zeros(pasos)
        aceleraciones = np.zeros(pasos)

        def fuerza_externa(_tiempo):
            return 0.0

        def aceleracion(x, v, tiempo):
            return (fuerza_externa(tiempo) - amortiguamiento * v - constante_resorte * x) / masa

        posiciones[0] = x0
        velocidades[0] = v0
        aceleraciones[0] = aceleracion(posiciones[0], velocidades[0], 0.0)

        # Primer paso: Taylor/Euler para obtener x_1.
        posiciones[1] = posiciones[0] + velocidades[0] * dt + 0.5 * aceleraciones[0] * dt**2
        velocidades[1] = (posiciones[1] - posiciones[0]) / dt
        aceleraciones[1] = aceleracion(posiciones[1], velocidades[1], dt)

        # Pasos siguientes: Verlet. El amortiguamiento entra por v_n aproximada.
        for n in range(1, pasos - 1):
            tiempo = n * dt
            velocidades[n] = (posiciones[n] - posiciones[n - 1]) / dt
            aceleraciones[n] = aceleracion(posiciones[n], velocidades[n], tiempo)
            posiciones[n + 1] = 2 * posiciones[n] - posiciones[n - 1] + aceleraciones[n] * dt**2

        velocidades[-1] = (posiciones[-1] - posiciones[-2]) / dt
        aceleraciones[-1] = aceleracion(posiciones[-1], velocidades[-1], (pasos - 1) * dt)
        return posiciones, velocidades, aceleraciones

    def crear_pared(self, origen):
        """Crea una pared fija desde donde se ancla el resorte."""
        pared = VGroup()
        pared.add(Line(origen + UP * 1.0, origen + DOWN * 1.0, color=GRAY_B, stroke_width=5))

        for desplazamiento in np.linspace(-0.9, 0.9, 7):
            pared.add(
                Line(
                    origen + LEFT * 0.45 + DOWN * desplazamiento,
                    origen + DOWN * desplazamiento + UP * 0.28,
                    color=GRAY_C,
                    stroke_width=2,
                )
            )
        return pared

    def crear_resorte(self, inicio, fin, vueltas=12, amplitud=0.22):
        """Dibuja un resorte zigzagueante entre dos puntos."""
        longitud = fin[0] - inicio[0]
        puntos = [inicio]

        for i in range(1, vueltas * 2):
            alfa = i / (vueltas * 2)
            x = inicio[0] + longitud * alfa
            y = inicio[1] + (amplitud if i % 2 else -amplitud)
            puntos.append(np.array([x, y, 0.0]))

        puntos.append(fin)
        resorte = VMobject(color=BLUE_C, stroke_width=4)
        resorte.set_points_as_corners(puntos)
        return resorte
