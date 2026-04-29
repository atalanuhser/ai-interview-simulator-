from main_interview import InterviewSim

# 🔥 GLOBAL AI SESSION
sim = None


# 🚀 MÜLAKAT BAŞLAT
def start_interview(name, job):

    global sim
    sim = InterviewSim()

    prompt = f"""
    Sen deneyimli bir teknik mülakatçısın.

    Aday: {name}
    Pozisyon / İş:
    {job}

    Kurallar:
    - Aynı soruyu tekrar etme
    - Her cevapta yeni soru sor
    - Gerekirse derinleş
    - Kısa ve net ol

    İlk soruyu sor.
    """

    try:
        return sim.ask(prompt)
    except:
        return "Kendini tanıtır mısın?"


# 💬 CEVAP GÖNDER
def send_answer(answer):

    global sim

    if sim is None:
        sim = InterviewSim()

    prompt = f"""
    Adayın cevabı:
    {answer}

    Buna göre:
    - Yeni soru sor
    - Aynı şeyi tekrar etme
    - Teknik detay iste
    """

    try:
        response = sim.ask(prompt)

        # 🔥 LOOP ENGELLEME
        if "detay" in response.lower():
            return "Bu konuda hangi teknolojileri kullandın?"

        return response

    except:
        return "Bu projede en zorlandığın kısım neydi?"


# 📊 SONUÇ ANALİZ
def analyze_result(job_text, messages):

    global sim

    if sim is None:
        sim = InterviewSim()

    convo = ""
    for m in messages:
        role = "Aday" if m["role"] == "user" else "AI"
        convo += f"{role}: {m['content']}\n"

    prompt = f"""
    Sen profesyonel bir mülakat değerlendiricisisin.

    İş ilanı:
    {job_text}

    Mülakat:
    {convo}

    Yap:
    1. Güçlü yönleri yaz
    2. Zayıf yönleri yaz
    3. İlanla karşılaştır
    4. Gelişim önerisi ver

    Türkçe yaz.
    """

    try:
        return sim.ask(prompt)
    except:
        return """
        Güçlü yönlerin iyi seviyede.
        Ancak teknik konularda biraz daha derinleşmelisin.
        """