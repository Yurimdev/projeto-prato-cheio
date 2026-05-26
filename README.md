# Projeto Prato Cheio - Sistema de Gestão de Doações para Bancos de Alimentos

> 🔗 **Aplicação publicada (Deploy):** _<SUBSTITUIR_PELO_LINK_DO_STREAMLIT>_

![Versão do App](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-green.svg)

## 📌 O Problema
Muitas ONGs e bancos de alimentos têm dificuldade para organizar as doações que recebem. O uso de papel ou planilhas acaba gerando erros no estoque e perda de tempo que poderia ser usado para ajudar quem precisa.

## 💡 A Solução (Projeto Prato Cheio)
O **Projeto Prato Cheio** é um programa de terminal simples feito em Python. Ele permite cadastrar doadores e itens de forma rápida, garantindo que os dados estejam organizados e corretos. O sistema não permite cadastrar quantidades vazias ou negativas, evitando erros comuns de digitação.

## 🎯 Público-Alvo
- Bancos de alimentos locais.
- ONGs que recebem e distribuem suprimentos.
- Projetos sociais e centros comunitários.

## ⚙️ Funcionalidades
- **Cadastro de Doações:** Registro de quem doou, o que foi doado e a quantidade.
- **Lista de Estoque:** Veja em uma lista simples tudo o que já foi coletado.
- **Filtro de Erros:** O sistema bloqueia automaticamente entradas com quantidades inválidas.
- **Enriquecimento via API pública (Open Food Facts):** Ao registrar um item, o sistema consulta a API e traz **marca, categoria e Nutri-Score** do alimento, ajudando a ONG a entender melhor o que recebe.
- **Interface Web:** Além do CLI, há uma aplicação web (Streamlit) publicada na nuvem.

## 🌐 Integração com API Pública (Open Food Facts)
A aplicação consome a API aberta **[Open Food Facts](https://world.openfoodfacts.org/)** (gratuita, sem necessidade de chave). A cada doação registrada, o sistema faz uma requisição `HTTP GET` ao endpoint de busca e utiliza os dados retornados (produto, marca, categoria e Nutri-Score) para enriquecer o cadastro do item.

A lógica de integração está isolada em [`src/api.py`](src/api.py) e é validada por um **teste de integração** em [`tests/test_integration.py`](tests/test_integration.py), que simula (mock) a resposta da API para garantir que o fluxo de dados não quebre a aplicação.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.8+
- **Interface Web / Deploy:** `streamlit`
- **Consumo de API:** `requests`
- **Testes Automatizados:** `pytest` (unitários + integração)
- **Linting e Análises Estáticas:** `flake8`
- **CI/CD:** GitHub Actions (lint + testes a cada push/PR)

---

## 🚀 Como Executar o Projeto

**1. Clone e acesse o Repositório:**
```bash
git clone https://github.com/Yurimdev/projeto-prato-cheio.git
cd projeto-prato-cheio
```

**2. Crie e ative o ambiente virtual (Recomendado):**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Execute o programa principal:**

*Adicionar nova doação:*
```bash
python src/main.py add --donor "Padaria São João" --item "Pães variados" --qty 50
```

*Listar todas as doações:*
```bash
python src/main.py list
```

*Consultar dados de um alimento na API pública (Open Food Facts):*
```bash
python src/main.py info --item "Arroz"
```

---

## 🌍 Como Executar a Interface Web (Streamlit)

A versão web reaproveita a mesma lógica de validação e a integração com a API.
```bash
pip install -r requirements.txt
streamlit run app.py
```
A aplicação também está publicada na nuvem — veja o link no topo deste README.

---

## 🧪 Como Executar os Testes

Para garantir a qualidade, utilizamos o `pytest`.
```bash
# Na raiz do projeto, execute:
pytest tests/
```
Isso validará o Caminho Feliz, Tratamento de Entradas Inválidas e Casos Limite.

---

## 🔍 Como Executar a Análise Estática (Linting)

Para verificar aderência às normas PEP8 de formatação:
```bash
flake8 src tests
```

---

## 📺 Evidência de Funcionamento

> **Atenção:** 
> *Abaixo está o registro quando executa no terminal:*

```bash
$ python src/main.py add --donor "Yuri Vinicius" --item "Cestas Básicas" --qty 50
Sucesso: Doação de 50x 'Cestas Básicas' por 'Yuri Vinicius' registrada!

$ python src/main.py add --donor "Professor de BOOTCAMP" --item "Pacotes de Arroz" --qty 100
Sucesso: Doação de 100x 'Pacotes de Arroz' por 'Professor de BOOTCAMP' registrada!

$ python src/main.py list

--- Lista de Doações ---
1. Doador: Yuri Vinicius | Item: Cestas Básicas | Qtd: 50
2. Doador: Professor de BOOTCAMP | Item: Pacotes de Arroz | Qtd: 100
------------------------
```

---

## 📸 Provas de Funcionamento (Captura de Tela)

Abaixo está o print da execução dos comandos no terminal:

![Execução Terminal](img/evidencia.png)

---

## 📄 Autoria e Licença

- **Autor:** Yuri Vinicius Pereira Martins (RA: 22504945)
- **Disciplina:** Bootcamp II - Entrega Intermediária
- **Versão:** 2.0.0
- **Licença:** Todos os direitos reservados. Confira o arquivo `LICENSE` para mais detalhes.
