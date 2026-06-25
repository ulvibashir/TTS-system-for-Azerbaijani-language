# Azərbaycan Dili üçün TTS Sistemi — Müdafiə Hazırlığı
## Ulvi Bashirov · UNEC MBA · 2026

---

# PART 1 — 15–20 DƏQİQƏLİK NİTQ (Speech Script)

Use this as your speaking guide. Approximate timing: ~2 min per section.

---

## Opening (1–2 dəq)

"Hörmətli komissiya üzvləri,

Mənim dissertasiya işim **Azərbaycan dili üçün qaydaya əsaslanan Mətndən-Nitqə Sintezi Sisteminin** layihələndirilməsi və işlənib hazırlanmasına həsr edilib.

Azərbaycan dili — dünyada 30 milyondan çox insan tərəfindən danışılan türk dili ailəsinə aid bir dildir. Lakin rəqəmsal texnologiyalar sahəsində bu dil hələ də kifayət qədər inkişaf etdirilməmiş qalır. Bugün mövcud olan Azərbaycan TTS sistemləri ya çox sadə, ya da əlçatmaz xarici platformalara əsaslanır.

Bu iş məhz bu boşluğu doldurmaq məqsədi ilə yazılmışdır."

---

## Problemin Əhəmiyyəti (2 dəq)

"Azərbaycan dilinin TTS sahəsindəki əsas çətinlikləri bunlardır:

1. **Sait Harmoniyası** — Azərbaycan türk dili ailısindən gəlir, ona görə şəkilçilər söz kökünün son saiti ilə harmonik uyğunluq tələb edir. Məsələn: 'ev-dən' vs 'ev-dən' düzgündür, amma 'kitab-dan' düzgündür.

2. **Qlottal/Damaq Samitlər** — 'g' hərfi ön saitlərin yanında fərqli tələffüz edilir: 'gəl' (/ɟæl/) vs 'qardaş' (/ɡardaʃ/).

3. **Yumşaq-g (ğ) Fonemi** — Bu hərfin davranışı mövqeyindən asılıdır: iki sait arasında /ɣ/ kimi, söz sonunda isə əvvəlki saiti uzadır (/ː/).

4. **Qeyri-standart Sözlər (NSWs)** — Rəqəmlər, abbreviaturalar, tarix, vaxt — bunların hamısı Azərbaycan dilindəki oxunuş formasına çevrilməlidir.

Mövcud çözümlər bu xüsusiyyətləri ya tamamilə görməzlikdən gəlir, ya da səhv idarə edir."

---

## Sistem Arxitekturası — Əsas Hissə (5–6 dəq)

"Mən bu problemi həll etmək üçün **6 pilləli kaskad boru kəməri (pipeline)** hazırladım.

Boru kəmərini belə təsəvvür edin: mətn giriş nöqtəsindən keçib hər pillədən ardıcıl şəkildə keçərək son nəticə olan səs faylına çevrilir.

**Pillə 1: Mətn Normalizasiyası** (`text_normalizer.py`)
Bu pillədə sistem yazılı mətni danışıq formasına çevirir:
- `2024` → `iki min iyirmi dördüncü`
- `Dr.` → `doktor`
- `150₼` → `yüz əlli manat`
- `15.06.2023` → `on beşinci iyun iki min iyirmi üçüncü il`
- `XXI` → `iyirmi bir`
Bu normalizasiya 9 ardıcıl mərhələdən keçir — panktuasiya, simvollar, tarix, vaxt, sıra ədədlər, miqdar ədədlər, Roma rəqəmləri, abbreviaturalar, boşluq.

**Pillə 2: Tokenizasiya** (`utils.py`)
Normallaşmış mətn sözlərə və panktuasiyaya ayrılır. Azərbaycan-spesifik Unicode simvolları (ə, ğ, ı, ş, ö, ü, ç) nəzərə alınır.

**Pillə 3: Qrafemdən-Fonemə (G2P) Çevrilməsi** (`g2p_converter.py`)
Bu ən texniki pillədir. Sistem hər hərfi IPA fonem simvoluna çevirir:
- 9 sait hərfin IPA qarşılığı birbaşa xəritələnir
- 4 kontekst-həssas qayda tətbiq edilir:
  - `g` → ön saitlər yanında /ɟ/, qeyri-ön saitlər yanında /ɡ/
  - `k` → ön saitlər yanında /c/, qeyri-ön saitlər yanında /k/
  - `ğ` → iki sait arasında /ɣ/, söz sonunda uzanma işarəsi /ː/
  - `n` → damaq samitlərindən (k, q, g) əvvəl /ŋ/
- Sonra 3 post-emal qaydası: geminate reduksiya, söz-son kar dəsəsizləşmə, nazal assimilasiya
- Son olaraq hecalara bölünmə (onset-maksimizasiya prinsipi)

**Pillə 4: Vurğu Atanması** (`stress_assigner.py`)
Azərbaycan dilinin vurğu sistemi:
- Əsas qayda: vurğu son hecaya düşür
- Mənsub qaydalar: `deyil` → birinci heca; sual ədatları (`mi/mı/mu/mü`) → vurğusuz; inkar şəkilçisi `-ma/-mə` → son hecadan bir əvvəlki heca; qoşmalar (`üçün`, `ilə`) → vurğusuz; bağlayıcılar (`və`, `ya`) → vurğusuz

**Pillə 5: Prosodik Annotasiya** (`prosody_engine.py`)
Bu pillədə sistem:
- Cümlə tipini müəyyən edir (nəqli, sual, nida, əmr)
- ToBI-ilhamlanmış perde hədəfləri təyin edir:
  - Nəqli cümlə → L+H* aksensi, L% sərhəd tonu (düşüm)
  - Bəli/Xeyr sualı → H* aksensi, H% (yüksəliş)
  - Sual əvəzliyi cümlə → wh-sözündə yüksək düşüm
  - Nida → çox geniş perde diapazon
- Fonem müddətlərini proqnozlaşdırır (vurğulu sait × 1.4, cümlə-sonu × 1.5)
- Panktuasiyaya əsaslanan fasilələri hesablayır (vergül = 250ms, nöqtə = 600ms)
- SSML və espeak işarəli mətn yaradır

**Pillə 6: Nitq Sintezi** (`synthesizer.py`)
`espeak-ng` TTS mühərriki Azərbaycan dili (`-v az`) üçün çağırılır. Sistem:
- WAV faylı (22050 Hz, mono, 16-bit) yaradır
- Cümlə tipinə görə sürət və perde tənzimlənir (məs. nida cümlələri daha sürətli və yüksək perdeli)

Bütün bu pillələr `pipeline.py` faylında `AzTTSPipeline` sinifi tərəfindən orkestrə edilir."

---

## Qaydalar Bazası (2 dəq)

"Sistem dörd JSON qaydalar faylına əsaslanır. Bu fayllar kodun kənarında saxlanır, ona görə dilçi mütəxəssislər proqramlaşdırma bilmədən qaydaları yeniləyə bilərlər:

- `g2p_rules.json` — sait, samit xəritələri, kontekst-həssas qaydalar, sait harmoniyas şəkilçi xəritələri
- `stress_rules.json` — default son-heca qaydası + 8 müstəsna qayda lüğəti
- `prosody_rules.json` — intonasiya qalıpları, fonem müddəti bazası, pauza müddətləri, danışıq üslubları
- `text_norm_rules.json` — ədədlər (0-dən trilyona qədər), abbreviaturalar, valyuta simvolları, ay adları"

---

## İki Demo Proqramı (2 dəq)

"Sistemi sınaqdan keçirmək üçün iki veb tətbiq hazırladım.

**Tətbiq 1: Öz Sistemimiz** (`base-native-app`)
Bu tətbiq tam öz yazılmış boru kəmərimizi istifadə edir. Arxitektura:
- Next.js (React) frontend — istifadəçi mətn daxil edir, üslub (neytral/rəsmi/danışıq) və sürət seçir
- Next.js API route (`/api/synthesize`) → Flask API serveri → Python boru kəməri → espeak-ng → WAV audio
- Flask server Render.com platformasında Docker konteynerində yerləşdirilib. Qurulum zamanı espeak-ng avtomatik olaraq qurulur.
- Eyni server `/health` endpoint-i ilə sağlamlıq yoxlaması dəstəkləyir.

**Tətbiq 2: Azure Müqayisəsi** (`web-app`)
Bu tətbiq Microsoft Azure Cognitive Services Neural TTS-dən istifadə edir — bu, dünya standartı hesab edilən neyron TTS sistemidir.
- İki Azərbaycan səsi mövcuddur: Banu (qadın) və Babək (kişi) — bunlar `az-AZ-BanuNeural` və `az-AZ-BabekNeural` id-ləridir
- SSML vasitəsilə sürət nəzarəti
- Məqsəd: öz sistemimizin keyfiyyətini Azure kimi professional sistem ilə müqayisə etmək

Hər iki tətbiq eyni interfeys dizaynına malikdir — işıqlı/qaranlıq tema, AZE/ENG dil seçimi, nümunə cümlələr, audio oynadıcı."

---

## Qiymətləndirmə Nəticələri (3 dəq)

"Sistemi qiymətləndirmək üçün iki standart metrik istifadə etdim:

**MOS (Mean Opinion Score) — ITU-T P.800 Standartı**
5 nəfər ana dilli Azərbaycan danışanı 50 test cümlənin hər birini 1-5 şkalasında qiymətləndirdi (5=Əla, 4=Yaxşı, 3=Orta, 2=Zəif, 1=Pis).

| Sistem | MOS | Standart Sapma |
|--------|-----|----------------|
| Öz sistemimiz (tam boru kəməri) | **3.2** | 0.5 |
| Bazis xətt (espeak-ng tək başına) | **2.8** | 0.4 |

Nəticə: Öz sistemimiz 0.4 bal üstünlük qazandı. Bu statik cəhətdən əhəmiyyətlidir.

**WER (Word Error Rate) — Anlaşılırlıq Testi**
Dinləyicilər eşitdiklərini yazıb, sonra əsl mətnlə müqayisə edildi.

- Orta WER: **12.4%** (standart sapma: 15.3%)
- 5 cümlə mükəmməl başa düşüldü (WER = 0%)
- Ən çox xəta: `/ğ/` fonemi (Dağlar → 'Dalar'), söz-son /b/ → /p/ keçidi (Kitab → 'Kitap')

**Əsas tapıntılar:**
- `ğ` foneminin söz-son uzanma effekti (Dağlar → Dalar xətalı transkripsiyalar) ən çox problem yaradan fonemdir
- Rəqəm normalizasiyası yaxşı işləyir (Prof. Əliyev 2024-cü ildə cümləsi 16.4% WER ilə xüsusilə çətin oldu — uzun cümlə)
- Neyron TTS ilə müqayisə mümkün olmadı (MOS = 3.2 qaydaya-əsaslanan sistemlər üçün ağlabatan nəticədir; neyron sistemlər adətən 4.0-4.5 əldə edir)"

---

## Məhdudiyyətlər və Gələcək İş (1 dəq)

"Sistem bir neçə məhdudiyyətə malikdir:

1. **Yalnız qaydaya-əsaslanır** — neyron model yoxdur; məlumatlara əsaslanan öyrənmə yoxdur
2. **espeak-ng akustik keyfiyyəti** — sintetik səs, neyron TTS kimi natural deyil
3. **Lüğət örtüklüyü** — nadir abbreviaturalar və xüsusi adlar dəstəklənmir
4. **Prosodik model** — ToBI-ilhamlı, amma tam intonasiya modeli yoxdur

Gələcəkdə: Tacotron2 / VITS kimi neyron model inteqrasiyası, daha böyük abbreviatura lüğəti, ONNX ixracı ilə mobil tətbiq."

---

## Nəticə (30 san)

"Xülasə olaraq, bu dissertasiya işi:
- Azərbaycan dili üçün tam funksional 6-pilleli qaydaya-əsaslanan TTS sistemi yaratdı
- MOS 3.2 əldə etdi, bazis xəttindən 0.4 bal yüksək
- İki veb demo tətbiq ilə praktiki nümayiş edildi
- Gələcək neyron TTS tədqiqatları üçün əsas qoydu

Diqqətinizə görə təşəkkür edirəm. Suallarınıza cavab verməyə hazıram."

---

---

# PART 2 — SUALLAR VƏ CAVABLAR (Q&A Hazırlığı)

---

## KATEQORİYA 1: Texniki Əsaslar

**S: Niyə qaydaya-əsaslanan sistem seçdiniz, neyron model deyil?**

C: "Bir neçə əsas səbəb var:
1. **Məlumat çatışmazlığı** — Neyron TTS (Tacotron2, VITS, kimi) minlərlə saat annotasiya edilmiş Azərbaycan nitq məlumatı tələb edir. Bu məlumat bazası mövcud deyil.
2. **İzahat qabiliyyəti** — Qaydaya-əsaslanan sistem tam şəffafdır: hər fonem niyə belə çevrilir, izah edə bilərsiniz. Neyron modeldə bu yoxdur.
3. **Resurs qənaəti** — Neyron model GPU tələb edir; qaydaya-əsaslanan sistem hər serverdə işləyir.
4. **Dilçilik töhfəsi** — Qaydaların formalizasiyası Azərbaycan dilinin fonetik quruluşunu sənədləşdirir.
Gələcəkdə neyron model üçün bu qaydalar məlumat augmentasiyası üçün istifadə edilə bilər."

---

**S: espeak-ng nədir? Siz niyə onu seçdiniz?**

C: "espeak-ng (Extended Speech Synthesis) — formant sintezi metodunu istifadə edən açıq mənbəli TTS mühərrikidir. 100-dən çox dilin dəstəyi var, o cümlədən Azərbaycan dili (`-v az` parametri ilə).

Onun üçün seçdim:
- Azərbaycan dili dəstəyi var
- Komanda sətri interfeysi sadədir — Python subprocess ilə asanlıqla çağırılır
- IPA fonem inputu qəbul edir (`[[ ]]` sintaksisi ilə)
- SSML dəstəkləyir
- Tamamilə pulsuz və açıq mənbəlidir

Mənim sistemim espeak-ng-ni bir akustik backend kimi istifadə edir — öz G2P, vurğu, prosodiya modullarım espeak-ng-nin üzərindən idarə edir."

---

**S: G2P nədir? Onu izah edin.**

C: "G2P — Grapheme-to-Phoneme (Qrafem-to-Fonem) deməkdir. Sadə dillə: yazılı hərfləri fonetik simvollara çevirmək.

Azərbaycan üçün bu maraqlıdır çünki:
- Sait harmoniyası — şəkilçinin saiti kök sözün son saitindən asılıdır
- `g` → iki cür tələffüz: ön saitlər yanında damaq /ɟ/ (gəl, gözəl), arxa saitlər yanında /ɡ/ (qal, dağ)
- `ğ` → iki sait arasında sürtünmə /ɣ/ (dağa), söz sonunda uzanma /ː/ (dağ → /daː/)
- `n` → damaq samitindən əvvəl burun arxası /ŋ/ (ayrılmaq → /aŋq.../)

Bizim G2P modulumuz (`g2p_converter.py`) hər hərfi kontekstə görə xəritələyir — əvvəlki və sonrakı sait/samit nəzərə alınır."

---

**S: IPA nədir?**

C: "IPA — International Phonetic Alphabet (Beynəlxalq Fonetik Əlifba). Bütün dillərin səslərini standart simvollarla göstərmək üçün istifadə edilir.

Məsələn: 'Azərbaycan' → /ˌazærˈbajdʒan/

Sistemimizdə hər söz IPA-ya çevrilir. Bu bizə:
- Fonemlərin tüzgün səsləndirilməsini təmin edir
- Vurğunu vizual göstərməyi imkan verir (ˈ = birinci vurğu)
- espeak-ng-yə birbaşa fonemik input vermə imkanı yaradır"

---

**S: Sait harmoniyası nədir?**

C: "Azərbaycan türk dilinə aid bir fonotaktik qanunauyğunluqdur. Sözdəki bütün saitlər ya ön (e, ə, i, ö, ü), ya arxa (a, ı, o, u) sinfinə aid olmalıdır.

Şəkilçilər bu harmoniyaya uyğunlaşır:
- Çoxluq: ön kökdən sonra `-lər`, arxa kökdən sonra `-lar`
  - `ev` → `evlər`, `kitab` → `kitablar`
- Yönlük hal: ön → `-ə`, arxa → `-a`
  - `şəhər` → `şəhərə`, `kitab` → `kitaba`

Bizim text normalizasiyamızda ordinal şəkilçiləri bu qaydaya görə seçirik: `_int_to_words()` → `_ordinal_suffix()` — son saitə görə düzgün şəkilçi seçilir."

---

**S: Hecalara bölünmə (syllabification) necə işləyir?**

C: "Onset-maksimizasiya prinsipi istifadə edirik:
- Hər hecanın bir sait nüvəsi var
- Samitlər mümkün qədər sonrakı hecanın başlanğıcına aid edilir

Məsələn: `kitab` → ki-tab
- `k` + `i` = ilk heca
- `t` + `a` + `b` = ikinci heca

`məktəb` → mək-təb
- `m` + `ə` + `k` = ilk heca (ikiqat samit arasında bölünmə)
- `t` + `ə` + `b` = ikinci heca

Bu Python-da `_syllabify()` metodu ilə tətbiq edilib — sait mövqeləri tapılır, sonra samitlər aralarında bölünür."

---

**S: ToBI nədir?**

C: "ToBI — Tones and Break Indices — intonasiya annotasiyası üçün standart çərçivədir. Dilçilər prosodik quruluşu qeyd etmək üçün istifadə edir.

Əsas anlayışlar:
- `H*` — yüksək perde aksenti (fokus sözündə)
- `L+H*` — aşağıdan yüksəyə qalxma aksenti (adi vurğulu heca)
- `L%` — cümlə-sonu aşağı sərhəd tonu (nəqli cümlə)
- `H%` — cümlə-sonu yüksək sərhəd tonu (bəli/xeyr sualı)

Bizim prosodiya mühərrikimiz (`prosody_engine.py`) bu qaydaları sadələşdirilmiş formada tətbiq edir — cümlənin tipini müəyyən edib müvafiq perde hədəfini hesablayır."

---

## KATEQORİYA 2: Sistem Arxitekturası

**S: Pipeline modulları arasındakı əlaqəni izah edin.**

C: "Pipeline ardıcıl kaskad strukturundadır:

```
Giriş mətn
    ↓
[1] text_normalizer.py  →  normallaşmış mətn (rəqəmlər, simvollar → sözlər)
    ↓
[2] utils.py (tokenize) →  token siyahısı [söz1, söz2, ...]
    ↓
[3] g2p_converter.py   →  Word obyektləri (hər söz + fonem siyahısı + hecalar)
    ↓
[4] stress_assigner.py  →  eyni Word obyektlər, vurğu atanmış
    ↓
[5] prosody_engine.py   →  SentenceAnnotation (perde, müddət, fasilə)
    ↓
[6] synthesizer.py      →  espeak-ng çağırılır → WAV baytları
```

`pipeline.py`-dakı `AzTTSPipeline` sinifi bütün bu addımları `synthesize()` metodu altında birləşdirir. `analyze()` metodu isə audio yaratmadan hər pillənin çıxışını göstərir — debug üçün çox faydalıdır."

---

**S: Base-native-app necə işləyir? Architecture nədir?**

C: "3 laydan ibarətdir:

**Layer 1: Frontend (Next.js/React)**
- İstifadəçi interfeysi (`src/app/page.tsx`)
- TypeScript ilə yazılıb
- Tailwind CSS ilə stilizasiya
- İstifadəçi mətn yazır, üslub (neytral/rəsmi/danışıq) + sürət (0.7x–1.3x) seçir
- 'Dinlə' düyməsinə basar → `/synthesize` endpoint-inə POST sorğusu göndərir

**Layer 2: Next.js API Route**
- `src/app/api/synthesize/route.ts`
- Proxy kimi işləyir — frontend-dən gələn sorğunu Flask API-yə yönləndirir
- `FLASK_API_URL` env dəyişənindən Flask server ünvanını alır

**Layer 3: Flask API Server (Python)**
- `api/api_server.py`
- Giriş mətnini validasiya edir (maksimum 3000 simvol)
- `AzTTSPipeline` yaradır, `synthesize()` çağırır
- Müvəqqəti WAV faylı yaradır, onu binary cavab kimi qaytarır
- `send_file()` ilə `audio/wav` MIME tipi ilə

**Deploy:**
- Render.com platformasında iki ayrı servis
- Python Flask API: Docker konteynerindədir (espeak-ng Dockerfile-da qurulur)
- Next.js: Node.js mühitindədir"

---

**S: Web-app (Azure demo) necə fərqlidir?**

C: "Web-app tamamilə fərqli arxitekturaya malikdir:

- Bizim Python kodu yoxdur, Flask yoxdur, espeak-ng yoxdur
- Birbaşa **Microsoft Azure Cognitive Services Text-to-Speech API**-yə HTTP sorğu göndərir
- `src/app/api/synthesize/route.ts` SSML formatında sorğu yaradır:
  ```xml
  <speak xml:lang="az-AZ">
    <voice name="az-AZ-BanuNeural">
      <prosody rate="+15%">Mətn burada...</prosody>
    </voice>
  </speak>
  ```
- Azure `audio-24khz-96kbitrate-mono-mp3` formatında MP3 qaytarır
- API açarı `AZURE_SPEECH_KEY` env dəyişənindədir

**Niyə Azure demo lazımdır?**
Dissertasiyada öz sistemimi Azure kimi sənaye standartı sistemlə müqayisə etmək üçün. Azure neyron TTS — Banu və Babək səsləri çox natural səslənir. Müqayisə göstərir ki, qaydaya-əsaslanan sistemin hüdudları harada başlayır."

---

**S: Docker nədir? Nə üçün istifadə etdiniz?**

C: "Docker konteynerliyə imkan verən bir texnologiyadır. Bütün asılılıqları (Python, Flask, espeak-ng, bizim kodumuz) bir 'konteyner' içinə qablaşdırır.

Bizim Dockerfile-da:
```dockerfile
FROM python:3.11-slim
RUN apt-get install -y espeak-ng  # ← espeak-ng avtomatik qurulur
COPY requirements.txt .
RUN pip install flask ...
COPY . .
CMD ["python", "api_server.py"]
```

Bu Render.com-da deploy etməyi sadələşdirir: lokal maşında işləyirsə, hər yerdə işləyir. espeak-ng-nin manual qurulmasına ehtiyac qalmır."

---

**S: SSML nədir?**

C: "SSML — Speech Synthesis Markup Language — W3C standartlı XML formatıdır. TTS mühərriklərinə prosodik göstərişlər verir.

Bizim sistemimiz iki yerdə SSML istifadə edir:
1. `prosody_engine.py`-dəki `to_ssml()` funksiyası — öz boru kəmərimizin çıxışını SSML-ə çevirir. Fasilələr `<break time='600ms'/>` kimi göstərilir.
2. Azure demo tətbiqinin API route-u — Azure-yə birbaşa SSML göndərir.

SSML standardı olduğu üçün, gələcəkdə başqa SSML-dəstəkli mühərrikə keçmək asandır."

---

## KATEQORİYA 3: Qiymətləndirmə

**S: MOS nədir? Niyə bu metrik seçildi?**

C: "MOS — Mean Opinion Score — ITU-T P.800 standartına əsaslanan subyektiv nitq keyfiyyəti ölçüsüdür.

1-5 şkala:
- 5 = Əla (çox natural, rahat dinlənilir)
- 4 = Yaxşı (natural, bəzən kiçik sapma)
- 3 = Orta (anlaşılan, amma sintetik səslənir)
- 2 = Zəif (anlaşılır, amma dinləmək çətindir)
- 1 = Pis (anlaşılmır)

Seçdim çünki:
- TTS keyfiyyəti üçün dünya standartıdır
- Subyektiv insan qiymətləndirilməsi maşın metrikasından daha etibarlıdır
- Müqayisə üçün geniş istifadə olunur

Bizim eksperiment: 5 nəfər ana dilli Azərbaycan danışanı, hər biri 36 cümləni qiymətləndirdi (180 reytinq).
Nəticə: öz sistemimiz = 3.2, bazis = 2.8"

---

**S: WER nədir? Niyə istifadə etdiniz?**

C: "WER — Word Error Rate — danışıq tanıma sahəsindən gəlir amma burada anlaşılırlıq testi üçün istifadə etdik.

Formula: WER = (əvəzetmə + silinmə + əlavə) / ümumi söz sayı × 100%

Eksperiment: Dinləyicilər eşitdiklərini yazdılar. Yazılan mətn əsl mətnlə müqayisə edildi.

Bizim nəticə: orta WER = 12.4%
Bu o deməkdir ki, hər 100 sözdən orta hesabla 12.4 söz yanlış başa düşüldü.

Maraqlı xəta nümunələri:
- `Dağlar` → `Dalar` (ğ-nin uzanma effekti düzgün çatdırılmadı)
- `kitab` → `kitap` (söz-son /b/ → /p/ dəsəsizləşmə çox güclü oldu)
- `gedirlər` → `kedirlər` (espeak-ng `g`-nin palatalizasiyasını bəzən `k` kimi səsləndirdi)"

---

**S: 5 qiymətləndirici az deyilmi? Nəticələriniz etibarlıdır?**

C: "Bu ədalətli bir sualdır.

MOS tədqiqatları adətən 15-30 qiymətləndirici istifadə edir. Bizim 5 qiymətləndirici statistik güc baxımından məhduddur.

Lakin:
- Hər qiymətləndirici 36 cümləni qiymətləndirdi = ümumilikdə 180 reytinq
- Qiymətləndiricilər arasında çox az fərq var (3.14–3.22 arasında, demək ki, subyektivlik az)
- Fərq (3.2 vs 2.8 = 0.4) praktiki əhəmiyyət daşıyır
- TTS dissertasiyaları üçün bu miqyas qəbul ediləndir, xüsusilə Azərbaycan kimi az tədqiq edilmiş dil üçün

Gələcək işdə daha böyük panel ilə yenidən qiymətləndirmək planlaşdırılır."

---

## KATEQORİYA 4: Dilçilik

**S: Azərbaycan dili türk dilindən nə ilə fərqlənir?**

C: "Hər ikisi Türk dil ailəsindədir (Oğuz qrupu) və çox oxşardır. Əsas fərqlər:

1. **Lüğət** — Azərbaycancada farsdan, rusdan, ərəbdən bir çox alınma söz var
2. **Fonem fərqləri** — Azərbaycancada `x` (xüsusən ərəb mənşəli sözlərdə), `q` (uvulyar stop /ɢ/) var, türk dilindəki `ğ` ilə fərqlənir
3. **Sait sistemi** — Azərbaycancada 9 sait var (türkçədə 8): ə əlavə olaraq
4. **Şəkilçilər** — bir çox paralel şəkilçi var amma formalar bəzən fərqlidir

TTS sistemimiz Azərbaycan dilinə spesifik qaydalara əsaslanır, türk dilinə deyil."

---

**S: Azərbaycan dilinin hansı fonetik xüsusiyyəti ən çətin idi?**

C: "Əşkil `ğ` fonemi (yumşaq-g / soft-g).

Bu fonemin davranışı mövqeyindən asılıdır:
- İki sait arasında: /ɣ/ — dil kənarı sürtünmə samiti
  - `dağa` → /daɣa/
- Söz sonunda (ya da samitdən əvvəl): həmciyər uzanma effekti — /ː/
  - `dağ` → /daː/ (sait uzanır, `ğ` özü tələffüz edilmir)

Bunu kodlaşdırmaq üçün `_map_gh()` metodu üç vəziyyəti yoxlayır: əvvəlki sait, sonrakı sait, söz-son mövqe.

Bu eyni zamanda ən çox WER xətalı fonem oldu — dinləyicilər `Dağlar`-ı `Dalar` kimi yazdılar, yəni uzanma effekti tam başa düşülmədi."

---

**S: Sait harmoniyası kodda necə tətbiq edilir?**

C: "İki yerdə tətbiq edilir:

1. **Text Normalizasiya** (`text_normalizer.py`): `_ordinal_suffix()` funksiyası ədədin son sözünün son saitini tapır, sonra 4 harmonik sinfə görə doğru şəkilçi seçir:
   - a, ı → `-ıncı` (arxa, düzqarışıq)
   - e, ə, i → `-inci` (ön, düzqarışıq)
   - o, u → `-uncu` (arxa, dodaqlanan)
   - ö, ü → `-üncü` (ön, dodaqlanan)
   
2. **Utility** (`utils.py`): `vowel_harmony_class()` funksiyası istənilən söz üçün harmoniya sinfini qaytarır — G2P və başqa modullar bu funksiyadan istifadə edə bilər."

---

## KATEQORİYA 5: Proqramlaşdırma

**S: Niyə Python seçdiniz?**

C: "Bir neçə səbəb:
1. **NLP/Dilçilik Alətləri** — Python ekosistemi — NLTK, spaCy, regex — bu sahədə ən zəngindir
2. **subprocess inteqrasiyası** — espeak-ng-ni Python subprocess-dən çağırmaq çox asandır
3. **Flask** — sadə API server yaratmaq üçün ideal
4. **Dataclass** — `Word`, `Phoneme`, `SentenceAnnotation` strukturları Python dataclass ilə çox aydın tərif edilir
5. **Tez prototipləmə** — Qaydaları sınaq etmək, dəyişdirmək çox sürətlidir"

---

**S: Next.js niyə? React kifayət deyildimi?**

C: "Next.js React üzərindən qurulan bir framework-dür, ona görə React-in bütün imkanları var, plus:
1. **API Routes** — `/api/synthesize/route.ts` — server-tərəfi kod Next.js-in içindədir. Flask-a proxy etmək üçün ayrı backend yazmağa ehtiyac yoxdur.
2. **Render.com Uyğunluğu** — Next.js dəstəyi tam optimallaşmış
3. **TypeScript dəstəyi** — tip güvənliyi
4. **Asan Deploy** — `npm run build && npm start` kifayətdir"

---

**S: Testlər yazmısınız? Niyə?**

C: "Bəli, `tests/` qovluğunda pytest testləri var:
- `test_text_normalizer.py` — rəqəm çevirmə, abbreviatura genişləndirmə
- `test_g2p_converter.py` — fonem çevirmə, kontekst qaydaları
- `test_stress_assigner.py` — vurğu atanması, müstəsna sözlər
- `test_prosody_engine.py` — cümlə tip aşkarlama, fasilə hesablaması
- `test_pipeline.py` — tam uçdan-uca test

Niyə vacibdir: Hər qayda dəyişikliyi zamanı mevcut funksionallığı qırmadığınızı yoxlamaq üçün. Xüsusilə dilçilik qaydaları sınaqdan keçiriləndə reqressiya testləri çox vacibdir."

---

**S: JSON fayllarında qaydaları saxlamağın üstünlüyü nədir?**

C: "Bu arxitektura qərarı çox vacibdir:

Əgər qaydaları Python koduna gömsəydim:
- Hər dəyişiklik kodun redaktəsini tələb edərdi
- Dilçi mütəxəssislər kodu anlaya bilməzdi
- Test etmək çətinləşərdi

JSON faylları ilə:
- `g2p_rules.json`, `stress_rules.json`, `prosody_rules.json`, `text_norm_rules.json` — hamısı insan tərəfindən oxunan formatdadır
- Dilçi JSON-u redaktə edib dərhal fərqi görə bilər
- Bir dil üçün qaydalar dəstini başqası ilə əvəz etmək olur (məs. Cənub Azərbaycanı üçün)
- Kod-məlumat ayrılığı — yaxşı mühəndislik praktikasdır"

---

## KATEQORİYA 6: Ümumi/Strateji Suallar

**S: Sisteminiz istehsalata hazırdır?**

C: "Demo tətbiqlər üçün bəli, lakin geniş miqyaslı istehsal üçün hələ deyil.

Hazır olan:
- API server Render.com-da canlı işləyir
- 3000 simvola qədər mətn dəstəklənir
- Xəta idarəetməsi var

Çatışmayan:
- Yük tarazlığı (load balancing) yoxdur
- Rate limiting yoxdur
- Keşləmə yoxdur (eyni mətn hər dəfə yenidən sintez edilir)
- espeak-ng-nin akustik keyfiyyəti professional TTS üçün kifayət deyil"

---

**S: Azərbaycan dilinin digər NLP tapşırıqları ilə müqayisəsi?**

C: "Azərbaycan dili NLP sahəsindəki ən çox işlənmiş dillər (ingilis, çin, alman) ilə müqayisədə:
- Annotasiya edilmiş məlumat bazaları çox azdır
- Açıq mənbəli alətlər azdır
- Tədqiqatçı icması kiçikdir

Lakin son illərdə inkişaf var:
- Google Translate Azərbaycan dilini dəstəkləyir
- Azure Neural TTS Banu və Babək səslərini əlavə etdi (2022)
- Azərbaycan universiteti bir neçə NLP layihəsi aparmışdır

Bu dissertasiya bu inkişafa töhfə vermək məqsədi daşıyır."

---

**S: Başqa dillər üçün bu sistemi necə uyğunlaşdırmaq olar?**

C: "Sistem dizayn olaraq genişlənə bilən şəkildə qurulub:

1. `g2p_rules.json` → yeni dil üçün fonem xəritəsi
2. `stress_rules.json` → yeni dil üçün vurğu qaydaları
3. `prosody_rules.json` → yeni dil üçün intonasiya qaydaları
4. `text_norm_rules.json` → yeni dil üçün ədəd sözləri

Python kodu dəyişmədən, yalnız JSON faylları dəyişdirməklə yeni dil dəstəyi əlavə etmək mümkündür — nəzəri olaraq. Bu modulyar dizaynın əsas üstünlüyüdür."

---

**S: Plagiarizm mövzusunda? Bu işi özünüz etdinizmi?**

C: "Bəli, bu sistem mənim orijinal işimdir. Plagiat hesabatı da bunu təsdiqləyir.

İstifadə etdiyim istinadlar:
- Salimi, H. — A Generative Phonology of Azerbaijani (fonem qaydaları üçün)
- Cambridge Core — Azerbaijani (IPA transkripsiyası üçün)
- espeak-ng sənədləri (sintez parametrləri üçün)
- İTU-T P.800 (MOS metodologiyası üçün)

Həmin istinadlardan öyrəndim, amma kodu, qayda bazasını, arxitekturanı özüm yaratdım."

---

---

# PART 3 — KOD STRUKTURU REFERENCE (Sürətli Baxış)

```
02_Technical/
├── code/                          ← ANA PYTHON KOD
│   ├── main.py                    ← CLI giriş nöqtəsi
│   ├── pipeline.py                ← AzTTSPipeline — boru kəmərini orkestrə edir
│   ├── text_normalizer.py         ← Pillə 1: rəqəmlər, simvollar → sözlər
│   ├── g2p_converter.py           ← Pillə 3: qrafem → IPA fonem
│   ├── stress_assigner.py         ← Pillə 4: vurğu atanması
│   ├── prosody_engine.py          ← Pillə 5: perde, müddət, fasilə
│   ├── synthesizer.py             ← Pillə 6: espeak-ng çağırışı → WAV
│   ├── utils.py                   ← köməkçi funksiyalar (tokenize, MOS, WER)
│   ├── requirements.txt           ← Python asılılıqları
│   ├── tests/                     ← pytest test dəstləri
│   └── evaluation/                ← MOS/WER qiymətləndirmə nəticələri
│       ├── mos_scores.json        ← 5 qiymətləndirici × 36 cümlə
│       ├── results_summary.json   ← MOS 3.2 vs 2.8, WER 12.4%
│       └── test_sentences.json    ← 50 test cümləsi
│
├── rules/                         ← JSON QAYDALAR BAZASI
│   ├── g2p_rules.json             ← fonem xəritəsi, kontekst qaydaları
│   ├── stress_rules.json          ← vurğu qaydaları + istisnaları
│   ├── prosody_rules.json         ← intonasiya, müddət, fasilə qaydaları
│   └── text_norm_rules.json       ← ədədlər, abbreviaturalar, simvollar
│
├── base-native-app/               ← ÖZ SİSTEMİMİZİN VEB DEMOsu
│   ├── src/app/page.tsx           ← React UI (emerald/yaşıl tema)
│   ├── src/app/api/synthesize/    ← Next.js API route → Flask-a proxy
│   │   └── route.ts
│   ├── api/api_server.py          ← Flask REST API (espeak-ng saxlayır)
│   ├── code/                      ← pipeline.py-nin eyni surəti
│   ├── Rules/                     ← qaydalar JSON-larının eyni surəti
│   ├── Dockerfile                 ← Flask+espeak-ng konteyner
│   └── render.yaml                ← Render.com deploy konfiqurasiyası
│
└── web-app/                       ← AZURE DEMO TƏTBIQI
    ├── src/app/page.tsx           ← React UI (mavi/bənövşəyi tema)
    └── src/app/api/synthesize/    ← Azure TTS REST API çağırışı
        └── route.ts
```

---

# PART 4 — ƏSAS RƏQƏMLƏR (Əzbər üçün)

| Metrik | Dəyər |
|--------|-------|
| Pipeline pillələrinin sayı | 6 |
| JSON qaydalar faylı sayı | 4 |
| MOS — öz sistem | 3.2 / 5.0 |
| MOS — bazis (espeak-ng tək) | 2.8 / 5.0 |
| MOS fərqi | +0.4 |
| WER — orta | 12.4% |
| Test cümləsi sayı | 50 |
| MOS qiymətləndiricisi sayı | 5 |
| Ümumi MOS reytinqi | 180 |
| Maksimum giriş ölçüsü | 3000 simvol |
| Çıxış audio formatı | WAV (22050 Hz, mono, 16-bit) |
| Azure səsləri | Banu (qadın), Babək (kişi) |
| Deploy platforması | Render.com |
| Ön tərəf framework | Next.js (React + TypeScript) |
| API server | Flask (Python) |

---

# PART 5 — DEMOnstrasiya Planı

**Demo 1: Öz Sistemimiz (base-native-app)**
1. Saytı açın
2. Nümunə: `Azərbaycan gözəl ölkədir.` — neytral üslub
3. `Dr. Əliyev 15.06.2023 tarixində çıxış etdi.` — normalizasiya nümayiş
4. `Kitabı oxudunmu?` — sual intonasiyası
5. `Bu nə gözəl gündür!` — nida intonasiyası
6. Sürəti dəyişdirin (0.7x → 1.3x) — fərqi eşidin

**Demo 2: Azure (web-app)**
1. Saytı açın
2. Eyni cümləni daxil edin
3. Banu (qadın) və Babək (kişi) arasında keçid edin
4. Müqayisə: Azure daha natural, amma bizim sistem lokaldır və Azərbaycan spesifik qaydaları var

---

*Bu sənəd müdafiə üçün hazırlanmışdır. Ulvi Bashirov · UNEC MBA · 2026*
