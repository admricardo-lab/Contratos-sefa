import os
import json
import sqlite3
from datetime import datetime, date
from flask import Flask, request, jsonify, render_template, g

app = Flask(__name__)
DATABASE = os.environ.get('DATABASE_PATH', 'contratos.db')

# ─── DB HELPERS ───────────────────────────────────────────────────

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.execute('''
        CREATE TABLE IF NOT EXISTS contratos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            contrato        TEXT NOT NULL,
            ug              TEXT,
            cnpj            TEXT,
            fornecedor      TEXT NOT NULL,
            nro_aditivo     TEXT,
            dt_inicio       TEXT,
            dt_fim          TEXT,
            valor_vigente   REAL DEFAULT 0,
            valor_mensal    REAL DEFAULT 0,
            conta_contabil  TEXT,
            descricao_servico TEXT,
            dias_restantes  INTEGER,
            situacao        TEXT,
            criado_em       TEXT DEFAULT (datetime('now','localtime')),
            atualizado_em   TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')
    db.commit()

    # Seed if empty
    count = db.execute('SELECT COUNT(*) FROM contratos').fetchone()[0]
    if count == 0:
        seed_file = os.path.join(os.path.dirname(__file__), 'seed_data.json')
        if os.path.exists(seed_file):
            with open(seed_file, 'r', encoding='utf-8') as f:
                records = json.load(f)
            for r in records:
                db.execute('''
                    INSERT INTO contratos
                    (contrato, ug, cnpj, fornecedor, nro_aditivo, dt_inicio, dt_fim,
                     valor_vigente, valor_mensal, conta_contabil, descricao_servico,
                     dias_restantes, situacao)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''', (
                    r.get('contrato',''), r.get('ug',''), r.get('cnpj',''),
                    r.get('fornecedor',''), r.get('nro_aditivo',''),
                    r.get('dt_inicio'), r.get('dt_fim'),
                    r.get('valor_vigente',0), r.get('valor_mensal',0),
                    r.get('conta_contabil',''), r.get('descricao_servico',''),
                    r.get('dias_restantes'), r.get('situacao','')
                ))
            db.commit()
            print(f'Seeded {len(records)} records.')
    db.close()

def recalc_dias(dt_fim):
    """Recalculate days remaining from today."""
    if not dt_fim:
        return None
    try:
        fim = datetime.strptime(dt_fim[:10], '%Y-%m-%d').date()
        return (fim - date.today()).days
    except Exception:
        return None

def row_to_dict(row):
    d = dict(row)
    # Always recalculate dias_restantes from dt_fim
    d['dias_restantes'] = recalc_dias(d.get('dt_fim'))
    return d

# ─── ROUTES ───────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

# LIST / SEARCH
@app.route('/api/contratos', methods=['GET'])
def list_contratos():
    db = get_db()
    q   = request.args.get('q', '').strip()
    sit = request.args.get('situacao', '').strip()

    sql  = 'SELECT * FROM contratos WHERE 1=1'
    args = []

    if q:
        sql += ''' AND (
            contrato        LIKE ? OR
            fornecedor      LIKE ? OR
            cnpj            LIKE ? OR
            descricao_servico LIKE ? OR
            conta_contabil  LIKE ? OR
            nro_aditivo     LIKE ? OR
            ug              LIKE ?
        )'''
        like = f'%{q}%'
        args += [like]*7

    if sit:
        sql += ' AND situacao = ?'
        args.append(sit)

    sql += ' ORDER BY fornecedor COLLATE NOCASE ASC'

    rows = db.execute(sql, args).fetchall()
    return jsonify([row_to_dict(r) for r in rows])

# CREATE
@app.route('/api/contratos', methods=['POST'])
def create_contrato():
    data = request.json
    db   = get_db()
    cur  = db.execute('''
        INSERT INTO contratos
        (contrato, ug, cnpj, fornecedor, nro_aditivo, dt_inicio, dt_fim,
         valor_vigente, valor_mensal, conta_contabil, descricao_servico,
         dias_restantes, situacao)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        data.get('contrato',''), data.get('ug',''), data.get('cnpj',''),
        data.get('fornecedor',''), data.get('nro_aditivo',''),
        data.get('dt_inicio'), data.get('dt_fim'),
        data.get('valor_vigente',0), data.get('valor_mensal',0),
        data.get('conta_contabil',''), data.get('descricao_servico',''),
        recalc_dias(data.get('dt_fim')), data.get('situacao','NORMAL')
    ))
    db.commit()
    row = db.execute('SELECT * FROM contratos WHERE id=?', (cur.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201

# READ ONE
@app.route('/api/contratos/<int:cid>', methods=['GET'])
def get_contrato(cid):
    db  = get_db()
    row = db.execute('SELECT * FROM contratos WHERE id=?', (cid,)).fetchone()
    if not row:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(row_to_dict(row))

# UPDATE
@app.route('/api/contratos/<int:cid>', methods=['PUT'])
def update_contrato(cid):
    data = request.json
    db   = get_db()
    db.execute('''
        UPDATE contratos SET
            contrato=?, ug=?, cnpj=?, fornecedor=?, nro_aditivo=?,
            dt_inicio=?, dt_fim=?, valor_vigente=?, valor_mensal=?,
            conta_contabil=?, descricao_servico=?, dias_restantes=?,
            situacao=?, atualizado_em=datetime('now','localtime')
        WHERE id=?
    ''', (
        data.get('contrato',''), data.get('ug',''), data.get('cnpj',''),
        data.get('fornecedor',''), data.get('nro_aditivo',''),
        data.get('dt_inicio'), data.get('dt_fim'),
        data.get('valor_vigente',0), data.get('valor_mensal',0),
        data.get('conta_contabil',''), data.get('descricao_servico',''),
        recalc_dias(data.get('dt_fim')), data.get('situacao','NORMAL'),
        cid
    ))
    db.commit()
    row = db.execute('SELECT * FROM contratos WHERE id=?', (cid,)).fetchone()
    if not row:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(row_to_dict(row))

# DELETE
@app.route('/api/contratos/<int:cid>', methods=['DELETE'])
def delete_contrato(cid):
    db = get_db()
    db.execute('DELETE FROM contratos WHERE id=?', (cid,))
    db.commit()
    return jsonify({'ok': True})

# ─── MAIN ─────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
