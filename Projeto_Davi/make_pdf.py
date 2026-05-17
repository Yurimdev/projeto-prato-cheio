from fpdf import FPDF
from datetime import datetime

class InformePDF(FPDF):
    def header(self):
        # Normal textual header in black, no background
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(0, 0, 0)
        self.ln(10)
        self.cell(0, 10, 'PROJETO DE ADOÇÃO ANIMAL', align='C')
        self.ln(25)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(169, 169, 169)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 15)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def chapter_body(self, text):
        self.set_font('Helvetica', '', 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 7, text)
        self.ln(5)

pdf = InformePDF()
pdf.add_page()
pdf.ln(10)

pdf.set_font('Helvetica', 'B', 12)
pdf.set_text_color(40, 40, 40)
# Different identification block
pdf.cell(0, 8, 'INFORMAÇÕES DO ESTUDANTE', new_x="LMARGIN", new_y="NEXT")
pdf.set_font('Helvetica', '', 12)
pdf.cell(0, 6, f'  -  Nome: Davi Augusto de Barros Resende Santana da Silva', new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 6, f'  -  RA: 22505381', new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

pdf.chapter_title('1. Sobre o Projeto')
desc_app = (
    "O 'Sistema de Controle de Adoção' foi concebido com uma interface via linha de "
    "comando, promovendo um processo de registro leve e ágil para abrigos.\n\n"
    "Os usuários podem registrar novos cães, gatos e outros animais, listar os bichinhos e "
    "alterar os status de adoção em tempo real."
)
pdf.chapter_body(desc_app)

pdf.chapter_title('2. Funcionalidades Desenvolvidas')
desc_func = (
    " * Entrada de Dados Dinâmica: Cadastro completo via linha de comando.\n"
    " * Persistência Inteligente: Salva automaticamente tudo em um arquivo 'animais.json'.\n"
    " * Testes Resilientes: Cobertura usando o framework 'pytest'.\n"
    " * CI/CD: Pipeline GitHub Actions que valida o código antes de qualquer merge."
)
pdf.chapter_body(desc_func)

pdf.chapter_title('3. Acesso ao Repositório')
pdf.set_font('Helvetica', '', 12)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 8, 'Abaixo está o link oficial da solução no GitHub:', new_x="LMARGIN", new_y="NEXT")

link = "https://github.com/Gaveta-cmd/adocao-animais-trabalhobootcamp"
pdf.set_font('Helvetica', 'B', 12)
pdf.set_text_color(0, 50, 200) # Blue back to standard
pdf.cell(0, 8, link, new_x="LMARGIN", new_y="NEXT", link=link)

# Finally generate
pdf.output('Entrega_Adocao_Davi.pdf')
print("PDF gerado com sucesso com nova estilização!")
