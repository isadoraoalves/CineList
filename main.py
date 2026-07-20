from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class Usuario(BaseModel):
    nome: str
    email: str
    senha: str

class Filme(BaseModel):
    id: int
    titulo: str
    genero: str
    ano: int
    nota: int
    usuario_email: str


banco_usuarios: List[Usuario] = [
    Usuario(nome="Isadora", email="isa@email.com", senha="123")
]

banco_de_filmes: List[Filme] = [
    Filme(id=1, titulo="Inception", genero="Ficção Científica", ano=2010, nota=5, usuario_email="isa@email.com"),
    Filme(id=2, titulo="O Rei Leão", genero="Animação", ano=1994, nota=5, usuario_email="isa@email.com"),
    Filme(id=3, titulo="Interstellar", genero="Ficção Científica", ano=2014, nota=5, usuario_email="isa@email.com")
]


usuario_logado: Optional[Usuario] = banco_usuarios[0]

@app.get("/", response_class=HTMLResponse)
def home(edit_id: Optional[int] = None, genero_filtro: Optional[str] = None):
    # Se não estiver logado, redireciona para a tela de login
    if not usuario_logado:
        return HTMLResponse(content="<script>window.location.href='/login-page';</script>")

    
    meus_filmes = [f for f in banco_de_filmes if f.usuario_email == usuario_logado.email]

    # Lógica do Dashboard
    total_filmes = len(meus_filmes)
    soma_notas = sum([f.nota for f in meus_filmes])
    media_notas = round(soma_notas / total_filmes, 1) if total_filmes > 0 else 0.0

   
    filmes_exibidos = meus_filmes
    if genero_filtro and genero_filtro.strip() != "":
        filmes_exibidos = [f for f in meus_filmes if genero_filtro.lower() in f.genero.lower()]

  
    filme_edicao = None
    if edit_id:
        for f in meus_filmes:
            if f.id == edit_id:
                filme_edicao = f
                break

    # Montagem da Tabela
    linhas_tabela = ""
    for filme in filmes_exibidos:
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
            .top-bar {{ display: flex; justify-content: space-between; align-items: center; background: #1e1e1e; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
            .dash-cards {{ display: flex; gap: 20px; margin-bottom: 20px; }}
            .card {{ flex: 1; background: #1e1e1e; padding: 15px; border-radius: 5px; border-left: 5px solid #ff9800; text-align: center; }}
            .card h2 {{ margin: 5px 0 0 0; color: #ff9800; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; background-color: #1e1e1e; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #333; }}
            th {{ background-color: #ff9800; color: black; }}
            .form-box {{ background-color: #1e1e1e; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
            input, select, button {{ padding: 10px; margin: 5px 0; width: 100%; box-sizing: border-box; }}
            button {{ background-color: #ff9800; border: none; font-weight: bold; cursor: pointer; }}
            .filter-box {{ display: flex; gap: 10px; margin-bottom: 15px; }}
            .cancel-btn {{ background-color: #555; color: white; text-align: center; display: block; padding: 10px; text-decoration: none; font-weight: bold; margin-top: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="top-bar">
                <h1 style="margin:0;">🎬 CineList</h1>
                <div>Usuário: <strong>{usuario_logado.nome}</strong> | <a href="/logout" style="color:#ff9800; text-decoration:none;">Sair</a></div>
            </div>

            <!-- DASHBOARD -->
            <div class="dash-cards">
                <div class="card">
                    <small>Total de Filmes</small>
                    <h2>{total_filmes}</h2>
                </div>
                <div class="card">
                    <small>Média das Avaliações</small>
                    <h2>{media_notas} ⭐</h2>
                </div>
            </div>

            <!-- FORMULÁRIO -->
            <div class="form-box">
                <h3>{titulo_form}</h3>
                <form action="{action_form}" method="post">
                    <input type="text" name="titulo" placeholder="Título do Filme" value="{val_titulo}" required>
                    <input type="text" name="genero" placeholder="Gênero (Ex: Ação, Comédia)" value="{val_genero}" required>
                    <input type="number" name="ano" placeholder="Ano de Lançamento" value="{val_ano}" required>
                    <select name="nota">
                        <option value="5">5 Estrelas</option>
                        <option value="4">4 Estrelas</option>
                        <option value="3">3 Estrelas</option>
                        <option value="2">2 Estrelas</option>
                        <option value="1">1 Estrela</option>
                    </select>
                    <button type="submit">Salvar Registro</button>
                    { '<a href="/" class="cancel-btn">Cancelar Edição</a>' if filme_edicao else '' }
                </form>
            </div>

            <!-- FILTRO DE FILMES -->
            <h2>Filmes no Catálogo</h2>
            <form action="/" method="get" class="filter-box">
                <input type="text" name="genero_filtro" placeholder="Filtrar por gênero..." value="{genero_filtro or ''}">
                <button type="submit" style="width: 150px;">Filtrar</button>
                <a href="/" class="cancel-btn" style="width: 100px; margin:5px 0;">Limpar</a>
            </form>

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
                    {linhas_tabela if linhas_tabela else '<tr><td colspan="5">Nenhum filme encontrado.</td></tr>'}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return html_content

# --- ROTAS DE AUTENTICAÇÃO REAL ---

@app.get("/login-page", response_class=HTMLResponse)
def login_page(erro: Optional[str] = None):
    msg_erro = f"<p style='color:#f44336;'>{erro}</p>" if erro else ""
    return f"""
    <html>
    <head><title>CineList - Login</title></head>
    <body style='background:#121212; color:white; font-family:Arial; padding:50px; text-align:center;'>
        <div style='max-width:350px; margin:0 auto; background:#1e1e1e; padding:30px; border-radius:8px;'>
            <h2>🎬 Entrar no CineList</h2>
            {msg_erro}
            <form action='/login' method='post'>
                <input type='email' name='email' placeholder='Seu E-mail' required style='width:100%; padding:10px; margin:8px 0; box-sizing:border-box;'><br>
                <input type='password' name='senha' placeholder='Sua Senha' required style='width:100%; padding:10px; margin:8px 0; box-sizing:border-box;'><br>
                <button type='submit' style='width:100%; padding:10px; background:#ff9800; border:none; font-weight:bold; cursor:pointer; margin-top:10px;'>Acessar Conta</button>
            </form>
            <p style='font-size:14px; margin-top:15px;'>Ainda não tem conta? <a href='/cadastro-page' style='color:#ff9800;'>Cadastre-se</a></p>
        </div>
    </body>
    </html>
    """

@app.post("/login")
def login(email: str = Form(...), senha: str = Form(...)):
    global usuario_logado
    for u in banco_usuarios:
        if u.email == email and u.senha == senha:
            usuario_logado = u
            return HTMLResponse(content="<script>window.location.href='/';</script>")
    return HTMLResponse(content="<script>window.location.href='/login-page?erro=E-mail ou senha incorretos!';</script>")

@app.get("/cadastro-page", response_class=HTMLResponse)
def cadastro_page():
    return """
    <html>
    <head><title>CineList - Cadastro</title></head>
    <body style='background:#121212; color:white; font-family:Arial; padding:50px; text-align:center;'>
        <div style='max-width:350px; margin:0 auto; background:#1e1e1e; padding:30px; border-radius:8px;'>
            <h2>🎬 Criar Conta</h2>
            <form action='/cadastrar' method='post'>
                <input type='text' name='nome' placeholder='Seu Nome' required style='width:100%; padding:10px; margin:8px 0; box-sizing:border-box;'><br>
                <input type='email' name='email' placeholder='Seu E-mail' required style='width:100%; padding:10px; margin:8px 0; box-sizing:border-box;'><br>
                <input type='password' name='senha' placeholder='Sua Senha' required style='width:100%; padding:10px; margin:8px 0; box-sizing:border-box;'><br>
                <button type='submit' style='width:100%; padding:10px; background:#ff9800; border:none; font-weight:bold; cursor:pointer; margin-top:10px;'>Cadastrar</button>
            </form>
            <p style='font-size:14px; margin-top:15px;'>Já tem uma conta? <a href='/login-page' style='color:#ff9800;'>Fazer Login</a></p>
        </div>
    </body>
    </html>
    """

@app.post("/cadastrar")
def cadastrar(nome: str = Form(...), email: str = Form(...), senha: str = Form(...)):
    global usuario_logado
    novo_user = Usuario(nome=nome, email=email, senha=senha)
    banco_usuarios.append(novo_user)
    usuario_logado = novo_user
    return HTMLResponse(content="<script>window.location.href='/';</script>")

@app.get("/logout")
def logout():
    global usuario_logado
    usuario_logado = None
    return HTMLResponse(content="<script>window.location.href='/login-page';</script>")

# --- ROTAS DO CRUD DE FILMES ---

@app.post("/adicionar")
def adicionar_filme(titulo: str = Form(...), genero: str = Form(...), ano: int = Form(...), nota: int = Form(...)):
    if not usuario_logado:
        return HTMLResponse(content="<script>window.location.href='/login-page';</script>")
    novo_id = max([f.id for f in banco_de_filmes]) + 1 if banco_de_filmes else 1
    novo_filme = Filme(id=novo_id, titulo=titulo, genero=genero, ano=ano, nota=nota, usuario_email=usuario_logado.email)
    banco_de_filmes.append(novo_filme)
    return HTMLResponse(content="<script>window.location.href='/';</script>")

@app.post("/editar/{filme_id}")
def editar_filme(filme_id: int, titulo: str = Form(...), genero: str = Form(...), ano: int = Form(...), nota: int = Form(...)):
    if not usuario_logado:
        return HTMLResponse(content="<script>window.location.href='/login-page';</script>")
    for f in banco_de_filmes:
        if f.id == filme_id and f.usuario_email == usuario_logado.email:
            f.titulo = titulo
            f.genero = genero
            f.ano = ano
            f.nota = nota
            break
    return HTMLResponse(content="<script>window.location.href='/';</script>")

@app.get("/deletar/{filme_id}")
def deletar_filme(filme_id: int):
    global banco_de_filmes
    if not usuario_logado:
        return HTMLResponse(content="<script>window.location.href='/login-page';</script>")
    banco_de_filmes = [f for f in banco_de_filmes if not (f.id == filme_id and f.usuario_email == usuario_logado.email)]
    return HTMLResponse(content="<script>window.location.href='/';</script>")