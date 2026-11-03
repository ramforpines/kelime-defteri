"""Gramer içeriği yazım yardımcıları. Test sorusu: Q(zorluk, etiket, soru, DOĞRU, [yanlışlar], açıklama). Doğru şık ilk yazılır; build.py şıkları karıştırır."""
def Q(lv,t,stem,right,wrongs,why):
    return dict(lv=lv,t=t,stem=stem,right=right,wrongs=list(wrongs),why=why)
