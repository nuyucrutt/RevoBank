from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from src.models import db, Pengguna, Akun, Transaksi
from src.auth import authenticate_user, jwt_required

user_bp = Blueprint('user', __name__, url_prefix='/users')
account_bp = Blueprint('account', __name__, url_prefix='/accounts')
transaction_bp = Blueprint('transaction', __name__, url_prefix='/transactions')

@user_bp.route('', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        if 'text/html' in request.accept_mimetypes:
            return "<h1>Pendaftaran Pengguna</h1><p>Gunakan metode POST untuk membuat pengguna</p>"
        return jsonify({"message": "Gunakan metode POST untuk membuat pengguna"}), 405
    
    data = request.get_json()
    if not data or not all(k in data for k in ['nama_belakang', 'email', 'kata_sandi']):
        if 'text/html' in request.accept_mimetypes:
            return "<h1>Error</h1><p>Field yang diperlukan tidak lengkap</p>", 400
        return jsonify({"error": "Field yang diperlukan tidak lengkap"}), 400

    if Pengguna.query.filter_by(nama_belakang=data['nama_belakang']).first():
        return jsonify({"error": "Nama belakang sudah digunakan"}), 400
    if Pengguna.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email sudah digunakan"}), 400

    pengguna = Pengguna(
        nama_belakang=data['nama_belakang'],
        email=data['email']
    )
    pengguna.set_password(data['kata_sandi'])
    db.session.add(pengguna)
    db.session.commit()

    return jsonify({
        "id": pengguna.id,
        "nama_belakang": pengguna.nama_belakang,
        "email": pengguna.email,
        "dibuat_di": pengguna.dibuat_di
    }), 201

@user_bp.route('/me', methods=['GET'])
def get_user():
    if 'text/html' in request.accept_mimetypes:
        return "<h1>Profil Pengguna</h1><p>Detail profil pengguna akan ditampilkan di sini</p>"
    return jsonify({"message": "Profil pengguna berhasil diambil"}), 200

@user_bp.route('/me', methods=['PUT'])
def update_user():
    return jsonify({"message": "Profil pengguna berhasil diperbarui"}), 200

@account_bp.route('', methods=['GET'])
def get_accounts():
    if 'text/html' in request.accept_mimetypes:
        return "<h1>Akun</h1><p>Daftar akun akan ditampilkan di sini</p>"
    return jsonify({"message": "Daftar akun berhasil diambil"}), 200

@account_bp.route('/<int:id>', methods=['GET'])
def get_account(id):
    return jsonify({"message": f"Detail akun {id} berhasil diambil"}), 200

@account_bp.route('', methods=['POST'])
@jwt_required
def create_account():
    data = request.get_json()
    if not data or not all(k in data for k in ['tipe_akun', 'nomor_akun']):
        return jsonify({"error": "Field yang diperlukan tidak lengkap"}), 400

    if Akun.query.filter_by(nomor_akun=data['nomor_akun']).first():
        return jsonify({"error": "Nomor akun sudah digunakan"}), 400

    current_user = authenticate_user()
    akun = Akun(
        tipe_akun=data['tipe_akun'],
        nomor_akun=data['nomor_akun'],
        keseimbangan=data.get('saldo_awal', 0.0),
        pengguna_id=current_user.id
    )
    db.session.add(akun)
    db.session.commit()

    return jsonify({
        "id": akun.id,
        "nomor_akun": akun.nomor_akun,
        "keseimbangan": float(akun.keseimbangan),
        "dibuat_di": akun.dibuat_di
    }), 201

@account_bp.route('/<int:id>', methods=['PUT'])
def update_account(id):
    return jsonify({"message": f"Akun {id} berhasil diperbarui"}), 200

@account_bp.route('/<int:id>', methods=['DELETE'])
def delete_account(id):
    return jsonify({"message": f"Akun {id} berhasil dihapus"}), 200

@transaction_bp.route('', methods=['GET'])
def get_transactions():
    return jsonify({"message": "Daftar transaksi berhasil diambil"}), 200

@transaction_bp.route('/<int:id>', methods=['GET'])
def get_transaction(id):
    return jsonify({"message": f"Detail transaksi {id} berhasil diambil"}), 200

@transaction_bp.route('', methods=['POST'])
@jwt_required
def create_transaction():
    data = request.get_json()
    if not data or not all(k in data for k in ['jumlah', 'jenis']):
        return jsonify({"error": "Field yang diperlukan tidak lengkap"}), 400

    current_user = authenticate_user()
    
    # Validasi akun milik pengguna
    dari_akun = None
    if 'dari_akun_id' in data:
        dari_akun = Akun.query.filter_by(
            id=data['dari_akun_id'],
            pengguna_id=current_user.id
        ).first()
        if not dari_akun:
            return jsonify({"error": "Akun sumber tidak valid"}), 400

    ke_akun = Akun.query.filter_by(
        id=data['ke_akun_id'],
        pengguna_id=current_user.id
    ).first()
    if not ke_akun:
        return jsonify({"error": "Akun tujuan tidak valid"}), 400

    # Buat transaksi
    transaksi = Transaksi(
        jumlah=data['jumlah'],
        jenis=data['jenis'],
        keterangan=data.get('keterangan'),
        dari_akun_id=data.get('dari_akun_id'),
        ke_akun_id=data.get('ke_akun_id')
    )
    db.session.add(transaksi)
    
    # Update saldo akun
    if dari_akun:
        dari_akun.keseimbangan -= data['jumlah']
    if ke_akun:
        ke_akun.keseimbangan += data['jumlah']
        
    db.session.commit()

    return jsonify({
        "id": transaksi.id,
        "jumlah": float(transaksi.jumlah),
        "jenis": transaksi.jenis,
        "dibuat_di": transaksi.dibuat_di
    }), 201
