from flask import Flask, render_template, request, redirect, session, flash, url_for
import mysql.connector


app = Flask(__name__)   # para iniciar o Flask
app.secret_key = 'impacta'


# variável conexão com db
con = mysql.connector.connect(host="localhost", database="livraria_aclmr",
                              user="root", password="**********")

cursor = con.cursor()   # cursor para executar os comandos para o db

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Roberta", "roberta", "impacta1")
usuario2 = Usuario("Catia", "catia", "impacta2")
usuario3 = Usuario("Marco", "marco", "impacta3")
usuario4 = Usuario("Lucas", "lucas", "impacta4")
usuario5 = Usuario("Anderson", "anderson", "impacta5")

usuarios = {usuario1.nickname : usuario1, usuario2.nickname : usuario2,
             usuario3.nickname : usuario3, usuario4.nickname : usuario4,
             usuario5.nickname : usuario5}


@app.route("/")   # rota para a página inicial (homepage)
def index():   # função para pág homepage
    return render_template("index.html")  # caminho p arq html pas templates


@app.route("/contato")   # rota para a página contatos
def contato():           # função para pág contato
    return render_template("contato.html")  # caminho p arq html past templates


@app.route("/cadastro_produtos")   # rota para a página de cadastro dos livros
def cadastro_produtos():   # função para pág cadastro dos livros
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login_colaborador'))
    return render_template('cadastro_produtos.html')


@app.route("/cadastro_clientes")   # rota para a página de cadastro de clientes
def cadastro_clientes():           # função para pág cadastro dos clientes
    return render_template("cadastro_clientes.html")
# caminho para o arquivo html na pasta templates

@app.route("/add_cliente", methods=["POST", "GET"])
def add_cliente():
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    endereco = request.form.get('endereco')
    telefone = request.form.get('telefone')
    comando = f'INSERT INTO cadastro_cliente (nome_cliente, cpf_cliente,\
                    email_cliente, endereco_cliente, telefone_cliente) VALUES ("{nome}",{cpf},\
                                                        "{email}","{endereco}", {telefone})'
    cursor.execute(comando)  # executa o comando SQL acima
    con.commit()  # edita o db
    flash('Cliente incluído com sucesso')
    return redirect(url_for('cadastro_clientes'))

@app.route("/consulta_clientes")   # rota para a página de consulta de estoque
def consulta_clientes():           # função para pág consulta de estoque
    comando = f'SELECT * FROM cadastro_cliente'
    cursor.execute(comando)
    resultado = (cursor.fetchall())
    return render_template("consulta_clientes.html", clientes=resultado)

@app.route("/<id>/altera_cliente", methods=['POST','GET'])
def altera_cliente(id):
    comando = f'SELECT * FROM cadastro_cliente WHERE id_cliente = {id}'
    cursor.execute(comando)
    resultado = (cursor.fetchone())
    return render_template("altera_cliente.html", clientes=resultado)


@app.route("/consulta_estoque_total")   # rota para a página de consulta de estoque
def consulta_estoque_total():           # função para pág consulta de estoque
    comando = f'SELECT * FROM cadastro_livro'
    cursor.execute(comando)
    resultado = (cursor.fetchall())
    return render_template("consulta_estoque_total.html", estoque=resultado)

@app.route("/<id>/altera_produto", methods=['POST','GET'])
def altera_produto(id):
    comando = f'SELECT * FROM cadastro_livro WHERE id_livro = {id}'
    cursor.execute(comando)
    resultado = (cursor.fetchone())
    if request.method == 'POST':
        nome = request.form['nome']
        autor = request.form['autor']
        editora = request.form['editora']
        preco = request.form['preco']
        quantidade = request.form['quantidade']
        return redirect(url_for('consulta_estoque_total'))
    return render_template("altera_produto.html", resultado=resultado)

@app.route('/<id>/remove_produto')
def remove_produto(id):
    comando = f'DELETE FROM cadastro_livro WHERE id_livro = {id}'
    cursor.execute(comando)
    con.commit()
    flash('Produto excluído com sucesso')
    return redirect(url_for("consulta_estoque_total"))

@app.route('/<id>/remove_cliente')
def remove_cliente(id):
    comando = f'DELETE FROM cadastro_cliente WHERE id_cliente = {id}'
    cursor.execute(comando)
    con.commit()
    flash('Cliente excluído com sucesso')
    return redirect(url_for("consulta_clientes"))



@app.route("/consulta_estoque_parcial", methods=['POST','GET'])   # rota para a página de consulta de estoque
def consulta_estoque_parcial():
    comando = f'SELECT * FROM cadastro_livro'
    cursor.execute(comando)
    resultado = (cursor.fetchall())
    parametro = request.form.get('parametro')
    return render_template("consulta_estoque_parcial.html", estoque=resultado)


@app.route("/consulta_estoque")   # rota para a página de consulta de estoque
def consulta_estoque():
    return render_template("consulta_estoque.html")


@app.route("/relatorio_vendas")   # rota para a página de relatório de vendas
def relatorio_vendas():           # função para pág relatório de vendas
    return render_template("relatorio_vendas.html")
    # caminho para o arquivo html na pasta templates


@app.route("/area_colaborador")   # rota para a página área do colaborador
def area_colaborador():           # função para pág área do colaborador
    return render_template("area_colaborador.html")
    # caminho para o arquivo html na pasta templates

@app.route('/autenticar_colaborador', methods=['POST', 'GET'])
def autenticar_colaborador():
    if request.form['senha'] == 'alohomora':
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' logado com sucesso!')
        return redirect(url_for('index'))
    else:
        flash('Usuário não logado')
        return redirect(url_for('login_colaborador'))


@app.route('/login_colaborador')
def login_colaborador():
    proxima = request.args.get('proxima')
    return render_template('login_colaborador.html', proxima=proxima)

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))


# rota p pág que recebe dados inseridos na pág cadastro livros
@app.route('/add_data', methods=['post'])
def add_data():   # função para receber os dados da pág cadastro_livros
    nome = request.form.get('nome')
    autor = request.form.get('autor')
    editora = request.form.get('editora')
    preco = request.form.get('preco')
    quantidade = request.form.get('quantidade')
    comando = f'INSERT INTO cadastro_livro (nome_livro, autor_livro,\
                editora_livro, preco_livro, qtidade_livro) VALUES ("{nome}","{autor}",\
                                                    "{editora}",{preco}, {quantidade})'
    cursor.execute(comando)   # executa o comando SQL acima
    con.commit()   # edita o db
    flash('Produto incluído com sucesso')
    return redirect(url_for('cadastro_produtos'))


# resultado = cursor.fetchall() # ler o db


if __name__ == "__main__":    # instrução para rodar a página quando for "main"
    app.run(debug=True)       # rodar

cursor.close()   # encerrar a conexão
con.close()

debug = True

