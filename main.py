from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Filme(BaseModel):
    id: int
    titulo: str
    genero: str
    ano: int
    nota: int

# Banco de dados em memória
banco_de_filmes: List[Filme] = [
    Filme(id=1, titulo="Inception", genero="Ficção Científica", ano=2010, nota=5),
    Filme(id=2, titulo="O Rei Leão", genero="Animação", ano=1994, nota=5)
]

@app.get("/", response_class=HTMLResponse)
def listar_filmes(edit_id: Optional[int] = None):
    linhas_tabela = ""
    filme_edicao = None

    # Se houver um ID para edição, busca o filme para preencher o formulário
    if edit_id:
        for f in banco_de_filmes:
            if f.id == edit_id:
                filme_edicao = f
                break

    for filme in banco_de_filmes:
        linhas_tabela += f"""
        <tr>
            <td>{filme.titulo}</td>
            <td>{filme.genero}</td>
            <td>{filme.ano}</td>
            <td>{'⭐' * filme.nota}</td>
            <td>
                <a href="/?edit_id={filme.id}" style="color: #ff9800; margin-right: 10px; text-decoration: none; font-weight: bold;">[Editar]</a>
                <a href="/deletar/{filme.id}" style="color: #f44336; text-decoration: none; font-weight: bold;" onclick="return confirm('Tem certeza?')">[Excluir]</a>
            </td>
        </tr>
        """

    # Define o título do formulário e para onde ele vai enviar os dados
    titulo_form = "Editar Filme" if filme_edicao else "Adicionar Novo Filme"
    action_form = f"/editar/{filme_edicao.id}" if filme_edicao else "/adicionar"
    val_titulo = filme_edicao.titulo if filme_edicao else ""
    val_genero = filme_edicao.genero if filme_edicao else ""
    val_ano = filme_edicao.ano if filme_edicao else ""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>CineList - Seu Catálogo de Filmes</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #121212; color: white; padding: 40px; }}
            .container {{ max-width: 900px; margin: 0 auto; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #1e1e1e; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #333; }}
            th {{ background-color: #ff9800; color: black; }}
            .form-box {{ background-color: #1e1e1e; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
            input, select, button {{ padding: 10px; margin: 5px 0; width: 100%; box-sizing: border-box; }}
            button {{ background-color: #ff9800; border: none; font-weight: bold; cursor: pointer; }}
            .cancel-btn {{ background-color: #555; color: white; text-align: center; display: block; padding: 10px; text-decoration: none; font-weight: bold; margin-top: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎬 CineList - Meu Catálogo</h1>
            
            <div class="form-box">
                <h3>{titulo_form}</h3>
                <form action="{action_form}" method="post">
                    <input type="text" name="titulo" placeholder="Título do Filme" value="{val_titulo}" required>
                    <input type="text" name="genero" placeholder="Gênero" value="{val_genero}" required>
                    <input type="number" name="ano" placeholder="Ano de Lançamento" value="{val_ano}" required>
                    <select name="nota">
                        <option value="5">5 Estrelas</option>
                        <option value="4">4 Estrelas</option>
                        <option value="3">3 Estrelas</option>
                        <option value="2">2 Estrelas</option>
                        <option value="1">1 Estrela</option>
                    </select>
                    <button type="submit">Salvar Alterações</button>
                    { '<a href="/" class="cancel-btn">Cancelar Edição</a>' if filme_edicao else '' }
                </form>
            </div>

            <h2>Filmes Cadastrados</h2>
            <table>
                <thead>
                    <tr>
                        <th>Título</th>
                        <th>Gênero</th>
                        <th>Ano</th>
                        <th>Avaliação</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    {linhas_tabela}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return html_content

@app.post("/adicionar")
def adicionar_filme(titulo: str = Form(...), genero: str = Form(...), ano: int = Form(...), nota: int = Form(...)):
    novo_id = max([f.id for f in banco_de_filmes]) + 1 if banco_de_filmes else 1
    novo_filme = Filme(id=novo_id, titulo=titulo, genero=genero, ano=ano, nota=nota)
    banco_de_filmes.append(novo_filme)
    return HTMLResponse(content="<script>window.location.href='/';</script>")

@app.post("/editar/{filme_id}")
def editar_filme(filme_id: int, titulo: str = Form(...), genero: str = Form(...), ano: int = Form(...), nota: int = Form(...)):
    for f in banco_de_filmes:
        if f.id == filme_id:
            f.titulo = titulo
            f.genero = genero
            f.ano = ano
            f.nota = nota
            break
    return HTMLResponse(content="<script>window.location.href='/';</script>")

@app.get("/deletar/{filme_id}")
def deletar_filme(filme_id: int):
    global banco_de_filmes
    banco_de_filmes = [f for f in banco_de_filmes if f.id != filme_id]
    return HTMLResponse(content="<script>window.location.href='/';</script>")