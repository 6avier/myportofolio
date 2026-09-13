Kemas Xavier Alvaresyah
2506656886
PBP C

---

### Tugas 1

**1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti <section>, <article>, atau <aside>? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?**

Ya. Kerangka halaman memakai `<header>`, `<nav>`, `<main>`, dan `<footer>`. Di dalamnya ada 6 `<section>` untuk tiap divisi konten (Profile, About, Education, Projects, Experience, Skills) dan 5 `<article>` untuk tiap entri di dalamnya, seperti riwayat pendidikan dan pengalaman organisasi. Data NPM dan Program saya tulis dengan `<dl>`, `<dt>`, dan `<dd>` karena isinya pasangan label dan nilai.

Hierarki `<h1>` ke `<h2>` ke `<h3>` membuat urutan kepentingan konten terbaca tanpa bergantung pada ukuran font. Nama saya menjadi `<h1>`, judul tiap section `<h2>`, dan judul tiap entri `<h3>`.

Elemen semantic juga menyelamatkan struktur halaman ini dari layout-nya sendiri. Saya menggeser tiap section ke posisi horizontal yang berbeda, sehingga posisi visual berhenti mencerminkan urutan konten. Screen reader dan saya sendiri saat menyunting tetap bisa membaca batas tiap blok karena strukturnya eksplisit di markup.

`<aside>` tidak saya pakai. Logo institusi dan sticker yang melayang di ruang kosong sempat saya pertimbangkan untuk dibungkus elemen itu, tetapi logo UI menerangkan entri Universitas Indonesia dan bukan konten sampingan yang berdiri sendiri. Saya membiarkannya sebagai `<img>` di dalam section terkait.

**2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?**

Konsep desain yang saya pilih sendiri yang menyulitkan. Di desktop halaman ini memakai grid 12 kolom dan tiap section mengambil rentang kolom yang berbeda. About di kolom 2 sampai 8, Education 7 sampai 12, Projects melebar dari 1 sampai 11. Asimetri itu identitas visualnya. Di layar 393px pola tersebut tidak mungkin bertahan karena tiap section hanya kebagian beberapa puluh piksel dan teksnya berhenti terbaca. Di bawah 900px saya jadikan semua section satu kolom penuh. Saya melepas ciri khas desain di mobile demi keterbacaan, dan saya menilai itu pertukaran yang tepat.

Keputusan tersebut merembet ke logo. Di desktop saya memposisikan logo institusi dan sticker secara absolute, melayang di ruang kosong hasil asimetri tadi. Begitu layout menjadi satu kolom, ruang kosong itu hilang dan logo menimpa teks. Saya kembalikan mereka ke alur normal di mobile dengan ukuran, kolom, dan jarak atas yang berbeda-beda supaya kesan berserakannya bertahan.

Masalah ketiga tidak saya duga. Logo KXA di header memakai efek ransom-note yang mengacak font tiap huruf lewat JavaScript. Tiap font punya lebar berbeda, jadi lebar logo berubah setiap kali huruf diacak. Setelah saya ukur, rentangnya 56px sampai 92px. Di desktop pergeseran itu tidak terasa. Di mobile navigasi duduk tepat di sebelahnya, sehingga navigasi ikut terdorong dan tercatat mendarat di 29 posisi berbeda. Saya mengubah header menjadi grid dengan kolom logo berlebar tetap, sehingga jatah ruang navigasi konstan berapa pun lebar huruf yang ter-render.

Urutan prioritas konten saya jaga sama di kedua ukuran: identitas dan foto, lalu narasi, lalu riwayat. Yang saya pangkas di mobile hanya hal dekoratif. Padding hero saya turunkan dari 4.5rem ke 1.25rem karena di ponsel menyisakan celah kosong hampir 90px, ukuran font navigasi saya kecilkan, dan posisi melayang saya ganti alur biasa. Tidak ada konten yang saya buang.

**3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?**

Seluruh konten tertanam di `index.html`. Setiap kali saya menambah satu proyek atau pengalaman, saya membuka file template, menyalin struktur `<article>` yang sudah ada, lalu menulis ulang isinya. Kalau entrinya bertambah sampai puluhan, cara ini rawan salah. Struktur tiap entri Experience juga identik dan hanya berbeda isi, padahal cukup ditulis sekali lalu diulang lewat perulangan.

Halaman ini juga belum bisa menerima apa pun dari pengunjung. Tidak ada tempat menyimpan data, sehingga form kontak tidak mungkin benar-benar mengirim pesan, penghitung kunjungan belum ada, dan penyaringan proyek berdasarkan teknologi harus saya tulis di sisi klien.

Setelah masuk database dan pola MVT, saya ingin membuat model Project dan Experience lebih dulu, supaya entri baru bisa saya tambah lewat halaman admin Django tanpa menyentuh HTML dan templatenya cukup memakai satu blok perulangan. Berikutnya form kontak yang pesannya tersimpan, lalu filter proyek berdasarkan tech stack. Fitur terakhir itu baru masuk akal setelah datanya tersimpan terstruktur.

---

### Menjalankan proyek secara lokal

```bash
git clone https://github.com/6avier/myportofolio.git
cd myportofolio
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

---

### Penggunaan AI

Saya menggunakan AI dalam pengerjaan tugas ini.

**Tools:** Claude (Claude Code), model Sonnet dan Opus.

**Strategi prompting:** Saya memberi instruksi desain dan menyertakan rujukan visual berupa tangkapan layar. 
Contohnya meminta placard foto dibuat menyerupai label museum lengkap dengan hierarki fontnya, dan meminta
tata letak section dibuat heterogen serta off-center tetapi tetap terbagi per
divisi. Untuk bug saya menyebutkan gejalanya lebih dulu, misalnya "kalau logonya
di-hover, posisinya suka pindah-pindah", lalu meminta AI menelusuri penyebabnya.
Satu hasil sering saya minta revisi berkali-kali sampai bentuknya sesuai.

**Bagian yang dibantu:**

- Troubleshooting Tutorial 0 dan 1: virtual environment, error `DisallowedHost`
  saat deploy ke PWS, konfigurasi WhiteNoise untuk file static, dan perapian
  riwayat git.
- Konsep layout long-scroll: pemilihan arah desain, tingkat asimetri, dan
  kepadatan konten CV yang masuk.
- Section About, Education, Projects, Experience, dan Skills: struktur HTML
  beserta CSS-nya, termasuk grid 12 kolom dan penempatan asimetris tiap section.
- Penempatan logo dan sticker yang melayang di ruang kosong beserta
  penyesuaiannya di mobile.
- Perbaikan bug tampilan: navigasi yang bergeser, nama di hero yang kadang
  menempel jadi satu baris, dan jarak berlebih di tampilan mobile.
- Riset referensi font dan sumber tekstur kertas.

### Tugas 2

1. Ketika pengguna membuka halaman `/education/`, request pertama kali masuk ke `portofolio/urls.py` (urls.py level proyek), yang mengecek prefix URL dan meneruskan request ke `main/urls.py` (urls.py level aplikasi) karena request tersebut cocok dengan include dari app `main`. Di dalam `main/urls.py`, Django mencocokkan path `education/` dengan `path("education/", show_education, name="show_education")`, lalu memanggil fungsi view `show_education` di `main/views.py`. View ini mengambil seluruh data `Education` dari database lewat `Education.objects.all()`, memasukkannya ke dalam sebuah `context` (dictionary), lalu memanggil `render()` dengan template `education.html` dan context tersebut. Django kemudian merender template itu: bagian `{% for education in education_list %}` melakukan iterasi ke setiap object Education dan mengisi HTML dengan data sebenarnya (institution, program, start_year, end_year, logo). Hasil HTML yang sudah jadi ini dikirim balik sebagai response ke browser, dan browser menampilkannya sebagai halaman Education yang dilihat pengguna.

2. Data untuk bagian portofolio baru sebaiknya disimpan di model, bukan ditulis langsung di template, karena template seharusnya hanya bertanggung jawab atas presentasi (tampilan), bukan penyimpanan data. Kalau data di-hardcode di HTML, setiap kali ada perubahan data (misalnya menambah riwayat pendidikan baru atau mengubah tahun kelulusan), saya harus mengedit langsung file template dan melakukan deploy ulang seluruh aplikasi. Dengan menyimpan data di model, saya bisa menambah, mengubah, atau menghapus data lewat Django admin tanpa menyentuh kode sama sekali, sehingga lebih aman dari technical debt dan human error saat mengedit HTML. Ini juga membuat data bisa dipakai ulang di tempat lain (misalnya API atau halaman lain) tanpa duplikasi, dan memisahkan tanggung jawab logika data (model) dari tampilan (template) sesuai prinsip separation of concerns pada pola MVT.

3. `makemigrations` membuat berkas migrasi baru berdasarkan perubahan yang saya buat di `models.py` — ini semacam "rencana perubahan" struktur database dalam bentuk kode Python, tapi belum benar-benar diterapkan ke database. `migrate` menjalankan berkas migrasi tersebut ke database sungguhan, mengeksekusi perintah SQL (CREATE TABLE, ALTER TABLE, dsb.) sehingga struktur database benar-benar berubah sesuai migrasi yang ada. Contoh nyata dari proyek ini: saat saya membuat model `Education` untuk pertama kali, saya menjalankan `makemigrations` untuk menghasilkan file migrasi `0002_education.py`, lalu `migrate` untuk benar-benar membuat tabel `main_education` di `db.sqlite3`. Selanjutnya, saat saya mengubah tipe field `logo` dari `URLField` menjadi `CharField`, saya kembali menjalankan `makemigrations` (menghasilkan `0003_alter_education_logo.py`) dan `migrate` supaya perubahan tipe kolom tersebut diterapkan ke tabel yang sudah ada di database.

### Penggunaan AI

**Tools:** Claude (Claude Code), model Sonnet.

**Strategi prompting:** Saya jelasin requirement-nya, lalu diarahkan
langkah demi langkah (model, migrasi, view, template, url, navbar, test)
dan saya yang ngetik sendiri tiap bagian kodenya. Kalau ada error, saya
kirim pesan errornya dan minta dijelasin penyebabnya.

**Bagian yang dibantu:**

- Perancangan model `Education` dan alur MVT-nya.
- Debugging error `URLField` dan `IndentationError` di test.
- Penyusunan unit test untuk halaman `/education/`.