from turkishnlp import detector

# Modülün içerisinden ilgili sınıf üzerinden bir obje oluşturuyoruz.

# metodları bu obje üzerinden çağıracağız.

nlpDetector = detector.TurkishNLP()

# Kullanmak istedğimiz fonksiyonlara geçmeden önce veri setini indir-

# memiz ve kelime setini hafızaya almamız gerekiyor.

# veri setini indirmek için kullandığımız ‘download’ bir defa

# kullanılması yeterli.

# nlpDetector.download()

nlpDetector.create_word_set()

# is_turkish metodu boolean döndürür ve türkçe dil tespiti için kullanılır.

print(nlpDetector.is_turkish("Ben bugün ankaraya gideceğim belki birşeyler alırım"))

# Sonuç %85 kesinlikle True olacaktır.

# list_words verilen metni kelimelere ayırır.

lwords = nlpDetector.list_words("vri kümsi idrae edre ancaka daha güezl oalbilir")
lwords = nlpDetector.list_words("bahdelievler")

# auto_correct ise hatalı kelimeleri düzeltip liste şeklinde geri döndürür.
correctWords = nlpDetector.auto_correct(lwords)

print(correctWords)

# dönen düzeltilmiş kelime listesini join yardımı ile birleştirebiliriz
corrected_string = " ".join(correctWords)
# print(nlpDetector.syllabicate_sentence("Hiç unutmadım, doğudan esen hafif bir yel saçlarını dalgalandırıyordu"))
print(nlpDetector.syllabicate_sentence("bahçelievler"))

print(nlpDetector.correct_text_without_space("bahçelievlermahallesi"))
