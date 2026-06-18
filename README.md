# 📚 Biblioteca Digital — Sistema de Gerenciamento

> Projeto desenvolvido para a disciplina **Programação para Ciência de Dados** — PUCPR, Hora da Prática 2.

Sistema de linha de comando (CLI) em Python para gerenciar documentos digitais de uma biblioteca universitária, permitindo listar, adicionar, renomear e remover arquivos e diretórios de forma eficiente.

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como usar](#como-usar)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Executando os testes](#executando-os-testes)
- [Guia de contribuição](CONTRIBUTING.md)

---

## Funcionalidades

| Operação | Descrição |
|---|---|
| `listar` | Lista documentos por tipo, por ano ou todos de uma vez |
| `adicionar` | Copia um documento externo para o acervo |
| `renomear` | Renomeia um documento existente no acervo |
| `remover` | Remove um documento do acervo (com confirmação) |
| `mkdir` | Cria um subdiretório dentro do acervo |
| `rmdir` | Remove um subdiretório vazio do acervo |

**Formatos suportados:** `.pdf`, `.epub`, `.docx`, `.txt`, `.mobi`

---

## Requisitos

- Python 3.10 ou superior
- Nenhuma dependência externa — apenas a biblioteca padrão do Python

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/new-emi/biblioteca-digital.git
cd biblioteca-digital
```

Nenhuma instalação adicional é necessária.

---

## Como usar

### Listar documentos

```bash
# Listar todos
python biblioteca.py listar

# Listar agrupado por tipo de arquivo
python biblioteca.py listar --por tipo

# Listar agrupado por ano de modificação
python biblioteca.py listar --por ano
```

### Adicionar documento

```bash
python biblioteca.py adicionar /caminho/para/artigo.pdf
```

### Renomear documento

```bash
python biblioteca.py renomear artigo_antigo.pdf artigo_novo.pdf
```

### Remover documento

```bash
# Com confirmação interativa
python biblioteca.py remover artigo.pdf

# Sem confirmação (forçado)
python biblioteca.py remover artigo.pdf --forcar
```

### Gerenciar diretórios

```bash
# Criar subdiretório
python biblioteca.py mkdir teses-2024

# Remover subdiretório vazio
python biblioteca.py rmdir teses-2024
```

---

## Estrutura do projeto

```
biblioteca-digital/
├── acervo/                  # Diretório principal do acervo (criado automaticamente)
├── biblioteca.py            # Código-fonte principal do sistema
├── test_biblioteca.py       # Testes automatizados (18 casos de teste)
├── CONTRIBUTING.md          # Guia de contribuição com Git e GitHub
└── README.md                # Esta documentação
```

---

## Executando os testes

```bash
python -m unittest test_biblioteca -v
```

Resultado esperado: **18 testes, todos passando (OK).**

Cada módulo do sistema possui cobertura de testes para os cenários de sucesso e de erro:

- **TestListagem** — listagem vazia, com arquivos, por tipo e por ano
- **TestAdicionar** — arquivo válido, inexistente, formato inválido e duplicado
- **TestRenomear** — sucesso, arquivo inexistente, formato inválido e conflito de nome
- **TestRemover** — sucesso e arquivo inexistente
- **TestDiretorios** — criar, criar duplicado, remover vazio e remover não vazio

---

## Convenções de código

O projeto segue a [PEP 8](https://pep8.org/):

- Nomes de funções e variáveis em `snake_case`
- Docstrings em todas as funções públicas (estilo Google)
- Linhas com no máximo 88 caracteres
- Separação visual por blocos com comentários `# ───`
