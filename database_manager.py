import pyodbc

# Senin bilgisayarına (LAPTOP-BINC41TK\SQLEXPRESS) özel bağlantı cümlesi
connection_string = (
    "Driver={SQL Server};"
    "Server=LAPTOP-BINC41TK\SQLEXPRESS;"
    "Database=DbAiInterview;"
    "Trusted_Connection=yes;"
)

def save_interview_start(name, title, cv_text, job_text):
    # Temizlenmiş verileri ana tabloya (TblInterviews) kaydeder
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        query = """
        INSERT INTO TblInterviews (UserFullName, JobTitle, CVContent, JobDescription)
        OUTPUT INSERTED.InterviewID
        VALUES (?, ?, ?, ?)
        """
        
        cursor.execute(query, (name, title, cv_text, job_text))
        interview_id = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        return interview_id
    except Exception as e:
        print(f"Veritabanı Başlatma Hatası: {e}")
        return None

def save_qa(interview_id, question, answer, evaluation="Bekleniyor", score=0):
    # Mülakat esnasındaki her soru-cevap çiftini detay tablosuna yazar
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        query = """
        INSERT INTO TblInterviewDetails (InterviewID, Question, UserAnswer, Evaluation, Score)
        VALUES (?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (interview_id, question, answer, evaluation, score))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Soru Kayıt Hatası: {e}")

def get_interview_history():
    # Geçmiş mülakatları ekranda göstermek için verileri çeker
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT InterviewID, UserFullName, JobTitle, InterviewDate, OverallScore FROM TblInterviews ORDER BY InterviewDate DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Geçmiş Çekme Hatası: {e}")
        return []

if __name__ == "__main__":
    print("SQL Server Bağlantı Modülü Aktif.")
def update_interview_score(interview_id, final_score):
    # Mülakat bittiğinde toplam puanı günceller
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        query = "UPDATE TblInterviews SET OverallScore = ? WHERE InterviewID = ?"
        cursor.execute(query, (final_score, interview_id))
        
        conn.commit()
        conn.close()
        print(f"✅ Mülakat {interview_id} için puan {final_score} olarak güncellendi.")
    except Exception as e:
        print(f"Puan Güncelleme Hatası: {e}")