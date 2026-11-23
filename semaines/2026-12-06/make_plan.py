import json
CTA={'fr':"👉 Commandez dès maintenant via DM, WhatsApp ou sur www.iread.ma ✅",'en':"👉 Order now via DM, WhatsApp or on www.iread.ma ✅",'ar':"👉 اطلبه الآن عبر الرسائل الخاصة أو واتساب أو من موقعنا www.iread.ma ✅",'arp':"👉 اطلبها الآن عبر الرسائل الخاصة أو واتساب أو من موقعنا www.iread.ma ✅"}
DEL={'fr':"🚚 Livraison gratuite dès 3 livres · Paiement à la livraison",'en':"🚚 Free delivery from 3 books · Cash on delivery",'ar':"🚚 توصيل مجاني ابتداءً من 3 كتب · الدفع عند الاستلام"}
def cap(lang,body,tags,pack=False):
    return f"{body}\n\n{DEL[lang]}\n\n{tags}\n\n{CTA['arp' if (pack and lang=='ar') else lang]}"
P=[]
def T(d,h): return f"2026-12-{d:02d}T{h}:00+00:00"
def D(d): return f"2026-12-{d:02d}"
def post(d,h,slug,title,slides,caption,kind='carousel'):
    P.append({"id":f"post-{D(d)}-{slug}","kind":kind,"publish_at":T(d,h),"title":title,"caption":caption,"slides":slides})
def st(d,n,h,title,fn,args):
    P.append({"id":f"story-{D(d)}-{n}","kind":"story","publish_at":T(d,h),"title":title,"slides":[{"fn":fn,"args":args}]})
def ph(p,cy=0.5): return {"fn":"post_photo","args":{"photo_path":p,"cy":cy}}
def pg(p,box=None):
    a={"page_path":p}
    if box: a["box"]=box
    return {"fn":"post_page","args":a}
K={'fr':("Lecture du jour","Disponible sur iread.ma"),'en':("Today's read","Available on iread.ma"),'ar':("قراءة اليوم","متوفر على iread.ma")}
X={'fr':("Extrait","Commande en DM"),'en':("Excerpt","Order via DM"),'ar':("مقتطف","اطلبه عبر الرسائل")}
CV={'fr':("Coup de cœur","Commande en DM"),'en':("Staff pick","Order via DM"),'ar':("اختيارنا","اطلبه عبر الرسائل")}
PK={'fr':("Pack","Nouveau pack","Commande en DM ou sur iread.ma"),'en':("Pack","New pack","Order via DM or on iread.ma"),'ar':("باقة","باقة جديدة","اطلبها عبر الرسائل أو على iread.ma")}
def sphoto(d,p,title,lang): st(d,1,"10:00",title,"story_photo",{"photo_path":p,"title":title,"kicker":K[lang][0],"cta":K[lang][1],"lang":lang})
def sext(d,slug,page,title,author,box,lang):
    a={"cover_path":f"couvertures/{slug}.jpg","page_path":page,"title":title,"author":author,"kicker":X[lang][0],"cta":X[lang][1],"lang":lang}
    if box: a["box"]=box
    st(d,2,"12:45",("مقتطف · " if lang=='ar' else "Extrait · ")+title,"story_extract",a)
def scover(d,slug,title,author,tag,lang): st(d,3,"15:45","Coup de cœur · "+title,"story_cover",{"cover_path":f"couvertures/{slug}.jpg","title":title,"author":author,"tagline":tag,"kicker":CV[lang][0],"cta":CV[lang][1],"lang":lang})
def sab(d,a,b,q,sub,cta,title): st(d,3,"15:45",title,"story_ab",{"cover_a":f"couvertures/{a}.jpg","cover_b":f"couvertures/{b}.jpg","question":q,"sub":sub,"cta":cta})
def spack(d,n,h,slugs,title,sub,lang,new=True): st(d,n,h,"Pack · "+title,"story_pack",{"cover_paths":[f"couvertures/{s}.jpg" for s in slugs],"title":title,"sub":sub,"dark":True,"kicker":PK[lang][1 if new else 0],"lang":lang,"cta":PK[lang][2]})

# ───── Dimanche 6
sphoto(6,"photos/La Peste/lapeste-aesthetic-2.jpg","La Peste","fr")
post(6,"12:00","jismuka-yatadhakkar-kull-shay","جسمك يتذكر كل شيء",[ph("photos/جسمك يتذكر كل شيء/jismuka-yatadhakkar-kull-shay-aesthetic-1.jpg"),pg("photos/جسمك يتذكر كل شيء/jismuka-yatadhakkar-kull-shay-page-1.jpg"),pg("photos/جسمك يتذكر كل شيء/jismuka-yatadhakkar-kull-shay-page-2.jpg")],
 cap('ar',"🧠 جسمك يتذكر كل شيء – د. بيسيل فان دير كولك\n\nالدماغ والعقل والجسم في عملية الشفاء من الصدمة النفسية. ما نعيشه لا يبقى في الذاكرة فقط، بل يسكن الجسد أيضًا… وهذا الكتاب يشرح كيف نتعافى منه خطوة بخطوة.\n\nمن أهم الكتب في علم النفس في السنوات الأخيرة، بترجمة محمد الدخاخني 🤍 اسحب لتقرأ صفحتين منه 👈",
 "#iRead #ireadma #جسمك_يتذكر_كل_شيء #علم_النفس #التعافي #كتب_عربية #كتب_المغرب #Bookstagram"))
sext(6,"miracle-morning","photos/Miracle Morning/miracle-morning-page-2.jpg","Miracle Morning","Hal Elrod",None,"fr")
scover(6,"ils-se-sont-tant-aimes","Ils se sont tant aimés","Tahar Ben Jelloun","Une histoire d'amour et de séparation, par la plume de Tahar Ben Jelloun.","fr")
post(6,"16:30","maybe-someday","Maybe Someday",[ph("photos/Maybe Someday/maybe-someday-aesthetic-2.jpg"),pg("photos/Maybe Someday/maybe-someday-page-1.jpg")],
 cap('en',"🎸 Maybe Someday – Colleen Hoover\n\nSydney's life falls apart in one night. Then she meets Ridge, the mysterious guitarist on the balcony across from hers, and music becomes the only way they can talk about everything they're not allowed to feel.\n\nA love story that hurts and heals at the same time 💔 Swipe to read the page 👉",
 "#iRead #ireadma #MaybeSomeday #ColleenHoover #BookTok #RomanceBooks #BooksMorocco #Bookstagram"))
spack(6,4,"18:30",["la-theorie-let-them","un-rien-peut-tout-changer","miracle-morning"],"Reprendre sa vie en main","Let Them · Un rien peut tout changer · Miracle Morning","fr")
post(6,"21:25","pack-prendre-soin-de-soi","Pack · Prendre soin de soi",[ph("photos/PACK Prendre soin de soi/taafi-ar-kie-pack-1.jpg")],
 cap('ar',"🌿 باقة اعتنِ بنفسك\n\nتعافيت · الوحش الذي يسكنك يمكن أن يكون لطيفًا · كتاب الراحة · ملاحظات حول كوكب متوتر\n\nأربعة كتب لتهدئة القلق، والتصالح مع نفسك، والتعافي على مهل… مع كأس شاي في صباح هادئ 🍵\n\n📚 الكتب الأربعة معًا بثمن مخفض",
 "#iRead #ireadma #تعافيت #مات_هيغ #الصحة_النفسية #كتب_عربية #كتب_المغرب #Bookstagram",True),kind='post')
spack(6,5,"22:15",["al-ab-al-ghani","saykolojiyat-al-mal","aghna-rajul-fi-babil"],"المال","الأب الغني والأب الفقير · سيكولوجية المال · أغنى رجل في بابل","ar")

# ───── Lundi 7
sphoto(7,"photos/جمرة/jamra-aesthetic-1.jpg","جمرة","ar")
post(7,"12:00","why-we-sleep","Why We Sleep",[ph("photos/Why We Sleep/why-we-sleep-aesthetic-1.jpg"),pg("photos/Why We Sleep/why-we-sleep-page-2.jpg"),pg("photos/Why We Sleep/why-we-sleep-page-3.jpg")],
 cap('en',"🌙 Why We Sleep – Matthew Walker\n\nSleep is not a luxury: it repairs your memory, calms your emotions, protects your immune system and even helps you heal from painful days.\n\nA neuroscientist explains why one good night can change everything. You'll never scroll in bed again 😴 Swipe to read two pages 👉",
 "#iRead #ireadma #WhyWeSleep #MatthewWalker #Sleep #Neuroscience #BooksMorocco #Bookstagram"))
sext(7,"maybe-someday","photos/Maybe Someday/maybe-someday-page-3.jpg","Maybe Someday","Colleen Hoover",None,"en")
sab(7,"al-fil-al-azraq","antikhristos","الفيل الأزرق أم أنتيخريستوس؟","روايتان مرعبتان، بأيهما تبدأ؟","أجب في رسالة","الفيل الأزرق أم أنتيخريستوس ؟")
post(7,"16:30","part-of-your-world","Part of Your World",[ph("photos/Part of Your World/part-of-your-world-aesthetic-4.jpg"),pg("photos/Part of Your World/part-of-your-world-page-2.jpg",[0,0.405,1,0.74]),pg("photos/Part of Your World/part-of-your-world-page-1.jpg")],
 cap('en',"💛 Part of Your World – Abby Jimenez\n\nAlexis is a big-city doctor from a prestigious family. Daniel is a carpenter, ten years younger, from a tiny town in Minnesota. Two worlds that should never meet… and a love that doesn't care.\n\nFunny, tender and full of heart 🏡 Swipe to read the pages 👉",
 "#iRead #ireadma #PartOfYourWorld #AbbyJimenez #RomCom #RomanceBooks #BooksMorocco #Bookstagram"))
spack(7,4,"18:30",["atomic-habits","the-compound-effect","can-t-hurt-me"],"Mode Discipline ON","Atomic Habits · The Compound Effect · Can't Hurt Me","en")
spack(7,5,"22:15",["rasail-min-al-quran","nabd","ila-al-munkasira-qulubuhum"],"أدهم شرقاوي","رسائل من القرآن · نبض · إلى المنكسرة قلوبهم","ar")

# ───── Mardi 8
sphoto(8,"photos/الأيام التي ستأتي/al-ayyam-allati-sata-ti-aesthetic-3.jpg","الأيام التي ستأتي","ar")
post(8,"12:00","fantastic-beasts","Fantastic Beasts and Where to Find Them",[ph("photos/Fantastic Beasts and Where to Find Them/fantastic-beasts-aesthetic-4.jpg"),pg("photos/Fantastic Beasts and Where to Find Them/fantastic-beasts-page-1.jpg")],
 cap('en',"🪄 Fantastic Beasts and Where to Find Them – J.K. Rowling\n\nThe original screenplay: New York, 1926. Newt Scamander arrives with a suitcase full of magical creatures… and some of them escape.\n\nA beautiful edition for every Harry Potter fan, to read the film like a story ✨ Swipe to read the page 👉",
 "#iRead #ireadma #FantasticBeasts #JKRowling #HarryPotter #WizardingWorld #BooksMorocco #Bookstagram"))
sext(8,"jamra","photos/جمرة/jamra-page-2.jpg","جمرة","دعاء الجدعاني",None,"ar")
scover(8,"al-muzdawaj","المزدوج","دوستويفسكي","رواية دوستويفسكي عن رجل يلتقي نسخته الأخرى","ar")
spack(8,4,"18:30",["transformez-votre-vie","le-pouvoir-du-moment-present","ikigai-marion-kondo"],"Paix intérieure","Transformez votre vie · Le Pouvoir du moment présent · Ikigai","fr")
post(8,"21:25","pack-briar-u","Pack · Briar U",[ph("photos/PACK Briar U/briar-u-kie-pack-1.jpg")],
 cap('en',"🏒 PACK · Briar U\n\nThe Chase · The Risk · The Play · The Dare\n\nHockey players, college drama, banter and swoon-worthy slow burns: Elle Kennedy's Briar U series, the spin-off of Off-Campus 💙\n\n📚 The 4 books together at a discounted pack price",
 "#iRead #ireadma #BriarU #ElleKennedy #HockeyRomance #BookTok #BooksMorocco #Bookstagram",True),kind='post')
spack(8,5,"22:15",["ababil","al-sijjil","arsas-1"],"أحمد آل حمدان","أبابيل · السجيل · آرسس","ar")

# ───── Mercredi 9
sphoto(9,"photos/Le Prince/leprince-aesthetic-1.jpg","Le Prince","fr")
post(9,"12:00","blue-ocean-strategy","Blue Ocean Strategy",[ph("photos/Blue Ocean Strategy/blue-ocean-strategy-aesthetic-1.jpg"),pg("photos/Blue Ocean Strategy/blue-ocean-strategy-page-3.jpg",[0,0,1,0.535]),pg("photos/Blue Ocean Strategy/blue-ocean-strategy-page-2.jpg")],
 cap('en',"🌊 Blue Ocean Strategy – W. Chan Kim & Renée Mauborgne\n\nStop fighting your competitors in a bloody red ocean. Create a new market where the competition becomes irrelevant.\n\nThe expanded edition of the business classic, with real examples like Cirque du Soleil and NetJets 📈 Swipe to read two pages 👉",
 "#iRead #ireadma #BlueOceanStrategy #Business #Strategy #Entrepreneurship #BooksMorocco #Bookstagram"))
sext(9,"le-pouvoir-du-moment-present","photos/Le Pouvoir du moment présent/le-pouvoir-du-moment-present-page-1.jpg","Le Pouvoir du moment présent","Eckhart Tolle",[0,0.122,1,0.94],"fr")
sab(9,"the-hunger-games","a-court-of-thorns-and-roses","Hunger Games or ACOTAR?","Two sagas, two worlds. Which one are you starting?","Answer by message","Hunger Games ou ACOTAR ?")
post(9,"16:30","for-one-more-day","For One More Day",[ph("photos/For One More Day/for-one-more-day-aesthetic-2.jpg"),pg("photos/For One More Day/for-one-more-day-page-2.jpg",[0,0.265,1,0.6])],
 cap('en',"🏡 For One More Day – Mitch Albom\n\nWhat would you do if you could spend one more day with someone you lost? Charley, at the lowest point of his life, goes back to his childhood home… and finds his mother waiting for him.\n\nShort, moving and unforgettable, by the author of Tuesdays with Morrie 🤍 Swipe to read the page 👉",
 "#iRead #ireadma #ForOneMoreDay #MitchAlbom #Family #MustRead #BooksMorocco #Bookstagram"))
spack(9,4,"18:30",["deep-work","ego-is-the-enemy","the-mountain-is-you"],"Deep Focus","Deep Work · Ego Is the Enemy · The Mountain Is You","en")
spack(9,5,"22:15",["ard-zikola","amarita","wadi-al-dhiab"],"عمرو عبد الحميد","أرض زيكولا · أماريتا · وادي الذئاب المنسية","ar")

# ───── Jeudi 10
sphoto(10,"photos/Part of Your World/part-of-your-world-aesthetic-1.jpg","Part of Your World","en")
post(10,"12:00","the-miracle-morning","The Miracle Morning",[ph("photos/The Miracle Morning/the-miracle-morning-aesthetic-2.jpg"),pg("photos/The Miracle Morning/the-miracle-morning-page-1-redresse.jpg",[0.06,0.20,0.97,0.772])],
 cap('en',"🌅 The Miracle Morning – Hal Elrod\n\nWhat if the first hour of your day could change everything else? Silence, affirmations, visualization, exercise, reading, scribing: the Life S.A.V.E.R.S.\n\nThe original English edition of the morning-routine bestseller ☕ Swipe to read the page 👉",
 "#iRead #ireadma #TheMiracleMorning #HalElrod #MorningRoutine #SelfGrowth #BooksMorocco #Bookstagram"))
sext(10,"why-we-sleep","photos/Why We Sleep/why-we-sleep-page-1.jpg","Why We Sleep","Matthew Walker",[0,0.05,1,0.97],"en")
scover(10,"qawanin-al-taharrur","قوانين التحرر من الصراع النفسي","د. يوسف الحسني","لتفهم صراعاتك الداخلية وتتحرر منها","ar")
spack(10,4,"18:30",["la-femme-de-menage","les-secrets-de-la-femme-de-menage","la-femme-de-menage-voit-tout"],"La Femme de ménage","La trilogie de Freida McFadden, dans l'ordre","fr")
post(10,"21:25","pack-if-love","Pack · If Love",[ph("photos/PACK If Love/if-love-kie-pack-2.jpg")],
 cap('en',"🌹 PACK · If Love\n\nIf We Ever Meet Again · If the Sun Never Sets · If Love Had a Price · If We Were Perfect\n\nAna Huang's complete If Love series: second chances, forbidden feelings and love stories across Shanghai, New York and San Francisco 💌\n\n📚 The 4 books together at a discounted pack price",
 "#iRead #ireadma #IfLoveSeries #AnaHuang #RomanceBooks #BookTok #BooksMorocco #Bookstagram",True),kind='post')
spack(10,5,"22:15",["al-adat-al-sabaa-lil-nas","kayfa-tuathir","quwwat-aqlak-al-batin"],"النجاح","العادات السبع · كيف تكسب الأصدقاء · قوة عقلك الباطن","ar")

# ───── Vendredi 11
sphoto(11,"photos/رسائل من القرآن/rasail-min-al-quran-aesthetic-1.jpg","رسائل من القرآن","ar")
post(11,"12:00","the-secret-fiancee","The Secret Fiancée",[ph("photos/The Secret Fiancée/the-secret-fiancee-aesthetic-2.jpg"),pg("photos/The Secret Fiancée/the-secret-fiancee-page-2.jpg",[0,0.19,1,0.745])],
 cap('en',"🌻 The Secret Fiancée – Catharina Maura\n\nRaven needs a fake fiancé. Xavier has been waiting for his chance for years. A secret engagement, a lot of teasing… and feelings that are not fake at all.\n\nA cozy, funny and swoony romance by the author of The Wife Contract 💍 Swipe to read the page 👉",
 "#iRead #ireadma #TheSecretFiancee #CatharinaMaura #FakeDating #RomanceBooks #BooksMorocco #Bookstagram"))
sext(11,"al-layali-al-bayda","photos/الليالي البيضاء/al-layali-al-bayda-page-2.jpg","الليالي البيضاء","دوستويفسكي",[0,0.53,1,1],"ar")
sab(11,"que-serais-je-sans-toi","la-fille-de-papier","Quel Musso ce week-end ?","Que serais-je sans toi ? ou La Fille de papier","Réponds en message","Que serais-je sans toi ? ou La Fille de papier ?")
spack(11,4,"18:30",["the-let-them-theory","101-essays","healing-is-the-new-high"],"Self-Love","The Let Them Theory · 101 Essays · Healing Is the New High","en")
spack(11,5,"22:15",["mazraat-al-hayawan","al-amir-machiavelli","al-layali-al-bayda"],"كلاسيكيات عالمية","مزرعة الحيوان · الأمير · الليالي البيضاء","ar")

# ───── Samedi 12
sphoto(12,"photos/La Librairie de Téhéran/la-librairie-de-teheran-aesthetic-3.jpg","La Librairie de Téhéran","fr")
sext(12,"miracle-morning","photos/Miracle Morning/miracle-morning-page-3.jpg","Miracle Morning","Hal Elrod",None,"fr")
scover(12,"samarcande","Samarcande","Amin Maalouf","Omar Khayyam, un manuscrit perdu et mille ans d'histoire.","fr")
spack(12,4,"18:30",["rich-dad-poor-dad","the-soul-of-money","the-art-of-spending-money"],"Money Mindset","Rich Dad Poor Dad · The Soul of Money · The Art of Spending Money","en")
post(12,"21:25","pack-throne-of-glass-5-8","Pack · Throne of Glass 5-8",[ph("photos/PACK Throne of Glass 5-8/throne-of-glass-5-8-kie-pack-1.jpg")],
 cap('en',"🗡️ PACK · Throne of Glass, books 5 to 8\n\nQueen of Shadows · Empire of Storms · Tower of Dawn · Kingdom of Ash\n\nThe epic second half of Sarah J. Maas's saga: Aelin's return, war, dragons' riders, impossible choices and that ending 👑\n\n📚 The 4 books together at a discounted pack price",
 "#iRead #ireadma #ThroneOfGlass #SarahJMaas #Fantasy #Romantasy #BooksMorocco #Bookstagram",True),kind='post')
spack(12,5,"22:15",["al-khadima","al-marida-al-samita","mutalazimat-frigoli"],"تشويق نفسي","الخادمة · المريضة الصامتة · متلازمة فريجولي","ar")

P.sort(key=lambda x:x['publish_at'])
json.dump(P,open('plan.json','w'),ensure_ascii=False,indent=1)
print(len(P), sum(1 for x in P if x['kind']!='story'))
