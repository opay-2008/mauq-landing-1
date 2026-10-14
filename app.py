"""
COURTLINE — Landing page toko sneakers & perlengkapan basket (Flask)

Struktur sama seperti project perkenalan-diri-python:
  app.py            -> logika & data (produk, kategori, form newsletter)
  templates/        -> tampilan HTML (MAUQ.TECH)
  static/style.css  -> gaya tampilan
  data/             -> dibuat otomatis, menyimpan email pendaftar (JSON)

Cara menjalankan:
    pip install -r requirements.txt
    python app.py
Lalu buka: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import datetime

app = Flask(__name__, static_folder="public", static_url_path="")
app.secret_key = "ganti-dengan-kunci-rahasia-kamu"  # ganti sebelum dipublikasikan

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = "/tmp" if os.environ.get("VERCEL") else os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
# =========================================================
# EDIT DATA TOKO DI SINI
# =========================================================
BRAND = {
    "nama": "MAUQ",
    "tagline": "Gear buat yang hidup di lapangan.",
    "email": "halo@mauq.tech",
    "whatsapp": "+62 822-5134-2682",
     "wa_nomor": "6282251342682",
}

KATEGORI = [
    {"icon": "👟", "nama": "Sneakers"},
    {"icon": "🏀", "nama": "Basket"},
    {"icon": "👕", "nama": "Jersey & Apparel"},
    {"icon": "🎒", "nama": "Aksesoris"},
    {"icon": "🔥", "nama": "Sale"},
]

PRODUK = [
    {"icon": "👟", "nama": "Aero Court Low", "kategori": "Sneakers", "harga": 1599000, "badge": "Baru", "warna": "#ff6b1a"},
    {"icon": "🏀", "nama": "Pro Grip Indoor Ball", "kategori": "Basket", "harga": 459000, "badge": "Terlaris", "warna": "#1f6feb"},
    {"icon": "👕", "nama": "Tipoff Reversible Jersey", "kategori": "Jersey", "harga": 399000, "badge": "", "warna": "#e11d48"},
    {"icon": "👟", "nama": "Skyline High Pro", "kategori": "Sneakers", "harga": 1899000, "badge": "Sale 20%", "warna": "#16a34a"},
    {"icon": "🎒", "nama": "Duffle Game Day 40L", "kategori": "Aksesoris", "harga": 649000, "badge": "", "warna": "#7c3aed"},
    {"icon": "🧦", "nama": "Crew Socks 3-Pack", "kategori": "Aksesoris", "harga": 149000, "badge": "Terlaris", "warna": "#0891b2"},
]

KEUNGGULAN = [
    ("✅", "100% Original", "Semua produk bergaransi keaslian."),
    ("🚚", "Gratis Ongkir", "Untuk pembelian di atas Rp1.000.000."),
    ("🔄", "Tukar 14 Hari", "Ukuran tidak pas? Tukar tanpa ribet."),
    ("💬", "Chat Cepat", "Tim kami siap bantu pilih ukuran."),
]
# =========================================================


@app.template_filter("rupiah")
def rupiah(n):
    return "Rp" + f"{n:,}".replace(",", ".")


@app.route("/")
def home():
    return render_template(
        "index.html",
        brand=BRAND,
        kategori=KATEGORI,
        produk=PRODUK,
        keunggulan=KEUNGGULAN,
    )


@app.route("/subscribe", methods=["POST"])
def subscribe():
    """Simpan email pendaftar newsletter ke data/subscribers.json."""
    email = request.form.get("email", "").strip().lower()

    if "@" not in email or "." not in email.split("@")[-1]:
        flash("Format email belum benar. Coba lagi.", "err")
        return redirect(url_for("home", _anchor="newsletter"))

    path = os.path.join(DATA_DIR, "subscribers.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    if any(d["email"] == email for d in data):
        flash("Email ini sudah terdaftar.", "err")
    else:
        data.append({"email": email, "waktu": datetime.datetime.now().isoformat()})
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        flash("Berhasil! Kamu akan dapat info drop terbaru.", "ok")

    return redirect(url_for("home", _anchor="newsletter"))


# ---------------- HALAMAN TAMBAHAN (baru) ----------------
@app.route("/tentang")
def tentang():
    return render_template("tentang.html", brand=BRAND)


@app.route("/kontak")
def kontak():
    return render_template("kontak.html", brand=BRAND)
# ---------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True, port=5000)