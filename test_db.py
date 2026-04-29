from database import DatabaseManager

# 1. Veritabanı yöneticisini başlat (Dosya adı: mülakatlar.db olacak)
db = DatabaseManager("mulakatlar.db")

# 2. Tabloları oluştur
db.init_schema()

# 3. Örnek bir mülakat kaydı oluştur
mulakat_id = db.create_interview("Yarengül", "Python Geliştirici", "2026-03-22")

# 4. Bir mesaj ekle
db.add_message(mulakat_id, "assistant", "Merhaba, mülakata hazır mısın?")

print(f"Başarıyla veritabanı oluşturuldu! Mülakat ID'n: {mulakat_id}")