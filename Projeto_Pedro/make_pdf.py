from fpdf import FPDF
from datetime import datetime

class InformePDF(FPDF):
    def header(self):
        self.rect(5, 5, 200, 287)
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(40, 40, 40)
        self.cell(0, 15, 'RELATÓRIO DE ENTREGA - MAIS SAÚDE', center=True, align='C')
        self.ln(10)
        self.set_font('Helvetica', 'I', 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'Sistema de Acompanhamento e Bem Estar', center=True, align='C')
        self.line(10, 35, 200, 35)
        self.ln(20)

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_fill_color(220, 230, 240)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, title, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('Helvetica', '', 12)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 8, text)
        self.ln(5)

pdf = InformePDF()
pdf.add_page()

pdf.set_font('Helvetica', 'B', 12)
pdf.set_text_color(0, 0, 0)
pdf.cell(50, 8, 'Aluno:', new_x="RIGHT")
pdf.set_font('Helvetica', '', 12)
pdf.cell(0, 8, 'Pedro Vitor Gomes Ferreira', new_x="LMARGIN", new_y="NEXT")

pdf.set_font('Helvetica', 'B', 12)
pdf.cell(50, 8, 'RA:', new_x="RIGHT")
pdf.set_font('Helvetica', '', 12)
pdf.cell(0, 8, '22509172', new_x="LMARGIN", new_y="NEXT")

pdf.set_font('Helvetica', 'B', 12)
pdf.cell(50, 8, 'Data da Entrega:', new_x="RIGHT")
pdf.set_font('Helvetica', '', 12)
data_atual = datetime.now().strftime("%d/%m/%Y")
pdf.cell(0, 8, data_atual, new_x="LMARGIN", new_y="NEXT")
pdf.ln(10)

pdf.chapter_title('1. Resumo do Aplicativo: Mais Saúde')
desc_app = (
    "O aplicativo Mais Saúde foi desenvolvido com a finalidade de auxiliar usuários a manterem "
    "o controle e acompanhamento de uma rotina de hábitos saudáveis, focando especialmente "
    "na ingestão de alimentos, rastreio calórico diário e verificação de rotinas vitais "
    "(como sono e hidratação adequados).\n\n"
    "Totalmente operado pelo terminal e construído em Python, o software possibilita uma "
    "maneira minimalista e direta de garantir registros sem distrações."
)
pdf.chapter_body(desc_app)

pdf.chapter_title('2. Características e Funcionalidades')
desc_func = (
    "- Lógica de Entrada de Dados (Validação e formatação de valores inteiros para calorias).\n"
    "- Persistência Local (As informações são conservadas em um arquivo JSON na máquina).\n"
    "- Arquitetura de Testes (Uso de testes de unidade para garantir qualidade do código em cada salvamento e leitura local).\n"
    "- Automação (Garantia de que atualizações tenham fluxo verificado pelo software na nuvem)."
)
pdf.chapter_body(desc_func)

pdf.chapter_title('3. Evidência do Repositório')
pdf.set_font('Helvetica', '', 12)
pdf.cell(0, 8, 'O código pode ser acessado pelo link:', new_x="LMARGIN", new_y="NEXT")

link = "https://github.com/PvZin222/bootcamp-habitos-saudaveis"
pdf.set_font('Helvetica', 'B', 12)
pdf.set_text_color(0, 50, 200)
pdf.cell(0, 8, link, new_x="LMARGIN", new_y="NEXT", link=link)

pdf.output('Entrega_MaisSaude_Pedro.pdf')
print("PDF gerado com sucesso!")
