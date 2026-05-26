import flet as ft
from dataclasses import dataclass
from typing import List

# EJERCICIO: Tabla de estudiantes con DataTable
# Muestra datos en formato de tabla con filas y columnas


@dataclass
class Estudiante:
    nombre: str
    codigo: str
    nota1: float
    nota2: float
    nota3: float

    @property
    def promedio(self) -> float:
        return (self.nota1 + self.nota2 + self.nota3) / 3

    @property
    def aprobado(self) -> bool:
        return self.promedio >= 3.0


def main(page: ft.Page):
    page.title = "Tabla de Estudiantes"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Datos de ejemplo
    estudiantes: List[Estudiante] = [
        Estudiante("Ana García", "2021001", 4.5, 3.8, 4.2),
        Estudiante("Carlos López", "2021002", 2.5, 2.8, 3.1),
        Estudiante("María Torres", "2021003", 1.5, 2.0, 2.5),
        Estudiante("Pedro Ramírez", "2021004", 5.0, 4.8, 4.9),
        Estudiante("Laura Díaz", "2021005", 3.2, 3.5, 3.8),
    ]

    def fila_estudiante(est: Estudiante) -> ft.DataRow:
        color_promedio = ft.Colors.GREEN_800 if est.aprobado else ft.Colors.RED_700
        fondo_fila = ft.Colors.RED_100 if not est.aprobado else ft.Colors.WHITE
        icono_estado = ft.Icon(
            ft.Icons.CHECK_CIRCLE if est.aprobado else ft.Icons.CANCEL,
            color=color_promedio,
            size=20
        )

        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(est.nombre, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87)),
                ft.DataCell(ft.Text(est.codigo, color=ft.Colors.BLACK54)),
                ft.DataCell(ft.Text(f"{est.nota1:.1f}", color=ft.Colors.BLACK87)),
                ft.DataCell(ft.Text(f"{est.nota2:.1f}", color=ft.Colors.BLACK87)),
                ft.DataCell(ft.Text(f"{est.nota3:.1f}", color=ft.Colors.BLACK87)),
                ft.DataCell(ft.Text(f"{est.promedio:.2f}", color=color_promedio, weight=ft.FontWeight.BOLD)),
                ft.DataCell(icono_estado),
            ],
            color=fondo_fila
        )

    def col(titulo):
        return ft.DataColumn(
            ft.Text(titulo, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=14)
        )

    def col_num(titulo):
        return ft.DataColumn(
            ft.Text(titulo, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, size=14),
            numeric=True
        )

    tabla = ft.DataTable(
        columns=[
            col("Nombre"),
            col("Código"),
            col_num("Nota 1"),
            col_num("Nota 2"),
            col_num("Nota 3"),
            col_num("Promedio"),
            col("Estado"),
        ],
        rows=[fila_estudiante(est) for est in estudiantes],
        border=ft.Border.all(1, ft.Colors.INDIGO_200),
        border_radius=10,
        horizontal_lines=ft.BorderSide(1, ft.Colors.GREY_300),
        heading_row_color=ft.Colors.INDIGO_700,
        heading_row_height=52,
    )

    # Estadísticas del grupo
    aprobados = sum(1 for e in estudiantes if e.aprobado)
    reprobados = len(estudiantes) - aprobados
    promedio_grupo = sum(e.promedio for e in estudiantes) / len(estudiantes)

    def stat_card(label, valor, color):
        return ft.Container(
            content=ft.Column(
                [ft.Text(str(valor), size=28, weight=ft.FontWeight.BOLD, color=color),
                 ft.Text(label, size=13, color=ft.Colors.GREY)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=2
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=12,
            border=ft.Border.all(1, ft.Colors.GREY_200),
            width=140
        )

    page.add(
        ft.Text("Reporte de Notas", size=28, weight=ft.FontWeight.BOLD),
        ft.Row([
            stat_card("Aprobados", aprobados, ft.Colors.GREEN),
            stat_card("Reprobados", reprobados, ft.Colors.RED),
            stat_card("Promedio del Grupo", f"{promedio_grupo:.2f}", ft.Colors.BLUE),
        ], spacing=10),
        ft.Divider(),
        ft.Text("Detalle por Estudiante", size=18, weight=ft.FontWeight.BOLD),
        ft.Container(content=tabla, border_radius=10)
    )


ft.run(main)
