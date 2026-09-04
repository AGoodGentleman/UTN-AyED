from __future__ import annotations

import argparse
import math
import textwrap
import webbrowser
from dataclasses import dataclass
from html import escape
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # SVG output still works without Pillow.
    Image = None
    ImageDraw = None
    ImageFont = None


OUT_DIR = Path(__file__).resolve().parent / "salida"

TEXT = "#1f2933"
MUTED = "#52616b"
LINE = "#40576b"
BLUE = "#e8f2f7"
BLUE_2 = "#dcecf3"
CREAM = "#fbf7ea"
WHITE = "#ffffff"
GRID = "#eef3f6"


class PngRenderer:
    def __init__(self, width: int, height: int) -> None:
        if Image is None or ImageDraw is None or ImageFont is None:
            raise RuntimeError("Pillow is not available")
        self.image = Image.new("RGB", (width, height), WHITE)
        self.draw = ImageDraw.Draw(self.image)
        self.font_dir = Path("C:/Windows/Fonts")

    def font(self, size: int, weight: str = "400", italic: bool = False):
        if italic:
            candidates = ["segoeuii.ttf", "ariali.ttf"]
        elif int(weight) >= 600:
            candidates = ["segoeuib.ttf", "arialbd.ttf"]
        else:
            candidates = ["segoeui.ttf", "arial.ttf"]
        for candidate in candidates:
            path = self.font_dir / candidate
            if path.exists():
                return ImageFont.truetype(str(path), size)
        return ImageFont.load_default()

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        fill: str,
        stroke: str,
        width: float,
        rx: float,
    ) -> None:
        xy = [x, y, x + w, y + h]
        outline = stroke if width > 0 else None
        if rx:
            self.draw.rounded_rectangle(xy, radius=rx, fill=fill, outline=outline, width=max(1, int(width)))
        else:
            self.draw.rectangle(xy, fill=fill, outline=outline, width=max(1, int(width)))

    def ellipse(
        self,
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        *,
        fill: str,
        stroke: str,
        width: float,
    ) -> None:
        self.draw.ellipse(
            [cx - rx, cy - ry, cx + rx, cy + ry],
            fill=fill,
            outline=stroke,
            width=max(1, int(width)),
        )

    def text(
        self,
        x: float,
        y: float,
        content: str,
        *,
        size: int,
        weight: str,
        anchor: str,
        fill: str,
        italic: bool,
    ) -> None:
        font = self.font(size, weight, italic)
        bbox = self.draw.textbbox((0, 0), content, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        if anchor == "middle":
            tx = x - text_w / 2
        elif anchor == "end":
            tx = x - text_w
        else:
            tx = x
        ty = y - text_h * 0.78
        self.draw.text((tx, ty), content, fill=fill, font=font)

    def line(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        *,
        stroke: str,
        width: float,
        dash: bool,
        marker_end: str | None,
    ) -> None:
        if dash:
            self._dashed_segment(p1, p2, stroke, width)
        else:
            self.draw.line([p1, p2], fill=stroke, width=max(1, int(width)))
        if marker_end:
            self._marker(p1, p2, stroke, marker_end)

    def polyline(
        self,
        points: list[tuple[float, float]],
        *,
        stroke: str,
        width: float,
        dash: bool,
        marker_end: str | None,
    ) -> None:
        for p1, p2 in zip(points, points[1:]):
            self.line(p1, p2, stroke=stroke, width=width, dash=dash, marker_end=None)
        if marker_end and len(points) >= 2:
            self._marker(points[-2], points[-1], stroke, marker_end)

    def polygon(
        self,
        points: list[tuple[float, float]],
        *,
        fill: str,
        stroke: str,
        width: float,
    ) -> None:
        self.draw.polygon(points, fill=fill, outline=stroke)
        if width > 1:
            self.draw.line(points + [points[0]], fill=stroke, width=max(1, int(width)))

    def _dashed_segment(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        stroke: str,
        width: float,
        dash_len: float = 12,
        gap_len: float = 9,
    ) -> None:
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            return
        ux = dx / length
        uy = dy / length
        pos = 0.0
        while pos < length:
            end = min(pos + dash_len, length)
            self.draw.line(
                [(x1 + ux * pos, y1 + uy * pos), (x1 + ux * end, y1 + uy * end)],
                fill=stroke,
                width=max(1, int(width)),
            )
            pos += dash_len + gap_len

    def _marker(self, p1: tuple[float, float], p2: tuple[float, float], stroke: str, marker: str) -> None:
        x1, y1 = p1
        x2, y2 = p2
        angle = math.atan2(y2 - y1, x2 - x1)
        ux = math.cos(angle)
        uy = math.sin(angle)
        px = -uy
        py = ux
        if marker == "arrow":
            size = 17
            base_x = x2 - ux * size
            base_y = y2 - uy * size
            points = [(x2, y2), (base_x + px * 7, base_y + py * 7), (base_x - px * 7, base_y - py * 7)]
            self.draw.polygon(points, fill=stroke)
        elif marker == "openTriangle":
            size = 22
            base_x = x2 - ux * size
            base_y = y2 - uy * size
            points = [(x2, y2), (base_x + px * 10, base_y + py * 10), (base_x - px * 10, base_y - py * 10)]
            self.draw.polygon(points, fill=WHITE, outline=stroke)

    def save(self, path: Path) -> None:
        self.image.save(path)


@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2

    @property
    def left(self) -> tuple[float, float]:
        return (self.x, self.cy)

    @property
    def right(self) -> tuple[float, float]:
        return (self.x + self.w, self.cy)

    @property
    def top(self) -> tuple[float, float]:
        return (self.cx, self.y)

    @property
    def bottom(self) -> tuple[float, float]:
        return (self.cx, self.y + self.h)


class Svg:
    def __init__(self, width: int, height: int, title: str) -> None:
        self.width = width
        self.height = height
        self.title = title
        self.items: list[str] = []
        try:
            self.png: PngRenderer | None = PngRenderer(width, height)
        except RuntimeError:
            self.png = None

    def add(self, raw: str) -> None:
        self.items.append(raw)

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        fill: str = WHITE,
        stroke: str = LINE,
        width: float = 2.0,
        rx: float = 0,
        dash: bool = False,
    ) -> None:
        dash_attr = ' stroke-dasharray="10 8"' if dash else ""
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"{dash_attr}/>'
        )
        if self.png and not dash:
            self.png.rect(x, y, w, h, fill=fill, stroke=stroke, width=width, rx=rx)

    def ellipse(
        self,
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        *,
        fill: str = WHITE,
        stroke: str = LINE,
        width: float = 2.4,
    ) -> None:
        self.add(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
        )
        if self.png:
            self.png.ellipse(cx, cy, rx, ry, fill=fill, stroke=stroke, width=width)

    def line(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        *,
        stroke: str = LINE,
        width: float = 2.2,
        dash: bool = False,
        marker_end: str | None = None,
    ) -> None:
        dash_attr = ' stroke-dasharray="10 8"' if dash else ""
        marker = f' marker-end="url(#{marker_end})"' if marker_end else ""
        self.add(
            f'<line x1="{p1[0]}" y1="{p1[1]}" x2="{p2[0]}" y2="{p2[1]}" '
            f'stroke="{stroke}" stroke-width="{width}" fill="none"{dash_attr}{marker}/>'
        )
        if self.png:
            self.png.line(p1, p2, stroke=stroke, width=width, dash=dash, marker_end=marker_end)

    def polyline(
        self,
        points: list[tuple[float, float]],
        *,
        stroke: str = LINE,
        width: float = 2.2,
        dash: bool = False,
        marker_end: str | None = None,
    ) -> None:
        dash_attr = ' stroke-dasharray="10 8"' if dash else ""
        marker = f' marker-end="url(#{marker_end})"' if marker_end else ""
        data = " ".join(f"{x},{y}" for x, y in points)
        self.add(
            f'<polyline points="{data}" fill="none" stroke="{stroke}" '
            f'stroke-width="{width}"{dash_attr}{marker}/>'
        )
        if self.png:
            self.png.polyline(points, stroke=stroke, width=width, dash=dash, marker_end=marker_end)

    def polygon(
        self,
        points: list[tuple[float, float]],
        *,
        fill: str,
        stroke: str = LINE,
        width: float = 2.2,
    ) -> None:
        data = " ".join(f"{x},{y}" for x, y in points)
        self.add(
            f'<polygon points="{data}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{width}"/>'
        )
        if self.png:
            self.png.polygon(points, fill=fill, stroke=stroke, width=width)

    def text(
        self,
        x: float,
        y: float,
        content: str,
        *,
        size: int = 18,
        weight: str = "400",
        anchor: str = "middle",
        fill: str = TEXT,
        italic: bool = False,
    ) -> None:
        font_style = "italic" if italic else "normal"
        self.add(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-size="{size}" font-weight="{weight}" '
            f'font-style="{font_style}" fill="{fill}">{escape(content)}</text>'
        )
        if self.png:
            self.png.text(x, y, content, size=size, weight=weight, anchor=anchor, fill=fill, italic=italic)

    def multiline(
        self,
        x: float,
        y: float,
        lines: list[str],
        *,
        size: int = 18,
        line_height: int = 22,
        anchor: str = "middle",
        fill: str = TEXT,
        weight: str = "400",
    ) -> None:
        if not lines:
            return
        start_y = y - ((len(lines) - 1) * line_height) / 2
        tspans = []
        for i, line in enumerate(lines):
            dy = 0 if i == 0 else line_height
            tspans.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
        self.add(
            f'<text x="{x}" y="{start_y}" text-anchor="{anchor}" '
            f'font-size="{size}" font-weight="{weight}" fill="{fill}">'
            + "".join(tspans)
            + "</text>"
        )
        if self.png:
            for i, line in enumerate(lines):
                self.png.text(
                    x,
                    start_y + i * line_height,
                    line,
                    size=size,
                    weight=weight,
                    anchor=anchor,
                    fill=fill,
                    italic=False,
                )

    def label(self, x: float, y: float, content: str, *, size: int = 18) -> None:
        pad_x = 8
        pad_y = 4
        approx_w = max(28, len(content) * size * 0.55)
        self.rect(
            x - approx_w / 2 - pad_x,
            y - size + pad_y,
            approx_w + pad_x * 2,
            size + pad_y * 2,
            fill=WHITE,
            stroke=WHITE,
            width=0,
            rx=5,
        )
        self.text(x, y, content, size=size, fill=TEXT)

    def save(self, path: Path) -> None:
        path.write_text(self.render(), encoding="utf-8")
        if self.png:
            self.png.save(path.with_suffix(".png"))

    def render(self) -> str:
        body = "\n".join(self.items)
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">
<title>{escape(self.title)}</title>
<defs>
  <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth">
    <path d="M 0 0 L 12 6 L 0 12 z" fill="{LINE}"/>
  </marker>
  <marker id="openTriangle" markerWidth="18" markerHeight="18" refX="16" refY="9" orient="auto" markerUnits="strokeWidth">
    <path d="M 1 1 L 17 9 L 1 17 z" fill="{WHITE}" stroke="{LINE}" stroke-width="2"/>
  </marker>
  <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#28465c" flood-opacity="0.15"/>
  </filter>
  <style>
    text {{ font-family: "Segoe UI", Arial, sans-serif; }}
  </style>
</defs>
<rect width="100%" height="100%" fill="{WHITE}"/>
{body}
</svg>
'''


def wrap(label: str, width: int) -> list[str]:
    lines: list[str] = []
    for part in label.split("\n"):
        wrapped = textwrap.wrap(part, width=width, break_long_words=False)
        lines.extend(wrapped or [""])
    return lines


def title(svg: Svg, main: str, subtitle: str | None = None) -> None:
    svg.text(svg.width / 2, 46, main, size=30, weight="700")
    if subtitle:
        svg.text(svg.width / 2, 76, subtitle, size=17, fill=MUTED)


def use_case(svg: Svg, cx: float, cy: float, w: float, h: float, label: str, *, fill: str = WHITE) -> Box:
    box = Box(cx - w / 2, cy - h / 2, w, h)
    svg.ellipse(cx, cy, w / 2, h / 2, fill=fill)
    svg.multiline(cx, cy + 7, wrap(label, 26), size=20, line_height=24)
    return box


def actor(svg: Svg, x: float, y: float, label: str, *, w: float = 220, h: float = 190) -> Box:
    box = Box(x, y, w, h)
    head_cy = y + 28
    body_top = y + 52
    body_bottom = y + 104
    svg.ellipse(box.cx, head_cy, 21, 21, fill=WHITE, stroke=LINE, width=2.3)
    svg.line((box.cx, body_top), (box.cx, body_bottom), width=2.3)
    svg.line((box.cx - 36, y + 72), (box.cx + 36, y + 72), width=2.3)
    svg.line((box.cx, body_bottom), (box.cx - 34, y + 138), width=2.3)
    svg.line((box.cx, body_bottom), (box.cx + 34, y + 138), width=2.3)
    svg.multiline(box.cx, y + 174, wrap(label, 22), size=19, line_height=22)
    return box


def entity(svg: Svg, x: float, y: float, w: float, name: str, attrs: list[str], *, fill: str = "#f7fafc") -> Box:
    line_h = 20
    header_h = 40
    h = header_h + 28 + line_h * len(attrs)
    box = Box(x, y, w, h)
    svg.rect(x, y, w, h, fill=fill, stroke=LINE, width=2.1, rx=16)
    svg.rect(x, y, w, header_h, fill=BLUE_2, stroke=LINE, width=0, rx=16)
    svg.line((x, y + header_h), (x + w, y + header_h), width=2.0)
    svg.text(box.cx, y + 27, name, size=18, weight="700")
    for i, attr in enumerate(attrs):
        svg.text(x + 16, y + header_h + 26 + i * line_h, attr, size=16, anchor="start")
    return box


def uml_class(
    svg: Svg,
    x: float,
    y: float,
    w: float,
    name: str,
    attrs: list[str] | None = None,
    methods: list[str] | None = None,
    *,
    stereotype: str | None = None,
    fill: str = "#f7fafc",
    header_fill: str = BLUE_2,
) -> Box:
    attrs = attrs or []
    methods = methods or []
    line_h = 21
    header_h = 50 if stereotype else 36
    max_chars = max(24, int((w - 28) / 8.2))
    wrapped_attrs = [
        line
        for attr in attrs
        for line in textwrap.wrap(attr, width=max_chars, break_long_words=False, subsequent_indent="  ")
    ]
    wrapped_methods = [
        line
        for method in methods
        for line in textwrap.wrap(method, width=max_chars, break_long_words=False, subsequent_indent="  ")
    ]
    attrs_h = 14 + line_h * len(wrapped_attrs) if wrapped_attrs else 0
    methods_h = 14 + line_h * len(wrapped_methods) if wrapped_methods else 0
    h = header_h + attrs_h + methods_h
    box = Box(x, y, w, h)
    svg.rect(x, y, w, h, fill=fill, stroke=LINE, width=2.2, rx=16)
    svg.rect(x, y, w, header_h, fill=header_fill, stroke=LINE, width=0, rx=16)
    svg.line((x, y + header_h), (x + w, y + header_h), width=2.0)
    if stereotype:
        svg.text(box.cx, y + 20, f"<<{stereotype}>>", size=15)
        svg.text(box.cx, y + 40, name, size=18, weight="700")
    else:
        svg.text(box.cx, y + 24, name, size=18, weight="700")
    current_y = y + header_h
    for i, attr in enumerate(wrapped_attrs):
        svg.text(x + 14, current_y + 23 + i * line_h, attr, size=15, anchor="start")
    current_y += attrs_h
    if wrapped_attrs and wrapped_methods:
        svg.line((x, current_y), (x + w, current_y), width=2.0)
    for i, method in enumerate(wrapped_methods):
        svg.text(x + 14, current_y + 23 + i * line_h, method, size=15, anchor="start")
    return box


def cardinality(svg: Svg, x: float, y: float, text: str) -> None:
    svg.label(x, y, text, size=16)


def diamond(svg: Svg, x: float, y: float, size: float = 13) -> None:
    svg.polygon(
        [(x, y - size), (x + size, y), (x, y + size), (x - size, y)],
        fill=LINE,
        stroke=LINE,
        width=1.6,
    )


def generate_use_case(path: Path) -> None:
    svg = Svg(1800, 1040, "Diagrama de casos de uso")
    title(svg, "Diagrama de Casos de Uso", "Sistema de Gestión de Turnos Quirúrgicos")

    boundary = Box(315, 115, 1180, 820)
    svg.rect(boundary.x, boundary.y, boundary.w, boundary.h, fill="#fbfdff", stroke="#9bb4c5", width=3, rx=26)
    svg.text(boundary.cx, boundary.y + 42, "Sistema de Gestión de Turnos Quirúrgicos", size=25, weight="700")

    personal = Box(80, 280, 220, 190)
    admin = Box(80, 640, 220, 190)
    medico = Box(1525, 735, 220, 190)

    case_centers = {
        "gestionar_pacientes": (545, 250, 310, 74, "Gestionar pacientes", WHITE),
        "programar": (885, 300, 345, 84, "Programar turno quirúrgico", BLUE),
        "reprogramar": (885, 430, 360, 84, "Reprogramar turno quirúrgico", WHITE),
        "cancelar": (885, 560, 330, 74, "Cancelar turno quirúrgico", WHITE),
        "consultar_turnos": (1235, 250, 310, 74, "Consultar turnos", WHITE),
        "disponibilidad": (1245, 420, 345, 84, "Consultar disponibilidad", CREAM),
        "asignar": (1245, 565, 370, 84, "Asignar profesionales al turno", CREAM),
        "gestionar_profesionales": (545, 705, 350, 74, "Gestionar profesionales", WHITE),
        "gestionar_especialidades": (545, 820, 360, 74, "Gestionar especialidades", WHITE),
        "gestionar_quirofanos": (915, 705, 330, 74, "Gestionar quirófanos", WHITE),
        "gestionar_tipos": (915, 820, 360, 74, "Gestionar tipos de cirugía", WHITE),
        "agenda": (1245, 820, 350, 74, "Consultar agenda personal", WHITE),
    }
    temp_cases = {
        key: Box(cx - w / 2, cy - h / 2, w, h)
        for key, (cx, cy, w, h, _label, _fill) in case_centers.items()
    }

    personal_point = (personal.cx + 46, personal.y + 72)
    admin_point = (admin.cx + 46, admin.y + 72)
    medico_point = (medico.cx - 46, medico.y + 72)

    # Asociaciones directas, ruteadas en abanico para reducir cruces.
    personal_routes = [
        ("gestionar_pacientes", [personal_point, (315, 250), temp_cases["gestionar_pacientes"].left]),
        ("programar", [personal_point, (315, 305), temp_cases["programar"].left]),
        ("reprogramar", [personal_point, (315, 430), temp_cases["reprogramar"].left]),
        ("cancelar", [personal_point, (315, 560), temp_cases["cancelar"].left]),
        ("consultar_turnos", [personal_point, (315, 205), (1075, 205), temp_cases["consultar_turnos"].left]),
    ]
    for target, route in personal_routes:
        case = temp_cases[target]
        svg.polyline(route, stroke="#6f8190", width=1.7)

    for target, bend_y in [
        ("gestionar_profesionales", 690),
        ("gestionar_quirofanos", 725),
        ("gestionar_especialidades", 805),
        ("gestionar_tipos", 842),
    ]:
        case = temp_cases[target]
        svg.polyline([admin_point, (315, bend_y), case.left], stroke="#6f8190", width=1.7)

    svg.polyline([medico_point, (1495, 820), temp_cases["agenda"].right], stroke="#6f8190", width=1.7)

    personal = actor(svg, personal.x, personal.y, "Personal administrativo")
    admin = actor(svg, admin.x, admin.y, "Administrador del sistema")
    medico = actor(svg, medico.x, medico.y, "Profesional médico")
    svg.polyline(
        [(admin.cx - 62, admin.y + 42), (admin.cx - 62, personal.y + 72), (personal.cx - 46, personal.y + 72)],
        marker_end="openTriangle",
        width=2.0,
    )

    svg.text(545, 180, "Datos maestros", size=18, weight="700", fill=MUTED)
    svg.text(885, 180, "Gestión de turnos", size=18, weight="700", fill=MUTED)
    svg.text(1245, 180, "Consultas e inclusiones", size=18, weight="700", fill=MUTED)

    cases: dict[str, Box] = {}
    for key, (cx, cy, w, h, label, fill) in case_centers.items():
        cases[key] = use_case(svg, cx, cy, w, h, label, fill=fill)

    include_lines = [
        ((1050, 315), (1085, 395), 1112, 344),
        ((1045, 330), (1085, 545), 1120, 512),
        ((1060, 420), (1085, 420), 1094, 405),
    ]
    for p1, p2, label_x, label_y in include_lines:
        svg.line(p1, p2, dash=True, marker_end="arrow", width=2.2)
        svg.label(label_x, label_y, "<<include>>", size=16)

    svg.text(
        svg.width / 2,
        990,
        "Figura 1. El Administrador del sistema es una especialización del Personal administrativo y hereda sus funciones.",
        size=17,
        fill=MUTED,
    )
    svg.save(path)


def generate_er(path: Path) -> None:
    svg = Svg(1850, 1190, "Diagrama Entidad-Relación")
    title(svg, "Diagrama Entidad-Relación", "Modelo de datos para MySQL")

    especialidad = entity(
        svg,
        65,
        135,
        330,
        "ESPECIALIDAD",
        ["PK id_especialidad", "UQ nombre", "descripcion"],
    )
    profesional = entity(
        svg,
        760,
        105,
        360,
        "PROFESIONAL",
        [
            "PK id_profesional",
            "UQ matricula",
            "UQ DNI",
            "nombre",
            "apellido",
            "telefono",
            "email",
            "activo",
            "FK id_especialidad",
        ],
    )
    tipo = entity(
        svg,
        490,
        340,
        390,
        "TIPO_CIRUGIA",
        [
            "PK id_tipo_cirugia",
            "UQ(nombre, id_especialidad)",
            "descripcion",
            "duracion_estimada_minutos",
            "FK id_especialidad",
        ],
    )
    paciente = entity(
        svg,
        455,
        600,
        360,
        "PACIENTE",
        [
            "PK id_paciente",
            "UQ DNI",
            "nombre",
            "apellido",
            "fecha_nacimiento",
            "telefono",
            "email",
            "activo",
        ],
    )
    quirofano = entity(
        svg,
        470,
        875,
        330,
        "QUIROFANO",
        ["PK id_quirofano", "UQ numero", "ubicacion", "estado"],
    )
    turno = entity(
        svg,
        1080,
        560,
        390,
        "TURNO_QUIRURGICO",
        [
            "PK id_turno",
            "fecha_hora_inicio",
            "fecha_hora_fin",
            "estado",
            "observaciones",
            "FK id_paciente",
            "FK id_quirofano",
            "FK id_tipo_cirugia",
        ],
        fill=BLUE,
    )
    turno_prof = entity(
        svg,
        1535,
        405,
        300,
        "TURNO_PROFESIONAL",
        ["PK, FK id_turno", "PK, FK id_profesional", "rol"],
        fill=CREAM,
    )

    # Relations and cardinalities.
    svg.polyline([especialidad.right, (565, especialidad.cy), profesional.left])
    cardinality(svg, especialidad.x + especialidad.w + 55, especialidad.cy - 14, "1")
    cardinality(svg, profesional.x - 55, profesional.cy - 12, "0..N")

    svg.polyline([especialidad.right, (430, tipo.cy), tipo.left])
    cardinality(svg, especialidad.x + especialidad.w + 55, tipo.cy - 13, "1")
    cardinality(svg, tipo.x - 55, tipo.cy - 12, "0..N")

    svg.polyline([tipo.right, (1010, 445), (1080, turno.y + 72)])
    cardinality(svg, tipo.x + tipo.w + 55, 431, "1")
    cardinality(svg, turno.x - 60, turno.y + 74, "0..N")

    svg.polyline([paciente.right, (980, paciente.cy), (1080, turno.y + 140)])
    cardinality(svg, paciente.x + paciente.w + 55, paciente.cy - 12, "1")
    cardinality(svg, turno.x - 60, turno.y + 140, "0..N")

    svg.polyline([quirofano.right, (980, quirofano.cy), (1080, turno.y + 210)])
    cardinality(svg, quirofano.x + quirofano.w + 55, quirofano.cy - 14, "1")
    cardinality(svg, turno.x - 60, turno.y + 210, "0..N")

    svg.polyline([turno.right, (1510, turno.y + 85), turno_prof.left])
    cardinality(svg, turno.x + turno.w + 55, turno.y + 70, "1")
    cardinality(svg, turno_prof.x - 55, turno_prof.cy + 36, "1..N")

    svg.polyline([profesional.right, (1355, profesional.cy), (1535, turno_prof.y + 25)])
    cardinality(svg, profesional.x + profesional.w + 55, profesional.cy - 15, "1")
    cardinality(svg, turno_prof.x - 55, turno_prof.y + 35, "0..N")

    svg.rect(1035, 940, 760, 130, fill=CREAM, stroke="#d6c997", width=1.8, rx=12)
    svg.text(1060, 970, "Reglas de negocio", size=17, weight="700", anchor="start")
    svg.multiline(
        1060,
        1010,
        [
            "QUIROFANO.estado usa HABILITADO, MANTENIMIENTO o FUERA_DE_SERVICIO.",
            "La disponibilidad horaria se calcula revisando turnos existentes.",
            "Cada turno debe tener exactamente un profesional con rol CIRUJANO_PRINCIPAL.",
        ],
        size=16,
        line_height=23,
        anchor="start",
    )

    svg.text(
        svg.width / 2,
        1140,
        "Figura 2. TURNO_PROFESIONAL resuelve la relación muchos a muchos entre turnos y profesionales.",
        size=17,
        fill=MUTED,
    )
    svg.save(path)


def generate_class_diagram_legacy(path: Path) -> None:
    svg = Svg(2100, 1700, "Diagrama de clases")
    title(svg, "Diagrama de Clases", "Dominio, enumeraciones, DAO, servicio y conexion")

    svg.rect(35, 95, 2030, 1040, fill="#fbfdff", stroke=GRID, width=2.0, rx=18)
    svg.text(80, 125, "Dominio", size=18, weight="700", anchor="start", fill=MUTED)

    persona = uml_class(
        svg,
        70,
        160,
        310,
        "Persona",
        ["- id: int", "- dni: String", "- nombre: String", "- apellido: String", "- telefono: String", "- email: String"],
        ["+ getNombreCompleto(): String", "+ validar(): boolean"],
        stereotype="abstract",
    )
    paciente = uml_class(
        svg,
        70,
        500,
        310,
        "Paciente",
        ["- fechaNacimiento: LocalDate", "- activo: boolean"],
        ["+ calcularEdad(): int", "+ activar(): void", "+ desactivar(): void", "+ validar(): boolean"],
    )
    profesional = uml_class(
        svg,
        430,
        500,
        330,
        "Profesional",
        ["- matricula: String", "- especialidad: Especialidad", "- activo: boolean"],
        ["+ activar(): void", "+ desactivar(): void", "+ validar(): boolean"],
    )
    especialidad = uml_class(
        svg,
        430,
        805,
        320,
        "Especialidad",
        ["- id: int", "- nombre: String", "- descripcion: String"],
        ["+ validar(): boolean"],
    )
    tipo = uml_class(
        svg,
        825,
        620,
        360,
        "TipoCirugia",
        [
            "- id: int",
            "- nombre: String",
            "- descripcion: String",
            "- duracionEstimadaMinutos: int",
            "- especialidad: Especialidad",
        ],
        ["+ calcularHoraFin(): LocalDateTime", "+ validar(): boolean"],
    )
    quirofano = uml_class(
        svg,
        1250,
        620,
        330,
        "Quirofano",
        ["- id: int", "- numero: String", "- ubicacion: String", "- estado: EstadoQuirofano"],
        ["+ estaHabilitado(): boolean", "+ cambiarEstado(): void", "+ validar(): boolean"],
    )
    turno = uml_class(
        svg,
        980,
        155,
        430,
        "TurnoQuirurgico",
        [
            "- id: int",
            "- fechaHoraInicio: LocalDateTime",
            "- fechaHoraFin: LocalDateTime",
            "- estado: EstadoTurno",
            "- observaciones: String",
            "- paciente: Paciente",
            "- quirofano: Quirofano",
            "- tipoCirugia: TipoCirugia",
            "- participaciones: List",
        ],
        [
            "+ agregarProfesional(): void",
            "+ cancelar(): void",
            "+ reprogramar(): void",
            "+ seSuperpone(): boolean",
            "+ validar(): boolean",
        ],
        fill=BLUE,
    )
    participacion = uml_class(
        svg,
        850,
        905,
        340,
        "ParticipacionProfesional",
        ["- profesional: Profesional", "- rol: RolProfesional"],
        ["+ validar(): boolean"],
    )
    validable = uml_class(
        svg,
        790,
        1055,
        300,
        "Validable",
        [],
        ["+ validar(): boolean"],
        stereotype="interface",
        fill=CREAM,
        header_fill=CREAM,
    )
    estado_turno = uml_class(
        svg,
        1660,
        165,
        340,
        "EstadoTurno",
        ["PROGRAMADO", "CONFIRMADO", "EN_CURSO", "FINALIZADO", "CANCELADO"],
        [],
        stereotype="enumeration",
    )
    estado_quirofano = uml_class(
        svg,
        1660,
        565,
        340,
        "EstadoQuirofano",
        ["DISPONIBLE", "MANTENIMIENTO", "FUERA_DE_SERVICIO"],
        [],
        stereotype="enumeration",
    )
    rol = uml_class(
        svg,
        1660,
        910,
        340,
        "RolProfesional",
        ["CIRUJANO_PRINCIPAL", "CIRUJANO_ASISTENTE", "ANESTESIOLOGO", "INSTRUMENTADOR"],
        [],
        stereotype="enumeration",
    )

    # Herencia.
    svg.line(paciente.top, persona.bottom, marker_end="openTriangle", width=2.2)
    svg.line(profesional.top, persona.bottom, marker_end="openTriangle", width=2.2)

    # Asociaciones del dominio.
    svg.polyline([turno.left, (710, 395), paciente.right])
    svg.label(745, 407, "N:1", size=15)
    svg.polyline([turno.bottom, (1120, 565), tipo.top])
    svg.label(1110, 575, "N:1", size=15)
    svg.polyline([(1250, turno.y + turno.h - 30), (1370, 560), quirofano.top])
    svg.label(1335, 570, "N:1", size=15)

    comp_start = (turno.x + 80, turno.y + turno.h)
    svg.polyline([comp_start, (1000, 760), participacion.top])
    diamond(svg, comp_start[0], comp_start[1] + 5)
    svg.label(985, 790, "1 .. 1..N", size=15)

    svg.polyline([participacion.left, (660, 820), profesional.bottom])
    svg.label(695, 830, "N:1", size=15)
    svg.polyline([profesional.bottom, (595, 770), especialidad.top])
    svg.label(630, 770, "N:1", size=15)
    svg.polyline([tipo.left, (720, 760), especialidad.right])
    svg.label(755, 770, "N:1", size=15)

    # Dependencias a enumeraciones.
    svg.line(turno.right, estado_turno.left, dash=True, marker_end="arrow", width=2.0)
    svg.line(quirofano.right, estado_quirofano.left, dash=True, marker_end="arrow", width=2.0)
    svg.line(participacion.right, rol.left, dash=True, marker_end="arrow", width=2.0)

    # Realizacion de interfaz Validable.
    for box in [paciente, profesional, tipo, quirofano, turno, participacion]:
        svg.line(box.bottom, validable.top, dash=True, marker_end="openTriangle", width=1.8)

    svg.rect(35, 1190, 2030, 455, fill="#fbfdff", stroke=GRID, width=2.0, rx=18)
    svg.text(80, 1220, "Persistencia y logica de negocio", size=18, weight="700", anchor="start", fill=MUTED)

    service = uml_class(
        svg,
        70,
        1260,
        460,
        "TurnoService",
        ["- turnoDAO: TurnoDAO", "- profesionalDAO: ProfesionalDAO", "- quirofanoDAO: QuirofanoDAO"],
        ["+ programarTurno(): void", "+ reprogramarTurno(): void", "+ cancelarTurno(): void", "+ verificarDisponibilidad(): boolean"],
        fill=BLUE,
    )
    prof_dao = uml_class(svg, 590, 1260, 260, "ProfesionalDAO", ["CRUD de Profesional"], [])
    quiro_dao = uml_class(svg, 875, 1260, 260, "QuirofanoDAO", ["CRUD de Quirofano"], [])
    tipo_dao = uml_class(svg, 1160, 1260, 270, "TipoCirugiaDAO", ["CRUD de TipoCirugia"], [])
    turno_dao = uml_class(svg, 1455, 1260, 300, "TurnoDAO", ["CRUD de TurnoQuirurgico", "+ buscarSuperposiciones(): List"], [])
    paciente_dao = uml_class(svg, 1780, 1260, 260, "PacienteDAO", ["CRUD de Paciente"], [])
    crud = uml_class(
        svg,
        690,
        1455,
        380,
        "CrudDAO<T>",
        [],
        [
            "+ crear(objeto: T): void",
            "+ buscarPorId(id: int): T",
            "+ listar(): List<T>",
            "+ actualizar(objeto: T): void",
            "+ eliminar(id: int): void",
        ],
        stereotype="interface",
        fill=CREAM,
        header_fill=CREAM,
    )
    conexion = uml_class(
        svg,
        1210,
        1455,
        420,
        "ConexionMySQL",
        ["- url: String", "- usuario: String", "- contrasena: String"],
        ["+ obtenerConexion(): Connection"],
    )

    for dao in [prof_dao, quiro_dao, turno_dao]:
        svg.line(service.right, dao.top, marker_end="arrow", width=2.0)
    for dao in [prof_dao, quiro_dao, tipo_dao, turno_dao, paciente_dao]:
        svg.line(dao.bottom, crud.top, dash=True, marker_end="openTriangle", width=1.8)
        svg.line(dao.bottom, conexion.top, marker_end="arrow", width=1.8)

    svg.text(
        svg.width / 2,
        1680,
        "Figura 3. Clases del dominio con herencia, interfaz, composicion y complemento DAO/servicio.",
        size=17,
        fill=MUTED,
    )
    svg.save(path)


def generate_class_diagram(path: Path) -> None:
    svg = Svg(2300, 1840, "Diagrama de clases")
    title(svg, "Diagrama de Clases", "Dominio, enumeraciones, DAO, servicio y conexión")

    svg.rect(35, 95, 2230, 1040, fill="#fbfdff", stroke=GRID, width=2.0, rx=18)
    svg.text(80, 125, "Paquete dominio", size=18, weight="700", anchor="start", fill=MUTED)

    persona = uml_class(
        svg,
        80,
        160,
        360,
        "Persona",
        ["- id: int", "- dni: String", "- nombre: String", "- apellido: String", "- telefono: String", "- email: String"],
        ["+ getNombreCompleto(): String", "+ validar(): boolean"],
        stereotype="abstract",
    )
    paciente = uml_class(
        svg,
        80,
        515,
        360,
        "Paciente",
        ["- fechaNacimiento: LocalDate", "- activo: boolean"],
        ["+ calcularEdad(): int", "+ activar(): void", "+ desactivar(): void", "+ validar(): boolean"],
    )
    profesional = uml_class(
        svg,
        500,
        515,
        390,
        "Profesional",
        ["- matricula: String", "- especialidad: Especialidad", "- activo: boolean"],
        ["+ activar(): void", "+ desactivar(): void", "+ validar(): boolean"],
    )
    especialidad = uml_class(
        svg,
        500,
        820,
        360,
        "Especialidad",
        ["- id: int", "- nombre: String", "- descripcion: String"],
        ["+ validar(): boolean"],
    )
    turno = uml_class(
        svg,
        940,
        145,
        630,
        "TurnoQuirurgico",
        [
            "- id: int",
            "- fechaHoraInicio: LocalDateTime",
            "- fechaHoraFin: LocalDateTime",
            "- estado: EstadoTurno",
            "- observaciones: String",
            "- paciente: Paciente",
            "- quirofano: Quirofano",
            "- tipoCirugia: TipoCirugia",
            "- participaciones: List<ParticipacionProfesional>",
        ],
        [
            "+ agregarProfesional(profesional: Profesional, rol: RolProfesional): void",
            "+ cancelar(motivo: String): void",
            "+ reprogramar(inicio: LocalDateTime, fin: LocalDateTime, quirofano: Quirofano): void",
            "+ seSuperpone(inicio: LocalDateTime, fin: LocalDateTime): boolean",
            "+ validar(): boolean",
        ],
        fill=BLUE,
    )
    participacion = uml_class(
        svg,
        980,
        690,
        520,
        "ParticipacionProfesional",
        ["- profesional: Profesional", "- rol: RolProfesional"],
        ["+ validar(): boolean"],
    )
    tipo = uml_class(
        svg,
        900,
        895,
        500,
        "TipoCirugia",
        [
            "- id: int",
            "- nombre: String",
            "- descripcion: String",
            "- duracionEstimadaMinutos: int",
            "- especialidad: Especialidad",
        ],
        ["+ calcularHoraFin(inicio: LocalDateTime): LocalDateTime", "+ validar(): boolean"],
    )
    quirofano = uml_class(
        svg,
        1460,
        895,
        420,
        "Quirofano",
        ["- id: int", "- numero: String", "- ubicacion: String", "- estado: EstadoQuirofano"],
        ["+ estaHabilitado(): boolean", "+ cambiarEstado(estado: EstadoQuirofano): void", "+ validar(): boolean"],
    )
    validable = uml_class(
        svg,
        1605,
        745,
        320,
        "Validable",
        [],
        ["+ validar(): boolean"],
        stereotype="interface",
        fill=CREAM,
        header_fill=CREAM,
    )
    estado_turno = uml_class(
        svg,
        2000,
        200,
        250,
        "EstadoTurno",
        ["PROGRAMADO", "CONFIRMADO", "EN_CURSO", "FINALIZADO", "CANCELADO"],
        [],
        stereotype="enumeration",
    )
    estado_quirofano = uml_class(
        svg,
        2000,
        570,
        250,
        "EstadoQuirofano",
        ["HABILITADO", "MANTENIMIENTO", "FUERA_DE_SERVICIO"],
        [],
        stereotype="enumeration",
    )
    rol = uml_class(
        svg,
        2000,
        870,
        250,
        "RolProfesional",
        ["CIRUJANO_PRINCIPAL", "CIRUJANO_ASISTENTE", "ANESTESIOLOGO", "INSTRUMENTADOR"],
        [],
        stereotype="enumeration",
    )

    # Herencia.
    svg.line(paciente.top, persona.bottom, marker_end="openTriangle", width=2.2)
    svg.line(profesional.top, persona.bottom, marker_end="openTriangle", width=2.2)

    # Asociaciones y multiplicidades UML.
    paciente_turno_end = (turno.x, turno.y + turno.h - 62)
    svg.polyline([paciente.right, (470, 665), (850, 665), paciente_turno_end])
    svg.label(463, 650, "1", size=15)
    svg.label(910, paciente_turno_end[1] - 10, "0..*", size=15)

    comp_start = (turno.cx, turno.y + turno.h)
    svg.polyline([comp_start, participacion.top])
    diamond(svg, comp_start[0], comp_start[1] + 5)
    svg.label(comp_start[0] - 20, comp_start[1] + 38, "1", size=15)
    svg.label(participacion.cx + 28, participacion.y - 12, "1..*", size=15)

    svg.polyline([profesional.right, (930, profesional.cy), participacion.left])
    svg.label(910, profesional.cy - 14, "1", size=15)
    svg.label(participacion.x - 30, participacion.cy - 12, "0..*", size=15)

    svg.polyline([profesional.bottom, especialidad.top])
    svg.label(profesional.cx + 28, profesional.y + profesional.h + 18, "0..*", size=15)
    svg.label(especialidad.cx + 36, especialidad.y - 12, "1", size=15)

    svg.polyline([especialidad.right, (880, especialidad.cy), tipo.left])
    svg.label(883, especialidad.cy - 15, "1", size=15)
    svg.label(tipo.x - 32, tipo.cy - 15, "0..*", size=15)

    svg.polyline([(turno.x + 135, turno.y + turno.h), (860, 760), tipo.top])
    svg.label(905, 750, "0..*", size=15)
    svg.label(tipo.cx - 50, tipo.y - 12, "1", size=15)

    svg.polyline([turno.right, (1640, 615), quirofano.top])
    svg.label(1595, 615, "0..*", size=15)
    svg.label(quirofano.cx + 30, quirofano.y - 12, "1", size=15)

    # Implementacion de interfaces y dependencias a enumeraciones.
    svg.polyline([persona.right, (740, persona.cy), (1605, validable.cy), validable.left], dash=True, marker_end="openTriangle", width=1.8)
    svg.polyline([turno.right, (1605, turno.cy), validable.left], dash=True, marker_end="openTriangle", width=1.8)
    svg.line(tipo.right, validable.left, dash=True, marker_end="openTriangle", width=1.8)
    svg.line(quirofano.left, validable.left, dash=True, marker_end="openTriangle", width=1.8)
    svg.line(participacion.right, validable.left, dash=True, marker_end="openTriangle", width=1.8)

    svg.line(turno.right, estado_turno.left, dash=True, marker_end="arrow", width=2.0)
    svg.line(quirofano.right, estado_quirofano.left, dash=True, marker_end="arrow", width=2.0)
    svg.line(participacion.right, rol.left, dash=True, marker_end="arrow", width=2.0)

    svg.rect(35, 1190, 2230, 560, fill="#fbfdff", stroke=GRID, width=2.0, rx=18)
    svg.text(80, 1220, "Paquete persistencia y lógica de negocio", size=18, weight="700", anchor="start", fill=MUTED)

    service = uml_class(
        svg,
        70,
        1270,
        640,
        "TurnoService",
        [
            "- pacienteDAO: PacienteDAO",
            "- profesionalDAO: ProfesionalDAO",
            "- quirofanoDAO: QuirofanoDAO",
            "- tipoCirugiaDAO: TipoCirugiaDAO",
            "- turnoDAO: TurnoDAO",
        ],
        [
            "+ programarTurno(pacienteId: int, tipoId: int, quirofanoId: int, inicio: LocalDateTime, profesionales: List<ParticipacionProfesional>): TurnoQuirurgico",
            "+ reprogramarTurno(turnoId: int, inicio: LocalDateTime, fin: LocalDateTime, quirofanoId: int): void",
            "+ cancelarTurno(turnoId: int, motivo: String): void",
            "+ verificarDisponibilidad(inicio: LocalDateTime, fin: LocalDateTime, quirofanoId: int, profesionales: List<Profesional>): boolean",
        ],
        fill=BLUE,
    )
    paciente_dao = uml_class(svg, 790, 1270, 245, "PacienteDAO", [], ["CRUD de Paciente"])
    profesional_dao = uml_class(svg, 1060, 1270, 245, "ProfesionalDAO", [], ["CRUD de Profesional"])
    quirofano_dao = uml_class(svg, 1330, 1270, 245, "QuirofanoDAO", [], ["CRUD de Quirofano"])
    tipo_dao = uml_class(svg, 1600, 1270, 245, "TipoCirugiaDAO", [], ["CRUD de TipoCirugia"])
    turno_dao = uml_class(
        svg,
        1870,
        1270,
        340,
        "TurnoDAO",
        [],
        [
            "CRUD de TurnoQuirurgico",
            "+ buscarSuperposiciones(inicio: LocalDateTime, fin: LocalDateTime, quirofanoId: int): List<TurnoQuirurgico>",
        ],
    )
    crud = uml_class(
        svg,
        1040,
        1535,
        430,
        "CrudDAO<T>",
        [],
        [
            "+ crear(objeto: T): void",
            "+ buscarPorId(id: int): T",
            "+ listar(): List<T>",
            "+ actualizar(objeto: T): void",
            "+ eliminar(id: int): void",
        ],
        stereotype="interface",
        fill=CREAM,
        header_fill=CREAM,
    )
    conexion = uml_class(
        svg,
        1610,
        1535,
        440,
        "ConexionMySQL",
        ["- url: String", "- usuario: String", "- contrasena: String"],
        ["+ obtenerConexion(): Connection"],
    )

    dao_boxes = [paciente_dao, profesional_dao, quirofano_dao, tipo_dao, turno_dao]
    for dao in dao_boxes:
        svg.polyline([dao.bottom, crud.top], dash=True, marker_end="openTriangle", width=1.7)
    svg.rect(1570, 1675, 510, 48, fill=CREAM, stroke="#d6c997", width=1.5, rx=8)
    svg.text(1590, 1705, "Nota: todos los DAO utilizan ConexionMySQL.", size=15, anchor="start")

    svg.text(
        svg.width / 2,
        1805,
        "Figura 3. Clases del dominio y capa de persistencia separadas por paquetes UML.",
        size=17,
        fill=MUTED,
    )
    svg.save(path)


def write_index(out_dir: Path) -> Path:
    index = out_dir / "index.html"
    html = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Diagramas - Turnos Quirúrgicos</title>
  <style>
    body {
      margin: 0;
      font-family: "Segoe UI", Arial, sans-serif;
      color: #1f2933;
      background: #f3f6f8;
    }
    main {
      width: min(1400px, calc(100vw - 32px));
      margin: 28px auto 48px;
    }
    h1 {
      margin: 0 0 18px;
      font-size: 28px;
    }
    h2 {
      margin: 28px 0 12px;
      font-size: 20px;
    }
    img {
      display: block;
      width: 100%;
      height: auto;
      background: white;
      border: 1px solid #d8e2e8;
      border-radius: 8px;
      box-shadow: 0 4px 14px rgba(31, 41, 51, 0.08);
    }
  </style>
</head>
<body>
  <main>
    <h1>Sistema de Gestión de Turnos Quirúrgicos</h1>
    <h2>1. Diagrama de casos de uso</h2>
    <img src="diagrama_casos_uso.svg" alt="Diagrama de casos de uso">
    <h2>2. Diagrama Entidad-Relación</h2>
    <img src="diagrama_entidad_relacion.svg" alt="Diagrama entidad relación">
    <h2>3. Diagrama de clases</h2>
    <img src="diagrama_clases.svg" alt="Diagrama de clases">
  </main>
</body>
</html>
"""
    index.write_text(html, encoding="utf-8")
    return index


def generate_all(open_viewer: bool = False) -> list[Path]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    svg_outputs = [
        OUT_DIR / "diagrama_casos_uso.svg",
        OUT_DIR / "diagrama_entidad_relacion.svg",
        OUT_DIR / "diagrama_clases.svg",
    ]
    generate_use_case(svg_outputs[0])
    generate_er(svg_outputs[1])
    generate_class_diagram(svg_outputs[2])
    index = write_index(OUT_DIR)
    png_outputs = [path.with_suffix(".png") for path in svg_outputs if path.with_suffix(".png").exists()]
    outputs = svg_outputs + png_outputs + [index]
    if open_viewer:
        webbrowser.open(index.resolve().as_uri())
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera los tres diagramas del sistema de turnos quirúrgicos.")
    parser.add_argument("--open", action="store_true", help="Abre el visor HTML después de generar los SVG.")
    args = parser.parse_args()
    outputs = generate_all(open_viewer=args.open)
    print("Archivos generados:")
    for path in outputs:
        print(f"- {path}")


if __name__ == "__main__":
    main()
