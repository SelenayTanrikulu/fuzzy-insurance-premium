# Bulanık Mantık Tabanlı Sigorta Prim Öneri Sistemi

Müşteri profiline göre sigorta prim seviyesini belirleyen Mamdani tipi bir bulanık mantık karar destek sistemi. Python ve scikit-fuzzy ile geliştirildi.

*Hesaplamalı Zeka dersi final projesi*

## Sistem

| Değişken | Tür | Aralık | Bulanık kümeler |
|---|---|---|---|
| Yaş | Giriş | 18-80 | Genç, Orta, Yaşlı |
| Meslek Riski | Giriş | 0-10 | Düşük, Orta, Yüksek |
| Hasar Geçmişi | Giriş | 0-10 | Temiz, Az, Çok |
| Prim Seviyesi | Çıkış | 0-100 | Düşük, Orta, Yüksek |

- Üyelik fonksiyonları: üçgen ve trapez
- 12 kurallı uzman bilgisine dayalı kural tabanı
- Çıkarım: Mamdani (min-max), durulaştırma: centroid

## Örnek Sonuçlar

| Senaryo | Yaş | Meslek Riski | Hasar Geçmişi | Prim Seviyesi |
|---|---|---|---|---|
| S1 | 25 | 2 | 0 | 15,6 (Düşük) |
| S2 | 42 | 5 | 4 | 50,0 (Orta) |
| S3 | 55 | 8 | 7 | 84,4 (Yüksek) |
| S4 | 30 | 4 | 8 | 83,1 (Yüksek) |
| S5 | 65 | 2 | 1 | 50,0 (Orta) |

Düşük riskli profillerde prim düşük, yüksek risk ve kötü hasar geçmişinde belirgin şekilde yüksek çıkmaktadır.

## Kurulum

```bash
git clone https://github.com/SelenayTanrikulu/fuzzy-insurance-premium.git
cd fuzzy-insurance-premium
pip install scikit-fuzzy numpy matplotlib
python Sigorta_Prim_Öneri.py
```


