import openai

def summarize_and_clarify(history_messages: list, current_question: str, model="gpt-4o", max_tokens=300):
    prompt = f"""
    Aşağıda son konuşma geçmişi ve kullanıcının yeni sorusu var.
    1. Önce, kullanıcının önceki sorularını ve taleplerini madde madde özetle.
       - Her satırda ana bölüm veya konu adını mutlaka belirt.
       - Eğer bir bölüm veya program hakkında konuşuluyorsa, özetin başında bu bölümü yaz ve sonraki maddelerde tekrar et.
       - Gereksiz detay ekleme, sadece ana başlık ve terimler.
    2. Ardından, yeni soruyu geçmişle ilişkili şekilde NETLEŞTİR.
       - Eğer yeni soru önceki konuşmanın devamıysa, bağlamı kullanarak açık hale getir.
       - Eğer konu değişmişse, sadece yeni soruyu netleştir, eski konudan bağlam çekme.
       - Soruyu uzatma, kısa ve net tut.

    Çıktı formatın şu şekilde olmalı:
    ---
    Özet:
    [madde 1]
    [madde 2]
    ...
    Netleştirilmiş Soru:
    [tek satır netleştirilmiş soru]
    ---

    Konuşma Geçmişi:
    {chr(10).join(history_messages)}

    Yeni Soru:
    {current_question}
    """

    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.2,
    )

    result = response.choices[0].message.content.strip()

    summary = ""
    clarified_question = ""
    if "Özet:" in result and "Netleştirilmiş Soru:" in result:
        parts = result.split("Netleştirilmiş Soru:")
        summary = parts[0].replace("Özet:", "").strip()
        clarified_question = parts[1].strip()

    return summary, clarified_question