from turkishnlp import detector

# Modülün içerisinden ilgili sınıf üzerinden bir obje oluşturuyoruz.

# metodları bu obje üzerinden çağıracağız.

nlpDetector = detector.TurkishNLP()

# Kullanmak istedğimiz fonksiyonlara geçmeden önce veri setini indir-

# memiz ve kelime setini hafızaya almamız gerekiyor.

# veri setini indirmek için kullandığımız ‘download’ bir defa

# kullanılması yeterli.

nlpDetector.download()

nlpDetector.create_word_set()

# is_turkish metodu boolean döndürür ve türkçe dil tespiti için kullanılır.

print(nlpDetector.is_turkish("Ben bugün ankaraya gideceğim belki birşeyler alırım"))

# Sonuç %85 kesinlikle True olacaktır.

# list_words verilen metni kelimelere ayırır.

lwords = nlpDetector.list_words("vri kümsi idrae edre ancaka daha güezl oalbilir")

# auto_correct ise hatalı kelimeleri düzeltip liste şeklinde geri döndürür.
correctWords = nlpDetector.auto_correct(lwords)

print(correctWords)

# dönen düzeltilmiş kelime listesini join yardımı ile birleştirebiliriz
corrected_string = " ".join(correctWords)

# Hecelere ayırma için syllabicate_sentence metodu kullanılıyor

nlpDetector.syllabicate_sentence("Hiç unutmadım, doğudan esen hafif bir yel saçlarını dalgalandırıyordu")

# sonuç şu şekilde olacaktır :

# “[[‘hiç’], [‘u’, ‘nut’, ‘ma’, ‘dım,’], [‘do’, ‘ğu’, ‘dan’], [‘e’, ‘sen’], [‘ha’, ‘fif’], [‘bir’], [‘yel’], [‘saç’, ‘la’, ‘rı’, ‘nı’], [‘dal’, ‘ga’, ‘lan’, ‘dı’, ‘rı’, ‘yor’, ‘du’]]”

# Türkçe dil kuralı olan büyük ünlü uyumu is_vowel_harmonic metodu ile kontrol ediliyor

nlpDetector.is_vowel_harmonic("Belki")

# kelime kökeni bulmak için ise is_turkish_origin metodu mevcut.

nlpDetector.is_turkish_origin("program")

# program için False cevabı dönecektir ancak yazılım için kullandığımızda True cevabı alırız.

nlpDetector.is_turkish_origin("yazılım")

# boşluksuz metnin düzeltilmesi için correct_text_without_space metodunu kullanıyoruz

nlpDetector.correct_text_without_space("türkçedoğaldilişleme")

# sonuç türkçe doğal dil işleme olacaktır. *Bu metod her zaman doğru cevap vermeyebiliyor.