import streamlit as st
import pandas as pd
import pyodbc
from database_manager import connection_string # Bağlantı ayarını diğer dosyadan çekiyoruz

def show_history():
    st.set_page_config(page_title="Mülakat Geçmişi", layout="wide")
    st.title("📋 Mülakat Geçmişi ve Analiz Paneli")
    st.write("Veritabanındaki (SQL Server) tüm mülakat kayıtları aşağıda listelenmiştir.")

    try:
        # Veritabanına bağlan
        conn = pyodbc.connect(connection_string)
        
        # En yeni mülakatı en üstte görmek için sorgu
        query = """
        SELECT InterviewID, UserFullName, JobTitle, InterviewDate, OverallScore 
        FROM TblInterviews 
        ORDER BY InterviewDate DESC
        """
        
        # Verileri Pandas ile oku (En şık tablo görünümü için)
        df = pd.read_sql(query, conn)
        conn.close()

        if not df.empty:
            # Tabloyu ekrana bas
            st.dataframe(df, use_container_width=True)
            
            # Küçük bir istatistik paneli
            col1, col2 = st.columns(2)
            col1.metric("Toplam Mülakat", len(df))
            col2.metric("Ortalama Puan", f"{df['OverallScore'].mean():.2f}")
        else:
            st.warning("Henüz veritabanında kayıtlı bir mülakat bulunmuyor.")

    except Exception as e:
        st.error(f"Veri çekme hatası: {e}")

if __name__ == "__main__":
    show_history()