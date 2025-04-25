from flask import Flask, render_template, request, session, redirect, url_for
from random import randint

app = Flask(__name__)
app.secret_key = 'очень_секретный_ключ'  # нужен для работы session

def is_valid(n, num):
    return num.isdigit() and n.isdigit() and 1 <= int(n) <= int(num)

@app.route('/', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        num = request.form.get('num')
        if num and num.isdigit():
            session['num'] = int(num)
            session['x'] = randint(1, int(num))
            session['ctr'] = 1
            return redirect(url_for('guess'))
        else:
            return render_template('start.html', error='Не балуйся! Введи число)')
    return render_template('start.html')

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    if 'x' not in session:
        return redirect(url_for('start'))

    num = str(session['num'])
    message = ''
    
    if request.method == 'POST':
        n = request.form.get('n')
        if not is_valid(n, num):
            message = 'А может быть все-таки введем целое число в рамках диапазона?'
        else:
            n = int(n)
            x = session['x']
            if n == x:
                return redirect(url_for('win'))
            elif n < x:
                message = 'Ваше число меньше загаданного, попробуйте еще разок'
            else:
                message = 'Ваше число больше загаданного, попробуйте еще разок'
            session['ctr'] += 1

    return render_template('guess.html', message=message, ctr=session['ctr'])

@app.route('/win')
def win():
    attempts = session.get('ctr', 0)
    return render_template('win.html', attempts=attempts)

@app.route('/restart', methods=['POST'])
def restart():
    session.clear()
    return redirect(url_for('start'))

if __name__ == '__main__':
    app.run(debug=True)