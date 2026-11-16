from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_kaskelas' # Diperlukan untuk fitur login session

DAFTAR_SISWA = [
    "Risky", "Hikmal", "Alfian", "Ardi", "Ares", "Bagus", "Berliana", 
    "Danish", "Aldi", "Clara", "Zaki", "Nopal", "Fazry", "Galeh", 
    "Haped", "Isa", "Oliv", "Aska", "Zidan", "Mayliza", "Sandy", 
    "Raffi", "Ajam", "Fitra", "Sanu", "Nizar", "Ima", "Penta", 
    "Radit", "Reza", "Nisa", "Sukma", "Thomas", "Tsani", "Zakina"
]

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS kas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            bulan TEXT,
            minggu INTEGER,
            status TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pengeluaran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keterangan TEXT,
            jumlah INTEGER
        )
    ''')
    
    cek_data = conn.execute('SELECT COUNT(*) FROM kas').fetchone()[0]
    if cek_data == 0:
        for nama in DAFTAR_SISWA:
            for minggu in range(1, 5):
                conn.execute('INSERT INTO kas (nama, bulan, minggu, status) VALUES (?, ?, ?, ?)',
                             (nama, 'November', minggu, 'Belum'))
    conn.commit()
    conn.close()

# Halaman Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Akun login sederhana untuk bendahara
        if username == 'kasyuk' and password == '123':
            session['user'] = username
            return redirect(url_for('index'))
        else:
            error = 'Username atau Password salah!'
    return render_template('login.html', error=error)

# Halaman Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Halaman Utama (Dashboard) - Harus Login dulu
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    pilih_bulan = request.args.get('bulan', 'November')
    pilih_minggu = request.args.get('minggu', '1')
    
    data_kas = conn.execute(
        'SELECT * FROM kas WHERE bulan = ? AND minggu = ?', 
        (pilih_bulan, pilih_minggu)
    ).fetchall()
    
    data_keluar = conn.execute('SELECT * FROM pengeluaran').fetchall()
