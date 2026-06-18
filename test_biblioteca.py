"""
Testes automatizados — Sistema de Gerenciamento de Biblioteca Digital
Disciplina: Programação para Ciência de Dados - PUCPR
"""

import os
import shutil
import tempfile
import unittest

# Aponta o sistema para um diretório temporário durante os testes
import biblioteca as bib


class ConfiguracaoBase(unittest.TestCase):
    """Cria e destrói um diretório temporário de acervo para cada teste."""

    def setUp(self):
        self.dir_original = bib.DIRETORIO_BASE
        self.temp_dir = tempfile.mkdtemp()
        bib.DIRETORIO_BASE = self.temp_dir

    def tearDown(self):
        bib.DIRETORIO_BASE = self.dir_original
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _criar_arquivo(self, nome: str) -> str:
        """Cria um arquivo fictício dentro do acervo temporário."""
        caminho = os.path.join(self.temp_dir, nome)
        with open(caminho, "w") as f:
            f.write("conteúdo de teste")
        return caminho


# ──────────────────────────────────────────────
# Testes de listagem
# ──────────────────────────────────────────────

class TestListagem(ConfiguracaoBase):

    def test_listar_todos_vazio(self):
        """Acervo vazio deve retornar lista vazia."""
        resultado = bib.listar_todos()
        self.assertEqual(resultado, [])

    def test_listar_todos_com_arquivos(self):
        """Deve retornar todos os arquivos criados no acervo."""
        self._criar_arquivo("artigo.pdf")
        self._criar_arquivo("tese.epub")
        resultado = bib.listar_todos()
        self.assertIn("artigo.pdf", resultado)
        self.assertIn("tese.epub", resultado)

    def test_listar_por_tipo_agrupamento(self):
        """Arquivos de diferentes tipos devem ser agrupados corretamente."""
        self._criar_arquivo("a.pdf")
        self._criar_arquivo("b.pdf")
        self._criar_arquivo("c.epub")
        resultado = bib.listar_por_tipo()
        self.assertIn(".pdf", resultado)
        self.assertIn(".epub", resultado)
        self.assertEqual(len(resultado[".pdf"]), 2)
        self.assertEqual(len(resultado[".epub"]), 1)

    def test_listar_por_ano_retorna_ano_atual(self):
        """Arquivos recém-criados devem aparecer no ano corrente."""
        from datetime import datetime
        self._criar_arquivo("novo.pdf")
        resultado = bib.listar_por_ano()
        ano_atual = str(datetime.now().year)
        self.assertIn(ano_atual, resultado)


# ──────────────────────────────────────────────
# Testes de adição
# ──────────────────────────────────────────────

class TestAdicionar(ConfiguracaoBase):

    def test_adicionar_arquivo_valido(self):
        """Deve copiar o arquivo para o acervo com sucesso."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            origem = f.name
        try:
            msg = bib.adicionar_documento(origem)
            self.assertIn("✔", msg)
            nome = os.path.basename(origem)
            self.assertTrue(os.path.exists(os.path.join(self.temp_dir, nome)))
        finally:
            os.unlink(origem)

    def test_adicionar_arquivo_inexistente(self):
        """Deve retornar mensagem de erro para arquivo que não existe."""
        msg = bib.adicionar_documento("/caminho/inexistente/arquivo.pdf")
        self.assertIn("Erro", msg)

    def test_adicionar_formato_invalido(self):
        """Deve rejeitar extensões não suportadas."""
        with tempfile.NamedTemporaryFile(suffix=".xyz", delete=False) as f:
            origem = f.name
        try:
            msg = bib.adicionar_documento(origem)
            self.assertIn("Erro", msg)
        finally:
            os.unlink(origem)

    def test_adicionar_duplicado(self):
        """Não deve sobrescrever arquivo já existente no acervo."""
        self._criar_arquivo("existente.pdf")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            origem = f.name
        # Renomeia o temp para ter o mesmo nome do existente
        destino_temp = origem.replace(os.path.basename(origem), "existente.pdf")
        os.rename(origem, destino_temp)
        try:
            msg = bib.adicionar_documento(destino_temp)
            self.assertIn("Erro", msg)
        finally:
            if os.path.exists(destino_temp):
                os.unlink(destino_temp)


# ──────────────────────────────────────────────
# Testes de renomeação
# ──────────────────────────────────────────────

class TestRenomear(ConfiguracaoBase):

    def test_renomear_sucesso(self):
        """Deve renomear o arquivo corretamente."""
        self._criar_arquivo("antigo.pdf")
        msg = bib.renomear_documento("antigo.pdf", "novo.pdf")
        self.assertIn("✔", msg)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "novo.pdf")))
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "antigo.pdf")))

    def test_renomear_arquivo_inexistente(self):
        """Deve retornar erro ao tentar renomear arquivo que não existe."""
        msg = bib.renomear_documento("fantasma.pdf", "novo.pdf")
        self.assertIn("Erro", msg)

    def test_renomear_formato_invalido(self):
        """Deve rejeitar novo nome com extensão inválida."""
        self._criar_arquivo("documento.pdf")
        msg = bib.renomear_documento("documento.pdf", "documento.xyz")
        self.assertIn("Erro", msg)

    def test_renomear_conflito(self):
        """Não deve renomear se já existe arquivo com o novo nome."""
        self._criar_arquivo("a.pdf")
        self._criar_arquivo("b.pdf")
        msg = bib.renomear_documento("a.pdf", "b.pdf")
        self.assertIn("Erro", msg)


# ──────────────────────────────────────────────
# Testes de remoção de arquivos
# ──────────────────────────────────────────────

class TestRemover(ConfiguracaoBase):

    def test_remover_sucesso(self):
        """Deve remover o arquivo do acervo."""
        self._criar_arquivo("remover.pdf")
        msg = bib.remover_documento("remover.pdf", confirmar=True)
        self.assertIn("✔", msg)
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, "remover.pdf")))

    def test_remover_inexistente(self):
        """Deve retornar erro para arquivo que não existe."""
        msg = bib.remover_documento("nao_existe.pdf", confirmar=True)
        self.assertIn("Erro", msg)


# ──────────────────────────────────────────────
# Testes de diretórios
# ──────────────────────────────────────────────

class TestDiretorios(ConfiguracaoBase):

    def test_criar_diretorio(self):
        """Deve criar o subdiretório com sucesso."""
        msg = bib.criar_diretorio("periódicos")
        self.assertIn("✔", msg)
        self.assertTrue(os.path.isdir(os.path.join(self.temp_dir, "periódicos")))

    def test_criar_diretorio_duplicado(self):
        """Deve retornar erro ao criar diretório que já existe."""
        bib.criar_diretorio("teses")
        msg = bib.criar_diretorio("teses")
        self.assertIn("Erro", msg)

    def test_remover_diretorio_vazio(self):
        """Deve remover diretório vazio com sucesso."""
        bib.criar_diretorio("vazio")
        msg = bib.remover_diretorio("vazio", confirmar=True)
        self.assertIn("✔", msg)

    def test_remover_diretorio_nao_vazio(self):
        """Deve retornar erro ao tentar remover diretório com conteúdo."""
        sub = os.path.join(self.temp_dir, "cheio")
        os.makedirs(sub)
        with open(os.path.join(sub, "arquivo.pdf"), "w") as f:
            f.write("x")
        msg = bib.remover_diretorio("cheio", confirmar=True)
        self.assertIn("Erro", msg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
