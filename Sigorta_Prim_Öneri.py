"""
Bulanık Mantık Tabanlı Sigorta Prim Öneri Sistemi
Öğrenci: Selenay TANRIKULU - 258273002010
Kütüphane: scikit-fuzzy
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# ─────────────────────────────────────────────────────────────
# 1. EVRENLERİ TANIMLA
# ─────────────────────────────────────────────────────────────
yas           = ctrl.Antecedent(np.arange(18, 81, 1),  'Yas')
meslek_riski  = ctrl.Antecedent(np.arange(0, 11, 0.1), 'Meslek_Riski')
hasar_gecmisi = ctrl.Antecedent(np.arange(0, 11, 0.1), 'Hasar_Gecmisi')
prim          = ctrl.Consequent(np.arange(0, 101, 1),  'Prim_Seviyesi')

# ─────────────────────────────────────────────────────────────
# 2. ÜYELİK FONKSİYONLARI
# ─────────────────────────────────────────────────────────────

# Yaş
yas['Genc']  = fuzz.trapmf(yas.universe,   [18, 18, 25, 35])
yas['Orta']  = fuzz.trimf(yas.universe,    [30, 45, 60])
yas['yasli'] = fuzz.trapmf(yas.universe,   [55, 65, 80, 80])

# Meslek Riski (0=Çok güvenli, 10=Çok tehlikeli)
meslek_riski['Dusuk']   = fuzz.trimf(meslek_riski.universe, [0, 0, 4])
meslek_riski['Orta']    = fuzz.trimf(meslek_riski.universe, [3, 5, 7])
meslek_riski['Yuksek']  = fuzz.trimf(meslek_riski.universe, [6, 10, 10])

# Hasar Geçmişi (0=Hiç hasar yok, 10=Çok fazla hasar)
hasar_gecmisi['Temiz']  = fuzz.trimf(hasar_gecmisi.universe, [0, 0, 3])
hasar_gecmisi['Az']     = fuzz.trimf(hasar_gecmisi.universe, [2, 5, 8])
hasar_gecmisi['Cok']    = fuzz.trimf(hasar_gecmisi.universe, [7, 10, 10])

# Prim Seviyesi (0=En düşük, 100=En yüksek)
prim['Dusuk']   = fuzz.trimf(prim.universe, [0, 0, 40])
prim['Orta']    = fuzz.trimf(prim.universe, [30, 50, 70])
prim['Yuksek']  = fuzz.trimf(prim.universe, [60, 100, 100])

# ─────────────────────────────────────────────────────────────
# 3. KURAL TABANI
# ─────────────────────────────────────────────────────────────
kural1 = ctrl.Rule(yas['Genc']  & meslek_riski['Dusuk']  & hasar_gecmisi['Temiz'], prim['Dusuk'])
kural2 = ctrl.Rule(yas['Genc']  & meslek_riski['Orta']   & hasar_gecmisi['Temiz'], prim['Dusuk'])
kural3 = ctrl.Rule(yas['Genc']  & meslek_riski['Dusuk']  & hasar_gecmisi['Az'],    prim['Orta'])
kural4 = ctrl.Rule(yas['Orta']  & meslek_riski['Orta']   & hasar_gecmisi['Az'],    prim['Orta'])
kural5 = ctrl.Rule(yas['Orta']  & meslek_riski['Dusuk']  & hasar_gecmisi['Temiz'], prim['Dusuk'])
kural6 = ctrl.Rule(yas['yasli'] & meslek_riski['Orta'],                             prim['Orta'])
kural7 = ctrl.Rule(yas['yasli'] & hasar_gecmisi['Cok'],                             prim['Yuksek'])
kural8 = ctrl.Rule(meslek_riski['Yuksek'],                                          prim['Yuksek'])
kural9  = ctrl.Rule(hasar_gecmisi['Cok'],                                            prim['Yuksek'])
kural10 = ctrl.Rule(yas['yasli'] & meslek_riski['Dusuk'] & hasar_gecmisi['Temiz'],  prim['Orta'])
kural11 = ctrl.Rule(yas['yasli'] & meslek_riski['Dusuk'] & hasar_gecmisi['Az'],     prim['Orta'])
kural12 = ctrl.Rule(yas['Orta']  & meslek_riski['Yuksek'],                          prim['Yuksek'])

# ─────────────────────────────────────────────────────────────
# 4. KONTROL SİSTEMİ
# ─────────────────────────────────────────────────────────────
prim_ctrl = ctrl.ControlSystem([
    kural1, kural2, kural3, kural4, kural5,
    kural6, kural7, kural8, kural9, kural10, kural11, kural12
])
prim_sim = ctrl.ControlSystemSimulation(prim_ctrl)

# ─────────────────────────────────────────────────────────────
# 5. ÜYELİK FONKSİYONU GRAFİKLERİ → Şekil 1
# ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Üyelik Fonksiyonları', fontsize=14, fontweight='bold')

# Yaş
axes[0, 0].plot(yas.universe, fuzz.trapmf(yas.universe, [18, 18, 25, 35]),  'b',  label='Genç')
axes[0, 0].plot(yas.universe, fuzz.trimf(yas.universe,  [30, 45, 60]),      'g',  label='Orta')
axes[0, 0].plot(yas.universe, fuzz.trapmf(yas.universe, [55, 65, 80, 80]),  'r',  label='Yaşlı')
axes[0, 0].set_title('Yaş'); axes[0, 0].set_xlabel('Yaş (yıl)'); axes[0, 0].set_ylabel('Üyelik Derecesi')
axes[0, 0].legend(); axes[0, 0].set_ylim(0, 1.1); axes[0, 0].grid(True, alpha=0.3)

# Meslek Riski
axes[0, 1].plot(meslek_riski.universe, fuzz.trimf(meslek_riski.universe, [0, 0, 4]),    'b', label='Düşük')
axes[0, 1].plot(meslek_riski.universe, fuzz.trimf(meslek_riski.universe, [3, 5, 7]),    'g', label='Orta')
axes[0, 1].plot(meslek_riski.universe, fuzz.trimf(meslek_riski.universe, [6, 10, 10]),  'r', label='Yüksek')
axes[0, 1].set_title('Meslek Riski'); axes[0, 1].set_xlabel('Risk Skoru (0-10)'); axes[0, 1].set_ylabel('Üyelik Derecesi')
axes[0, 1].legend(); axes[0, 1].set_ylim(0, 1.1); axes[0, 1].grid(True, alpha=0.3)

# Hasar Geçmişi
axes[1, 0].plot(hasar_gecmisi.universe, fuzz.trimf(hasar_gecmisi.universe, [0, 0, 3]),   'b', label='Temiz')
axes[1, 0].plot(hasar_gecmisi.universe, fuzz.trimf(hasar_gecmisi.universe, [2, 5, 8]),   'g', label='Az')
axes[1, 0].plot(hasar_gecmisi.universe, fuzz.trimf(hasar_gecmisi.universe, [7, 10, 10]), 'r', label='Çok')
axes[1, 0].set_title('Hasar Geçmişi'); axes[1, 0].set_xlabel('Hasar Skoru (0-10)'); axes[1, 0].set_ylabel('Üyelik Derecesi')
axes[1, 0].legend(); axes[1, 0].set_ylim(0, 1.1); axes[1, 0].grid(True, alpha=0.3)

# Prim Seviyesi
axes[1, 1].plot(prim.universe, fuzz.trimf(prim.universe, [0, 0, 40]),    'b', label='Düşük')
axes[1, 1].plot(prim.universe, fuzz.trimf(prim.universe, [30, 50, 70]),   'g', label='Orta')
axes[1, 1].plot(prim.universe, fuzz.trimf(prim.universe, [60, 100, 100]), 'r', label='Yüksek')
axes[1, 1].set_title('Prim Seviyesi'); axes[1, 1].set_xlabel('Prim (0-100)'); axes[1, 1].set_ylabel('Üyelik Derecesi')
axes[1, 1].legend(); axes[1, 1].set_ylim(0, 1.1); axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('sekil1_uyelik_fonksiyonlari.png', dpi=150, bbox_inches='tight')
plt.show()
print("Şekil 1 kaydedildi: sekil1_uyelik_fonksiyonlari.png")

# ─────────────────────────────────────────────────────────────
# 6. SİMÜLASYON SENARYOLARI
# ─────────────────────────────────────────────────────────────
senaryolar = [
    {"ad": "S1 - Düşük Riskli Genç",          "yas": 25, "meslek": 2, "hasar": 0},
    {"ad": "S2 - Orta Profilli Yetişkin",       "yas": 42, "meslek": 5, "hasar": 4},
    {"ad": "S3 - Yüksek Riskli Orta Yaş",      "yas": 55, "meslek": 8, "hasar": 7},
    {"ad": "S4 - Genç / Kötü Sicil",           "yas": 30, "meslek": 4, "hasar": 8},
    {"ad": "S5 - Yaşlı / Temiz Sicil",         "yas": 65, "meslek": 2, "hasar": 1},
]

print("\n" + "="*65)
print(f"{'Senaryo':<30} {'Yaş':>4} {'Risk':>5} {'Hasar':>6} {'Prim':>8}")
print("="*65)

sonuclar = []
for s in senaryolar:
    prim_sim.input['Yas']           = s["yas"]
    prim_sim.input['Meslek_Riski']  = s["meslek"]
    prim_sim.input['Hasar_Gecmisi'] = s["hasar"]
    prim_sim.compute()
    deger = prim_sim.output['Prim_Seviyesi']

    if deger < 35:
        etiket = "DÜŞÜK"
    elif deger < 65:
        etiket = "ORTA"
    else:
        etiket = "YÜKSEK"

    sonuclar.append({"senaryo": s["ad"], "deger": deger, "etiket": etiket})
    print(f"{s['ad']:<30} {s['yas']:>4} {s['meslek']:>5} {s['hasar']:>6} {deger:>7.1f}  ({etiket})")

print("="*65)

# ─────────────────────────────────────────────────────────────
# 7. SENARYO SONUÇLARI ÇUBUK GRAFİĞİ → Şekil 2
# ─────────────────────────────────────────────────────────────
fig2, ax = plt.subplots(figsize=(10, 5))

renkler = ['#27AE60' if s['etiket'] == 'DÜŞÜK' else '#F39C12' if s['etiket'] == 'ORTA' else '#E74C3C'
           for s in sonuclar]
isimler  = [s['senaryo'] for s in sonuclar]
degerler = [s['deger']   for s in sonuclar]

bars = ax.bar(isimler, degerler, color=renkler, edgecolor='black', linewidth=0.8)

# Değerleri çubukların üstüne yaz
for bar, val, s in zip(bars, degerler, sonuclar):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f"{val:.1f}\n({s['etiket']})", ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.axhline(y=35, color='#27AE60', linestyle='--', alpha=0.5, label='Düşük/Orta sınırı (35)')
ax.axhline(y=65, color='#E74C3C', linestyle='--', alpha=0.5, label='Orta/Yüksek sınırı (65)')

ax.set_title('Simülasyon Senaryoları – Prim Seviyesi Sonuçları', fontsize=13, fontweight='bold')
ax.set_ylabel('Prim Seviyesi (0–100)')
ax.set_ylim(0, 110)
ax.legend(loc='upper left')
ax.grid(axis='y', alpha=0.3)
plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig('sekil2_senaryo_sonuclari.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nŞekil 2 kaydedildi: sekil2_senaryo_sonuclari.png")
print("\nKod başarıyla tamamlandı!")

# ─────────────────────────────────────────────────────────────
# 8. 3D YÜZEY GRAFİĞİ → Şekil 3
# Yaş sabit (42), Meslek Riski ve Hasar Geçmişi değişken
# ─────────────────────────────────────────────────────────────
from mpl_toolkits.mplot3d import Axes3D

meslek_aralik = np.arange(0, 10.5, 0.5)
hasar_aralik  = np.arange(0, 10.5, 0.5)
Z = np.zeros((len(hasar_aralik), len(meslek_aralik)))

for i, h in enumerate(hasar_aralik):
    for j, m in enumerate(meslek_aralik):
        try:
            prim_sim.input['Yas']           = 42
            prim_sim.input['Meslek_Riski']  = m
            prim_sim.input['Hasar_Gecmisi'] = h
            prim_sim.compute()
            Z[i, j] = prim_sim.output['Prim_Seviyesi']
        except:
            Z[i, j] = np.nan

X, Y = np.meshgrid(meslek_aralik, hasar_aralik)

fig3 = plt.figure(figsize=(10, 7))
ax3  = fig3.add_subplot(111, projection='3d')
surf = ax3.plot_surface(X, Y, Z, cmap='RdYlGn_r', edgecolor='none', alpha=0.9)
ax3.set_xlabel('Meslek Riski (0-10)', labelpad=10)
ax3.set_ylabel('Hasar Geçmişi (0-10)', labelpad=10)
ax3.set_zlabel('Prim Seviyesi (0-100)', labelpad=10)
ax3.set_title('Şekil 3. Meslek Riski ve Hasar Geçmişine Göre\nPrim Seviyesi Yüzey Grafiği (Yaş=42)',
              fontsize=12, fontweight='bold', pad=15)
fig3.colorbar(surf, ax=ax3, shrink=0.5, label='Prim Seviyesi')
plt.tight_layout()
plt.savefig('sekil3_yuzey_grafigi.png', dpi=150, bbox_inches='tight')
plt.show()
print("Şekil 3 kaydedildi: sekil3_yuzey_grafigi.png")