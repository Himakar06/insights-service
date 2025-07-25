from fpdf import FPDF
import matplotlib.pyplot as plt
import pandas as pd
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Data Insights Report', border=False, ln=1, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def add_section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.ln(10)
        self.cell(0, 10, title, ln=True)

    def add_text(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, text)

    def add_table(self, df: pd.DataFrame, title: str = ""):
        self.add_section_title(title)
        self.set_font('Arial', '', 10)
        col_widths = [30] * len(df.columns)
        row_height = 8

        # Header
        for col in df.columns:
            self.cell(col_widths[0], row_height, str(col), border=1)
        self.ln()

        # Rows
        for _, row in df.iterrows():
            for item in row:
                self.cell(col_widths[0], row_height, str(item), border=1)
            self.ln()

    def add_image(self, image_path, title=""):
        self.add_section_title(title)
        self.image(image_path, w=180)
