from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Pengguna(db.Model):
    """Model untuk menyimpan data pengguna"""
    __tablename__ = 'pengguna'
    
    id = db.Column(db.Integer, primary_key=True)
    nama_belakang = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    kata_sandi_hash = db.Column(db.String(255), nullable=False)
    dibuat_di = db.Column(db.DateTime, default=datetime.utcnow)
    diperbarui_di = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    akun = db.relationship('Akun', back_populates='pemilik', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash dan simpan password"""
        self.kata_sandi_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifikasi password"""
        return check_password_hash(self.kata_sandi_hash, password)

class Akun(db.Model):
    """Model untuk menyimpan data akun pengguna"""
    __tablename__ = 'akun'
    
    id = db.Column(db.Integer, primary_key=True)
    tipe_akun = db.Column(db.String(255), nullable=False)
    nomor_akun = db.Column(db.String(255), unique=True, nullable=False)
    keseimbangan = db.Column(db.DECIMAL(10, 2), nullable=False, default=0.00)
    pengguna_id = db.Column(db.Integer, db.ForeignKey('pengguna.id'), nullable=False)
    dibuat_di = db.Column(db.DateTime, default=datetime.utcnow)
    diperbarui_di = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    pemilik = db.relationship('Pengguna', back_populates='akun')
    transaksi_keluar = db.relationship('Transaksi', 
                                     foreign_keys='Transaksi.dari_akun_id',
                                     back_populates='dari_akun')
    transaksi_masuk = db.relationship('Transaksi',
                                    foreign_keys='Transaksi.ke_akun_id',
                                    back_populates='ke_akun')

class Transaksi(db.Model):
    """Model untuk menyimpan data transaksi"""
    __tablename__ = 'transaksi'
    
    id = db.Column(db.Integer, primary_key=True)
    jumlah = db.Column(db.DECIMAL(10, 2), nullable=False)
    jenis = db.Column(db.String(50), nullable=False)
    keterangan = db.Column(db.String(255))
    dari_akun_id = db.Column(db.Integer, db.ForeignKey('akun.id'))
    ke_akun_id = db.Column(db.Integer, db.ForeignKey('akun.id'))
    dibuat_di = db.Column(db.DateTime, default=datetime.utcnow)
    
    dari_akun = db.relationship('Akun', foreign_keys=[dari_akun_id], back_populates='transaksi_keluar')
    ke_akun = db.relationship('Akun', foreign_keys=[ke_akun_id], back_populates='transaksi_masuk')
