from database_manager import save_interview_start, save_qa

def sistemi_test_et():
    print("🚀 Test kaydı başlatılıyor...")

    # İsimleri database_manager içindeki tanımlarla (cv_text, job_text) eşitledik
    mulakat_id = save_interview_start(
        name="İlayda Memiş", 
        title="Backend Developer", 
        cv_text="Deneyimli Python ve SQL geliştiricisi.", 
        job_text="Yapay zeka tabanlı mülakat simülasyonu projesi için mühendis aranıyor."
    )

    if mulakat_id:
        print(f"✅ Ana kayıt oluşturuldu! ID: {mulakat_id}")

        # Soru-cevap detay kaydı
        save_qa(
            interview_id=mulakat_id,
            question="SQL Server'da Foreign Key neden kullanılır?",
            answer="Tablolar arasındaki ilişkiyi ve veri bütünlüğünü sağlamak için kullanılır.",
            evaluation="Doğru ve teknik bir açıklama.",
            score=95
        )
        print("✅ Soru-cevap detay kaydı eklendi!")
        print("\n🎉 Test başarıyla tamamlandı. Şimdi Dashboard'u kontrol et!")
    else:
        print("❌ Kayıt başarısız! Veritabanı bağlantısını ve tablo isimlerini kontrol et.")

if __name__ == "__main__":
    sistemi_test_et()