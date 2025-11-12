# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, aggiungi_appuntamento, get_appuntamenti_giorno, get_appuntamenti_settimana
from datetime import datetime, timedelta  # timedelta necessario nei template

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Inizializza il DB al primo avvio
init_db()

@app.route('/')
def index():
    oggi = datetime.now().strftime('%Y-%m-%d')
    return redirect(url_for('giorno', data=oggi))

@app.route('/giorno/<data>')
def giorno(data):
    try:
        data_obj = datetime.strptime(data, '%Y-%m-%d')
    except:
        flash("Data non valida")
        return redirect(url_for('index'))

    appuntamenti = get_appuntamenti_giorno(data)
    return render_template(
        'giorno.html',
        data=data_obj,
        appuntamenti=appuntamenti,
        timedelta=timedelta
    )

@app.route('/settimana/<data>')
def settimana(data):
    try:
        lunedi = datetime.strptime(data, '%Y-%m-%d')
        lunedi = lunedi - timedelta(days=lunedi.weekday())
    except:
        flash("Data non valida")
        return redirect(url_for('index'))

    giorni = [(lunedi + timedelta(days=i)).date() for i in range(7)]
    appuntamenti = get_appuntamenti_settimana(lunedi.date(), (lunedi + timedelta(days=6)).date())
    
    # Inizializza dizionario: chiave = date, valore = lista appuntamenti
    appuntamenti_per_giorno = {g: [] for g in giorni}
    
    # CORREZIONE: converte app['data'] (stringa) in oggetto date
    for app in appuntamenti:
        data_app = datetime.strptime(app['data'], '%Y-%m-%d').date()
        if data_app in appuntamenti_per_giorno:
            appuntamenti_per_giorno[data_app].append(app)

    return render_template(
        'settimana.html',
        lunedi=lunedi,
        giorni=giorni,
        appuntamenti_per_giorno=appuntamenti_per_giorno,
        timedelta=timedelta
    )

@app.route('/aggiungi', methods=['POST'])
def aggiungi():
    titolo = request.form['titolo'].strip()
    descrizione = request.form['descrizione'].strip()
    data = request.form['data']
    ora = request.form['ora']

    if not titolo or len(descrizione) > 200:
        flash("Titolo obbligatorio, descrizione max 200 caratteri")
        return redirect(request.referrer or url_for('index'))

    try:
        datetime.strptime(data, '%Y-%m-%d')
        datetime.strptime(ora, '%H:%M')
    except:
        flash("Formato data/ora non valido")
        return redirect(request.referrer or url_for('index'))

    aggiungi_appuntamento(titolo, descrizione, data, ora)
    flash("Appuntamento aggiunto!")
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)