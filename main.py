from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Representação em Orientação a Objetos do Filme
class Filme(BaseModel):
    id: int
    titulo: str
    genero: str
    ano: int
    nota: int

# Banco de dados simulado na memória
banco_de_filmes: List[Filme] = [
    Filme(id=1, titulo="Inception", genero="Ficção Científica", ano=2010, nota=5),
    Filme(id=2, titulo="O Rei Leão", genero="Animação", ano=1994, nota=5)
]

@app.get("/", response_class=HTMLResponse)
def listar_filmes():
    # Gerando a tabela de filmes dinamicamente
    linhas_tabela = ""
    for filme in banco_de_filmes:
        linhas_tabela += f"""
        <tr>
            <td>{filme.titulo}</td>
            <td>{filme.genero}</td>
            <td>{filme.ano}</td>
            <td>{'⭐' * filme.nota}</td>
        </tr>
        """

    # HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>CineList - Seu Catálogo de Filmes</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #121212; color: white; padding: 40px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #1e1e1e; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #333; }}
            th {{ background-color: #ff9800; color: black; }}
            .form-box {{ background-color: #1e1e1e; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
            input, select, button {{ padding: 10px; margin: 5px 0; width: 100%; box-sizing: border-box; }}
            button {{ background-color: #ff9800; border: none; font-weight: bold; cursor: pointer; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎬 CineList - Meu Catálogo</h1>
            
            <div class="form-box">
                <h3>Adicionar Novo Filme</h3>
                <form action="/adicionar" method="post">
                    <input type="text" name="titulo" placeholder="Título do Filme" required>
                    <input type="text" name="genero" placeholder="Gênero" required>
                    <input type="number" name="ano" placeholder="Ano de Lançamento" required>
                    <select name="nota">
                        <option value="5">5 Estrelas</option>
                        <option value="4">4 Estrelas</option>
                        <option value="3">3 Estrelas</option>
                        <option value="2">2 Estrelas</option>
                        <option value="1">1 Estrela</option>
                    </select>
                    <button type="submit">Salvar Filme</button>
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
    novo_id = len(banco_de_filmes) + 1
    # Criando o objeto da classe Filme (Orientação a Objetos)
    novo_filme = Filme(id=novo_id, titulo=titulo, genero=genero, ano=ano, nota=nota)
    banco_de_filmes.append(novo_filme)
    
    # Redireciona de volta para a página inicial atualizada
    return HTMLResponse(content="<script>window.location.href='/';</script>")