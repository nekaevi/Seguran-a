from flask import Flask, render_template, request, session, redirect, url_for, make_response
from flask_wtf.csrf import CSRFProtect
import secrets
from markupsafe import escape

app = Flask(__name__)

# Configurações de segurança
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Chave secreta forte
app.config['SESSION_COOKIE_SECURE'] = True  # Envia cookies apenas sobre HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Impede acesso JavaScript aos cookies de sessão
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Proteção contra CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Sessão expira em 1 hora

# Habilitar CSRF Protection globalmente
csrf = CSRFProtect(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Processar o formulário com proteção CSRF (automática via Flask-WTF)
        username = escape(request.form.get('username', ''))  # Proteção XSS com escape
        message = escape(request.form.get('message', ''))
        
        # Aqui você processaria os dados com segurança
        # Por exemplo, salvar no banco de dados
        
        return render_template('index.html', 
                             username=username, 
                             message=message,
                             success="Mensagem enviada com sucesso!")
    
    return render_template('index.html')

@app.route('/logout')
def logout():
    # Limpar a sessão de forma segura
    session.clear()
    response = make_response(redirect(url_for('index')))
    # Configurar cookies de segurança
    response.set_cookie('session', '', expires=0, secure=True, httponly=True, samesite='Lax')
    return response

if __name__ == '__main__':
    app.run(debug=True)  # Em produção, defina debug=False