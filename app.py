import csv
import os

class GudangJagung:
    def __init__(self, directory="data", filename="gudang_jagung.csv"):
        self.directory = directory
        self.filename = os.path.join(directory, filename)
        self.stack = []       # Struktur Data 1: Stack (Tumpukan Karung)
        self.hash_map = {}    # Struktur Data 2: Hash Map (Ringkasan Total Berat per Jenis)
        self.init_database()
        self.load_from_csv()

    # Membuat folder dan file CSV di awal jika belum ada
    def init_database(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
            
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["id_karung", "jenis_jagung", "berat_kg", "tanggal_masuk"])

    # Membaca data dari CSV ke memori (Stack & Hash Map) saat program start
    def load_from_csv(self):
        self.stack = []
        self.hash_map = {}
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                karung = {
                    "id_karung": row["id_karung"],
                    "jenis_jagung": row["jenis_jagung"],
                    "berat_kg": float(row["berat_kg"]),
                    "tanggal_masuk": row["tanggal_masuk"]
                }
                self.stack.append(karung) 
                # Sinkronisasi ke Hash Map
                jenis = karung["jenis_jagung"]
                self.hash_map[jenis] = self.hash_map.get(jenis, 0.0) + karung["berat_kg"]

    # Menulis ulang isi Stack ke file CSV (Sinkronisasi Database)
    def save_to_csv(self):
        with open(self.filename, mode='w', newline='') as file:
            fieldnames = ["id_karung", "jenis_jagung", "berat_kg", "tanggal_masuk"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for karung in self.stack:
                writer.writerow(karung)

    # --- FITUR WAJIB (CRUD & STRUKTUR DATA) ---

    # 1. CREATE / PUSH (Tambah Karung ke Tumpukan Teratas)
    def tambah_karung(self, id_karung, jenis, berat, tanggal):
        if self.searching_by_id(id_karung) is not None:
            print("❌ Gagal! ID Karung sudah terdaftar di gudang.")
            return

        karung = {
            "id_karung": id_karung,
            "jenis_jagung": jenis,
            "berat_kg": float(berat),
            "tanggal_masuk": tanggal
        }
        self.stack.append(karung) 
        self.save_to_csv()
        self.load_from_csv() # Refresh data memori
        print(f"✅ Karung {id_karung} sukses ditumpuk di posisi teratas!")

    # 2. DELETE / POP (Ambil Karung dari Tumpukan Teratas - LIFO)
    def ambil_karung(self):
        if not self.stack:
            print("⚠️ Gudang Kosong! Tidak ada karung yang bisa diambil.")
            return
        
        karung_diambil = self.stack.pop()
        self.save_to_csv()
        self.load_from_csv() # Refresh data memori
        print(f"📦 Karung {karung_diambil['id_karung']} ({karung_diambil['jenis_jagung']}) seberat {karung_diambil['berat_kg']} kg berhasil diambil!")

    # 3. READ (Tampilkan Kondisi Tumpukan Gudang saat ini)
    def tampilkan_gudang(self):
        if not self.stack:
            print("📭 Gudang Kosong.")
            return
        
        print("\n=== POSISI TUMPUKAN GUDANG JAGUNG (Teratas ke Terbawah) ===")
        for i in range(len(self.stack) - 1, -1, -1):
            k = self.stack[i]
            print(f" Posisi [{i}] -> ID: {k['id_karung']} | Jenis: {k['jenis_jagung']} | Berat: {k['berat_kg']} kg | Masuk: {k['tanggal_masuk']}")
        
        print("\n=== RINGKASAN STOK GLOBAL (HASH MAP) ===")
        for jenis, total_berat in self.hash_map.items():
            print(f" 🌽 {jenis}: {total_berat:.2f} kg")

    # 4. SEARCHING (Linear Search untuk Cari Karung berdasarkan ID)
    def searching_by_id(self, target_id):
        for index, karung in enumerate(self.stack):
            if karung["id_karung"].lower() == target_id.lower():
                return index, karung
        return None

    # 5. SORTING (Bubble Sort untuk mengurutkan data visual dari yang Terringan)
    def sorting_by_berat(self):
        if not self.stack:
            print("📭 Gudang Kosong, tidak ada data untuk diurutkan.")
            return
        
        # Duplikasi list agar urutan fisik Stack asli tidak berantakan
        sorted_list = list(self.stack)
        n = len(sorted_list)
        for i in range(n):
            for j in range(0, n - i - 1):
                if sorted_list[j]["berat_kg"] > sorted_list[j + 1]["berat_kg"]:
                    sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
                    
        print("\n=== HASIL SORTING KARUNG JAGUNG (DARI PALING RINGAN) ===")
        for k in sorted_list:
            print(f" ID: {k['id_karung']} | Jenis: {k['jenis_jagung']} | Berat: {k['berat_kg']} kg")

# --- MENU USER INTERFACE (CLI) ---
def main():
    gudang = GudangJagung()
    while True:
        print("\n=============================================")
        print("    SISTEM MANAJEMEN GUDANG JAGUNG (LIFO)   ")
        print("=============================================")
        print("1. Tambah Karung Jagung Baru (Push/Create)")
        print("2. Ambil Karung Jagung Teratas (Pop/Delete)")
        print("3. Cek Tumpukan Gudang & Stok (Read)")
        print("4. Cari Karung berdasarkan ID (Searching)")
        print("5. Urutkan Karung berdasarkan Berat (Sorting)")
        print("6. Keluar Selesai")
        
        pilihan = input("Pilih Menu (1-6): ")

        if pilihan == "1":
            id_k = input("Masukkan ID Karung (Contoh: KRG01): ")
            jenis = input("Jenis Jagung (Manis / Pakan / Pipil): ")
            try:
                berat = float(input("Berat Karung (kg): "))
            except ValueError:
                print("❌ Berat harus berupa angka!")
                continue
            tgl = input("Tanggal Masuk (YYYY-MM-DD): ")
            gudang.tambah_karung(id_k, jenis, berat, tgl)
        elif pilihan == "2":
            gudang.ambil_karung()
        elif pilihan == "3":
            gudang.tampilkan_gudang()
        elif pilihan == "4":
            target = input("Masukkan ID Karung yang ingin dicari: ")
            hasil = gudang.searching_by_id(target)
            if hasil:
                idx, k = hasil
                print(f"🎯 Karung Ditemukan! Ada di indeks tumpukan ke-{idx}")
                print(f"   Detail -> Jenis: {k['jenis_jagung']} | Berat: {k['berat_kg']} kg | Masuk: {k['tanggal_masuk']}")
            else:
                print("❌ Karung dengan ID tersebut tidak ditemukan.")
        elif pilihan == "5":
            gudang.sorting_by_berat()
        elif pilihan == "6":
            print("👋 Keluar aplikasi. Data Anda aman tersimpan di CSV!")
            break
        else:
            print("❌ Menu tidak valid. Silakan pilih angka 1-6.")

if __name__ == "__main__":
    main()