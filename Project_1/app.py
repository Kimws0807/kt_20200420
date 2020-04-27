import os
from flask import Flask
from flask import request, redirect, abort

app = Flask(__name__, static_folder="content")

members = [
    {"id" : "taegeun", "pw" : "10057779"},
    {"id" : "wansoo", "pw" : "10149426"}
]

def get_menu():
    menu_temp = "<li><a href='{0}'>{0}</a></li>"
    menu = [e for e in os.listdir('views') if e[0] != '.']
    return "\n".join([menu_temp.format(m) for m in menu])

def get_template(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        template = f.read()
        
    return template

# def get_page(filename):
#     with open(f'menu/{filename}.html', 'r', encoding="utf-8") as f:
#         template = f.read()
        
#     return template

@app.route("/")
def index():
    with open('template.html', 'r', encoding="utf-8") as f:
        default = f.read()
    return default


@app.route("/<title>")
def html(title):
    template = get_template(title)
    menu = get_menu()

    if title not in menu:
        return abort(404)

    with open(f'views/{title}.html', 'r', encoding="utf-8") as f:
        content = f.read()

    return template.format(title, content, menu)


# @app.route("/create", methods=['GET', 'POST'])
# def create():
#     template = get_template('create.html')
#     menu = get_menu()
    
#     if request.method == 'GET':
#         return template.format('', menu)
    
#     elif request.method == 'POST':
#         with open(f'/{request.form["title"]}', 'w') as f:
#             f.write(request.form['desc'])
            
#         return redirect('/')

@app.route("/login", methods=['GET', 'POST'])
def login():
    template = get_template('login.html')
    menu = get_menu()
    
    if request.method == 'GET':
        return template.format("", menu)
    
    elif request.method =='POST':
        # 회원 검증 방법
        m = [e for e in members if e['id'] == request.form['id']]
        if len(m) == 0:
            return template.format("<p>회원이 아닙니다.</p>", menu)
        
        # PW 검증 방법
        if request.form['pw'] != m[0]['pw']:
            return template.format("<p>패스워드를 확인해 주세요</p>", menu)
        
        # 검증 성공하여 로그인
        return redirect("views/Home?id=" + m[0]['id'])

@app.route("/views/Home")
def main():
    id = request.args.get('id', '')
    template = get_template('views/Home')
    
    title = 'Welcome ' + id + '씨'
    content = """환영합니다."""
    menu = get_menu()
    return template.format(title, content, menu)


@app.route("/views/<title>" , methods=['GET', 'POST'])
def html2(title):
    id = request.args.get('id', '')
    template = get_template('template2.html')
    menu = get_menu()

    with open(f'views/{title}', 'r', encoding="utf-8") as f:
        content = f.read()
    
    if request.method == 'GET':
        return template.format(id, content, menu)

    elif request.method == 'POST':
        with open(f'database/{request.form["subject"]}', 'w', encoding="utf-8") as f:
            f.write(request.form['contents'])
  
    return redirect(f'{title}')


@app.route('/favicon.ico')
def favicon():
    return abort(404)
