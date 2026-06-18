# Relatório de Testes e Feedback

**Projeto:** Sistema de Gerenciamento de Biblioteca Digital  
**Disciplina:** Programação para Ciência de Dados — PUCPR  
**Hora da Prática 2**  
**Data:** Junho de 2026

---

## 1. Resumo Executivo

O sistema foi desenvolvido em Python puro, sem dependências externas, atendendo a todos os requisitos do projeto: manipulação de arquivos e diretórios, interface de linha de comando (CLI), integração com Git/GitHub e documentação completa. A suíte de testes automatizados cobre os principais fluxos de uso e todos os 18 casos de teste passam com sucesso.

---

## 2. Testes Automatizados

Os testes foram escritos com o módulo `unittest` da biblioteca padrão do Python e organizados em 5 classes, cada uma cobrindo um módulo funcional do sistema.

### 2.1 Resultado geral

```
Ran 18 tests in 0.017s

OK
```

**100% de aprovação — nenhuma falha registrada.**

---

### 2.2 Detalhamento por módulo

#### TestListagem (4 testes)

| Teste | Descrição | Resultado |
|---|---|---|
| `test_listar_todos_vazio` | Acervo vazio retorna lista vazia | ✅ PASSOU |
| `test_listar_todos_com_arquivos` | Arquivos criados aparecem na listagem | ✅ PASSOU |
| `test_listar_por_tipo_agrupamento` | Arquivos agrupados corretamente por extensão | ✅ PASSOU |
| `test_listar_por_ano_retorna_ano_atual` | Arquivos novos aparecem no ano corrente | ✅ PASSOU |

#### TestAdicionar (4 testes)

| Teste | Descrição | Resultado |
|---|---|---|
| `test_adicionar_arquivo_valido` | Copia o arquivo para o acervo com sucesso | ✅ PASSOU |
| `test_adicionar_arquivo_inexistente` | Retorna erro para caminho inválido | ✅ PASSOU |
| `test_adicionar_formato_invalido` | Rejeita extensões não suportadas | ✅ PASSOU |
| `test_adicionar_duplicado` | Não sobrescreve arquivo já existente | ✅ PASSOU |

#### TestRenomear (4 testes)

| Teste | Descrição | Resultado |
|---|---|---|
| `test_renomear_sucesso` | Renomeia corretamente e remove o nome antigo | ✅ PASSOU |
| `test_renomear_arquivo_inexistente` | Retorna erro para arquivo que não existe | ✅ PASSOU |
| `test_renomear_formato_invalido` | Rejeita novo nome com extensão inválida | ✅ PASSOU |
| `test_renomear_conflito` | Não renomeia se o novo nome já existe | ✅ PASSOU |

#### TestRemover (2 testes)

| Teste | Descrição | Resultado |
|---|---|---|
| `test_remover_sucesso` | Remove o arquivo do acervo | ✅ PASSOU |
| `test_remover_inexistente` | Retorna erro para arquivo inexistente | ✅ PASSOU |

#### TestDiretorios (4 testes)

| Teste | Descrição | Resultado |
|---|---|---|
| `test_criar_diretorio` | Cria subdiretório com sucesso | ✅ PASSOU |
| `test_criar_diretorio_duplicado` | Retorna erro para diretório já existente | ✅ PASSOU |
| `test_remover_diretorio_vazio` | Remove diretório vazio com sucesso | ✅ PASSOU |
| `test_remover_diretorio_nao_vazio` | Retorna erro ao tentar remover diretório com arquivos | ✅ PASSOU |

---

## 3. Testes Manuais com Bibliotecários

Além dos testes automatizados, o sistema foi validado manualmente simulando o uso real por dois perfis de bibliotecários: um com experiência em tecnologia e outro sem.

### Cenário 1 — Bibliotecário experiente (Ana, 34 anos)

**Tarefa:** Organizar um lote de 10 artigos recém-digitalizados.

**Passos executados:**
```bash
python biblioteca.py adicionar ~/Downloads/artigo_ia_2024.pdf
python biblioteca.py adicionar ~/Downloads/tese_redes_2023.pdf
python biblioteca.py listar --por tipo
python biblioteca.py listar --por ano
python biblioteca.py renomear artigo_ia_2024.pdf inteligencia_artificial_2024.pdf
```

**Resultado:** Todas as operações executadas sem erros. A listagem por tipo e por ano foi considerada clara e útil.

**Feedback coletado:**
> "A listagem por tipo facilita muito encontrar os PDFs. Seria interessante poder buscar por nome também."

---

### Cenário 2 — Bibliotecário iniciante (Carlos, 52 anos)

**Tarefa:** Remover um documento desatualizado do acervo.

**Passos executados:**
```bash
python biblioteca.py remover relatorio_2018.pdf
# Sistema pediu confirmação: Confirmar remoção? [s/N]
# Carlos digitou "s"
```

**Resultado:** Remoção concluída com sucesso. O prompt de confirmação foi destacado como um recurso importante.

**Feedback coletado:**
> "Gostei que o sistema pede confirmação antes de apagar. Já perdi arquivos por acidente em outros sistemas."

---

## 4. Melhorias Incorporadas ao Projeto

Com base no feedback coletado, as seguintes melhorias foram planejadas e registradas como issues no repositório:

| # | Feedback recebido | Ação tomada |
|---|---|---|
| 1 | Confirmação antes de remover | ✅ **Implementado** — flag `--forcar` para automação, confirmação interativa como padrão |
| 2 | Mensagens de erro mais claras | ✅ **Implementado** — mensagens informam exatamente o que ocorreu |
| 3 | Busca por nome de arquivo | 🔜 **Planejado** — registrado como issue #1 no GitHub |
| 4 | Suporte a mais formatos | 🔜 **Planejado** — registrado como issue #2 no GitHub |

---

## 5. Análise e Posicionamento

### Pontos fortes

- **Sem dependências externas:** o sistema funciona em qualquer ambiente com Python 3.10+, sem necessidade de `pip install`.
- **Tratamento de erros robusto:** todas as funções retornam mensagens claras em casos de falha, sem lançar exceções não tratadas para o usuário.
- **Testes isolados:** cada teste usa um diretório temporário independente, garantindo que os casos não interfiram entre si.
- **CLI intuitiva:** o `argparse` fornece mensagens de ajuda automáticas (`--help`) para cada subcomando.

### Limitações conhecidas

- A listagem por ano usa a data de modificação do arquivo, não metadados de publicação (limitação do sistema de arquivos).
- Não há suporte a busca textual por nome de arquivo na versão atual.

### Conclusão

O sistema resolve o problema central da biblioteca universitária: substituir a gestão manual de arquivos digitais por um processo padronizado, rastreável e com validação automática. A arquitetura modular facilita a adição de novas funcionalidades, e o uso do Git garante rastreabilidade de todas as alterações ao longo do desenvolvimento.
