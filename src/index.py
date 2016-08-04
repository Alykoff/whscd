from bottle import route, run, template, view, get, request, post, response, redirect
import bottle
import uuid
import base64
from scored_parser import get_england_json
from auth import auth_login, auth_pass

ppp = []
def get_uuid():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode('utf-8')
    return r_uuid.replace('=', '')

def check_login(login, pss):
    return login == auth_login and pss == auth_pass

def check_cook():
    print('======')
    print(request.cookies)
    if request.cookies is not None and request.cookies.cook not in ppp:
        redirect('/login')
        abort(401, "Sorry, access denied.")
    return True

@get('/login')
def login_get():
    return """
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>"""

@post('/login')
def login_post():
    global ppp
    print(ppp)
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        if len(ppp) > 10:
            ppp = ppp[5:]
        cook = get_uuid()
        ppp.append(cook)
        response.set_header('Set-Cookie', 'cook=' + cook)
        redirect('/')
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"


@get('/')
@view('index')
def index():
    print(ppp)
    check_cook()
    return dict()

@get('/parse')
def parse():
    check_cook()
    cookie = request.query['cookie']
    res = get_england_json(base64.b64decode(cookie).strip())
    print("ress")
    print(res)
    return res


run(host = 'localhost', port=8080)
