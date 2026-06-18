# Guia de Contribuição

Obrigado por querer contribuir com o projeto **Biblioteca Digital**! Este guia explica como configurar o ambiente, trabalhar com o repositório e submeter contribuições de qualidade.

---

## 1. Configuração inicial do Git

Antes de tudo, certifique-se de que seu Git está configurado com seu nome e e-mail:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

---

## 2. Clonando o repositório

```bash
git clone https://github.com/<seu-usuario>/biblioteca-digital.git
cd biblioteca-digital
```

---

## 3. Fluxo de trabalho

### 3.1 Crie uma branch para sua contribuição

Nunca trabalhe diretamente na branch `main`. Crie uma branch com nome descritivo:

```bash
# Para novas funcionalidades
git checkout -b feat/nome-da-funcionalidade

# Para correção de bugs
git checkout -b fix/descricao-do-bug

# Para melhorias de documentação
git checkout -b docs/o-que-foi-documentado
```

**Exemplos de nomes válidos:**
- `feat/exportar-relatorio-csv`
- `fix/erro-renomear-arquivo-duplicado`
- `docs/atualizar-exemplos-cli`

---

### 3.2 Realizando commits

Commits devem ser **pequenos, atômicos e descritivos**. Use o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>: <descrição curta no imperativo>
```

**Tipos aceitos:**

| Tipo | Quando usar |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Alteração em documentação |
| `test` | Adição ou correção de testes |
| `refactor` | Refatoração sem mudança de comportamento |
| `style` | Formatação, espaçamento (sem mudança de lógica) |

**Exemplos de commits corretos:**

```bash
git commit -m "feat: adicionar listagem de documentos por ano"
git commit -m "fix: corrigir erro ao renomear arquivo com nome duplicado"
git commit -m "test: adicionar casos de teste para remover_diretorio"
git commit -m "docs: documentar parâmetros da função adicionar_documento"
```

**Exemplos de commits ruins (evite):**

```bash
git commit -m "ajustes"
git commit -m "wip"
git commit -m "correção"
```

---

### 3.3 Enviando para o GitHub (push)

```bash
# Enviar sua branch para o repositório remoto
git push origin feat/nome-da-funcionalidade
```

---

### 3.4 Abrindo um Pull Request (PR)

1. Acesse o repositório no GitHub
2. Clique em **"Compare & pull request"**
3. Preencha o título seguindo o mesmo padrão dos commits
4. Na descrição, inclua:
   - O que foi feito
   - Por que foi feito
   - Como testar a mudança
5. Clique em **"Create pull request"**

**Exemplo de descrição de PR:**

```
## O que foi feito
Implementada a funcionalidade de exportação do acervo para CSV.

## Por que
Facilita a integração com ferramentas externas de análise de dados.

## Como testar
python biblioteca.py exportar --saida acervo.csv
Verificar se o arquivo acervo.csv foi gerado com as colunas corretas.
```

---

## 4. Boas práticas de código

- Siga a **PEP 8** (estilo de código Python)
- Adicione **docstrings** em todas as funções novas
- Escreva **testes** para toda nova funcionalidade
- Rode os testes antes de abrir o PR:

```bash
python -m unittest test_biblioteca -v
```

---

## 5. Revisão e merge

- Todo PR será revisado antes de ser integrado à `main`
- Responda aos comentários de revisão com clareza
- Após aprovação, o merge será feito via **"Squash and merge"** para manter o histórico limpo
