import json
CTA={'fr':"👉 Commandez dès maintenant via DM, WhatsApp ou sur www.iread.ma ✅",'en':"👉 Order now via DM, WhatsApp or on www.iread.ma ✅",'ar':"👉 اطلبه الآن عبر الرسائل الخاصة أو واتساب أو من موقعنا www.iread.ma ✅",'arp':"👉 اطلبها الآن عبر الرسائل الخاصة أو واتساب أو من موقعنا www.iread.ma ✅"}
DEL={'fr':"🚚 Livraison gratuite dès 3 livres · Paiement à la livraison",'en':"🚚 Free delivery from 3 books · Cash on delivery",'ar':"🚚 توصيل مجاني ابتداءً من 3 كتب · الدفع عند الاستلام"}
def cap(lang,body,tags,pack=False):
    l='ar' if lang=='ar' else lang
    return f"{body}\n\n{DEL[l]}\n\n{tags}\n\n{CTA['arp' if (pack and lang=='ar') else l]}"
P=[]
def T(d,h): return f"2026-11-{d}T{h}:00+00:00"
def post(d,h,slug,title,slides,caption,kind='carousel'):
    P.append({"id":f"post-2026-11-{d}-{slug}","kind":kind,"publish_at":T(d,h),"title":title,"caption":caption,"slides":slides})
def st(d,n,h,title,fn,args):
    P.append({"id":f"story-2026-11-{d}-{n}","kind":"story","publish_at":T(d,h),"title":title,"slides":[{"fn":fn,"args":args}]})
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
def sext(d,slug,page,title,author,box,lang): st(d,2,"12:45",("مقتطف · " if lang=='ar' else "Extrait · ")+title,"story_extract",{"cover_path":f"couvertures/{slug}.jpg","page_path":page,"title":title,"author":author,"box":box,"kicker":X[lang][0],"cta":X[lang][1],"lang":lang})
def scover(d,slug,title,author,tag,lang): st(d,3,"15:45","Coup de cœur · "+title,"story_cover",{"cover_path":f"couvertures/{slug}.jpg","title":title,"author":author,"tagline":tag,"kicker":CV[lang][0],"cta":CV[lang][1],"lang":lang})
def sab(d,a,b,q,sub,cta,title): st(d,3,"15:45",title,"story_ab",{"cover_a":f"couvertures/{a}.jpg","cover_b":f"couvertures/{b}.jpg","question":q,"sub":sub,"cta":cta})
def spack(d,n,h,slugs,title,sub,lang,new=False): st(d,n,h,"Pack · "+title,"story_pack",{"cover_paths":[f"couvertures/{s}.jpg" for s in slugs],"title":title,"sub":sub,"dark":True,"kicker":PK[lang][1 if new else 0],"lang":lang,"cta":PK[lang][2]})
def spackph(d,n,h,photo,title,books,lang): st(d,n,h,"Pack · "+title,"story_pack_photo",{"photo_path":photo,"title":title,"books":books,"kicker":PK[lang][1],"lang":lang,"cta":PK[lang][2]})

# ───── Dimanche 22
sphoto(22,"photos/La Peste/lapeste-aesthetic-1.jpg","La Peste","fr")
post(22,"12:00","qawaid-jartin","قواعد جارتين",[ph("photos/قواعد جارتين/qawaid-jartin-aesthetic-1.jpg"),pg("photos/قواعد جارتين/qawaid-jartin-page-1.jpg"),pg("photos/قواعد جارتين/qawaid-jartin-page-2.jpg")],
 cap('ar',"⚔️ قواعد جارتين – عمرو عبد الحميد\n\nعالم جديد من خيال مؤلف ثنائية أرض زيكولا: بلدة لها قواعدها الصارمة، ولكل قاعدة ثمن… ومن يجرؤ على كسرها يدفعه غاليًا.\n\nفانتازيا وتشويق من الصفحة الأولى 🔥 اسحب لتقرأ صفحتين منها 👈",
 "#iRead #ireadma #عمرو_عبد_الحميد #قواعد_جارتين #أرض_زيكولا #فانتازيا #كتب_المغرب #Bookstagram"))
sext(22,"ego-is-the-enemy","photos/Ego Is the Enemy/ego-is-the-enemy-page-3.jpg","Ego Is the Enemy","Ryan Holiday",[0.05,0.325,1,0.567],"en")
scover(22,"le-passe-simple","Le Passé simple","Driss Chraïbi","Le roman marocain qui a fait scandale en 1954.","fr")
spack(22,4,"18:30",["un-appartement-a-paris","sept-ans-apres","la-fille-de-papier","que-serais-je-sans-toi","je-reviens-te-chercher","sauve-moi"],"Musso Addict","6 romans de Guillaume Musso réunis","fr")
post(22,"21:25","pack-maple-hills","Pack · Maple Hills",[ph("photos/PACK Maple Hills/maple-hills-kie-pack-1.jpg")],
 cap('en',"🏒 NEW PACK · Maple Hills\n\nIcebreaker · Daydream\n\nHannah Grace's hockey romances: Anastasia and Nate forced to share the ice, then Halle and Henry between books and matches. Cozy, funny and swoony, perfect for winter nights ❄️\n\n📚 The 2 books together at a discounted pack price",
 "#iRead #ireadma #MapleHills #Icebreaker #HannahGrace #HockeyRomance #BooksMorocco #Bookstagram",True),kind='post')
spackph(22,5,"22:15","photos/PACK أنتيخريستوس/antikhristos-ar-kie-pack-1.jpg","أنتيخريستوس 1 و 2",["أنتيخريستوس","أنتيخريستوس II"],"ar")

# ───── Lundi 23
sphoto(23,"photos/Fearless/fearless-aesthetic-1.jpg","Fearless","en")
post(23,"12:00","la-librairie-de-teheran","La Librairie de Téhéran",[ph("photos/La Librairie de Téhéran/la-librairie-de-teheran-aesthetic-1.jpg"),pg("photos/La Librairie de Téhéran/la-librairie-de-teheran-page-2.jpg",[0,0,1,0.755])],
 cap('fr',"📚 La Librairie de Téhéran – Marjan Kamali\n\nTéhéran, été 1953. Dans une petite librairie de quartier, Roya rencontre Bahman : un premier amour, des poèmes de Rûmî… puis un rendez-vous manqué au milieu d'un coup d'État. Soixante ans plus tard, leurs chemins se croisent à nouveau.\n\nUne histoire d'amour bouleversante au doux parfum d'Iran 🌹 Glissez pour lire la page 👉\n\n📚 Aussi dans notre pack « Le goût des livres » (prix réduit)",
 "#iRead #ireadma #LaLibrairieDeTeheran #MarjanKamali #RomanDAmour #LivreMaroc #Bookstagram #LectureDuMoment"))
sext(23,"jamra","photos/جمرة/jamra-page-1.jpg","جمرة","دعاء الجدعاني",[0.2,0.475,0.76,0.655],"ar")
sab(23,"les-amants-de-casablanca","regardez-nous-danser","Ben Jelloun ou Slimani ?","Deux plumes marocaines, deux romans. Lequel ce mois-ci ?","Réponds en message","Les amants de Casablanca ou Regardez-nous danser ?")
post(23,"16:30","fastajabna-lah","فاستجبنا له",[ph("photos/فاستجبنا له/fastajabna-lah-aesthetic-1.jpg"),pg("photos/فاستجبنا له/fastajabna-lah-page-1.jpg",[0,0,0.885,1])],
 cap('ar',"🤍 فاستجبنا له – فهد البشارة\n\nرواية عن العائلة والصبر وقوة الدعاء، عن الانتظار الطويل وعن يقين بأن الله يسمع.\n\nحكاية دافئة تلامس القلب 🌅 اسحب لتقرأ صفحة منها 👈",
 "#iRead #ireadma #فهد_البشارة #فاستجبنا_له #روايات #كتب_عربية #كتب_المغرب #Bookstagram"))
spack(23,4,"18:30",["this-is-marketing","influence-cialdini","blue-ocean-strategy","good-to-great"],"Marketing & stratégie","Seth Godin, Cialdini, Blue Ocean & Jim Collins","en",True)
post(23,"21:25","pack-hajar-al-shams-ar","Pack · حجر الشمس",[ph("photos/PACK حجر الشمس/hajar-al-shams-ar-kie-pack-1.jpg")],
 cap('ar',"☀️ باقة جديدة · حجر الشمس\n\nسماء بلا ضياء · إعصار بلا قرار · نار بلا شرار\n\nسلسلة خولة حمدي كاملة بأجزائها الثلاثة: مغامرة وفانتازيا وأسرار تتكشف جزءًا بعد جزء… ابدأها ولن تتوقف ✨\n\n📚 الأجزاء الثلاثة معًا بثمن مخفض",
 "#iRead #ireadma #خولة_حمدي #حجر_الشمس #روايات #كتب_عربية #كتب_المغرب #Bookstagram",True),kind='post')
spack(23,5,"22:15",["hopeless-colleen-hoover","maybe-now","reminders-of-him","confess-colleen-hoover"],"Colleen Hoover 2","Hopeless · Maybe Now · Reminders of Him · Confess","en",True)

# ───── Mardi 24
sphoto(24,"photos/قواعد العشق الأربعون/quarante-regles-de-l-amour-ar-aesthetic-1.jpg","قواعد العشق الأربعون","ar")
post(24,"12:00","the-secret","The Secret",[ph("photos/The Secret/the-secret-rhonda-byrne-aesthetic-1.jpg"),pg("photos/The Secret/the-secret-rhonda-byrne-page-1.jpg"),pg("photos/The Secret/the-secret-rhonda-byrne-page-2.jpg")],
 cap('en',"✨ The Secret – Rhonda Byrne\n\nThe book that made millions of readers believe in the law of attraction: your thoughts shape your life, so choose them well.\n\nEasy to read, hard to forget, and perfect to end the year with the right mindset. Swipe for two highlighted pages 👉",
 "#iRead #ireadma #TheSecret #RhondaByrne #LawOfAttraction #Mindset #BooksMorocco #Bookstagram"))
sext(24,"la-chute","photos/La Chute/lachute-page-1.jpg","La Chute","Albert Camus",[0.07,0.2,0.81,0.507],"fr")
scover(24,"a-tale-of-two-cities","A Tale of Two Cities","Charles Dickens","Love, sacrifice and revolution between London and Paris.","en")
post(24,"16:30","azmat-rujula","أزمة رجولة",[ph("photos/أزمة رجولة/azmat-rujula-aesthetic-2.jpg"),pg("photos/أزمة رجولة/azmat-rujula-page-1.jpg"),pg("photos/أزمة رجولة/azmat-rujula-page-2.jpg")],
 cap('ar',"🌹 أزمة رجولة – فاتن حمود\n\nنصوص قصيرة عن الحب والكرامة والنضج، تقول ما نشعر به ولا نجرؤ دائمًا على قوله… وتذكّرنا بأن نمنح أنفسنا الحب أولًا.\n\nاسحب لتقرأ صفحتين منه 👈",
 "#iRead #ireadma #فاتن_حمود #أزمة_رجولة #خواطر #كتب_عربية #كتب_المغرب #Bookstagram"))
spack(24,4,"18:30",["le-pouvoir-du-moment-present","le-pouvoir-des-habitudes","miracle-morning","l-obstacle-est-le-chemin"],"Nouveau départ","4 livres pour reprendre sa vie en main","fr")
spackph(24,5,"22:15","photos/PACK Maple Hills/maple-hills-kie-pack-1.jpg","Maple Hills",["Icebreaker","Daydream"],"en")

# ───── Mercredi 25
sphoto(25,"photos/Chanson douce/chansondouce-aesthetic-1.jpg","Chanson douce","fr")
post(25,"12:00","al-marida-al-samita","المريضة الصامتة",[ph("photos/المريضة الصامتة/al-marida-al-samita-aesthetic-1.jpg"),pg("photos/المريضة الصامتة/al-marida-al-samita-page-2.jpg",[0,0,1,0.957]),pg("photos/المريضة الصامتة/al-marida-al-samita-page-1.jpg",[0,0,1,0.962])],
 cap('ar',"🎨 المريضة الصامتة – ألكس ميكايليديس\n\nأليشيا رسامة مشهورة أطلقت النار على زوجها 5 مرات… ثم لم تنطق بكلمة واحدة بعدها. المعالج النفسي ثيو مصمم على أن يجعلها تتكلم.\n\nتشويق نفسي بنهاية لن تتوقعها أبدًا 😶 اسحب لتقرأ صفحة منها 👈\n\n📚 متوفرة أيضًا في باقة روايات التشويق النفسي بثمن مخفض",
 "#iRead #ireadma #المريضة_الصامتة #ألكس_ميكايليديس #روايات_تشويق #كتب_عربية #كتب_المغرب #Bookstagram"))
sext(25,"two-twisted-crowns","photos/Two Twisted Crowns/two-twisted-crowns-page-1.jpg","Two Twisted Crowns","Rachel Gillig",[0.01,0.35,0.985,0.59],"en")
sab(25,"l-alchimiste-ar","alam-sofi","الخيميائي أم عالم صوفي؟","روايتان عن البحث عن المعنى، بأيهما تبدأ؟","أجب في رسالة","الخيميائي أم عالم صوفي ؟")
spack(25,4,"18:30",["shatter-me","unravel-me","ignite-me","restore-me","defy-me","imagine-me"],"Shatter Me 1–6","The complete saga by Tahereh Mafi","en",True)
post(25,"21:25","pack-dark-romantasy","Pack · Dark Romantasy",[ph("photos/PACK Dark Romantasy/dark-romantasy-kie-pack-1.jpg")],
 cap('en',"🖤 NEW PACK · Dark Romantasy\n\nPhantasma · Heartless Hunter · The Atlas Complex\n\nDeadly games, witch hunters and secret magical societies: three dark, addictive fantasies with an impossible love at their heart 🗡️\n\n📚 The 3 books together at a discounted pack price",
 "#iRead #ireadma #DarkRomantasy #Phantasma #HeartlessHunter #TheAtlasComplex #BooksMorocco #Bookstagram",True),kind='post')
spack(25,5,"22:15",["al-awsaj","al-awsaj-2"],"العوسج 1 و 2","رواية الجوهرة الرمال بجزأيها","ar",True)

# ───── Jeudi 26
sphoto(26,"photos/Le Rocher de Tanios/le-rocher-de-tanios-aesthetic-1.jpg","Le Rocher de Tanios","fr")
post(26,"12:00","no-excuses","No Excuses!",[ph("photos/No Excuses!/no-excuses-aesthetic-3.jpg"),pg("photos/No Excuses!/no-excuses-page-1.jpg",[0,0,1,0.669])],
 cap('en',"🚫 No Excuses! – Brian Tracy\n\nThe power of self-discipline in 21 practical ways: for your goals, your work, your money, your health and your relationships.\n\nIf this year was full of \"tomorrow\", let this be the book that turns it into \"today\" 💪 Swipe for the page 👉\n\n📚 Also in our Self-Discipline pack (discounted price)",
 "#iRead #ireadma #NoExcuses #BrianTracy #SelfDiscipline #Productivity #BooksMorocco #Bookstagram"))
sext(26,"al-ayyam-allati-sata-ti","photos/الأيام التي ستأتي/al-ayyam-allati-sata-ti-page-2.jpg","الأيام التي ستأتي","",[0.05,0.47,1,0.79],"ar")
scover(26,"mazraat-al-hayawan","مزرعة الحيوان","جورج أورويل","حكاية رمزية خالدة عن السلطة والحرية","ar")
post(26,"16:30","saykolojiyat-al-mal","سيكولوجية المال",[ph("photos/سيكولوجية المال/saykolojiyat-al-mal-aesthetic-1.jpg"),pg("photos/سيكولوجية المال/saykolojiyat-al-mal-page-1.jpg")],
 cap('ar',"💰 سيكولوجية المال – مورجان هاوسل\n\nالنجاح المالي لا يتعلق بما تعرفه، بل بطريقة تصرفك. 19 قصة قصيرة عن الطمع والخوف والصبر، وعن علاقتنا الغريبة بالمال.\n\nكتاب يغيّر نظرتك إلى المال والسعادة 📈 اسحب لتقرأ 👈\n\n📚 متوفر أيضًا في باقة المال بثمن مخفض",
 "#iRead #ireadma #سيكولوجية_المال #مورجان_هاوسل #المال #تطوير_الذات #كتب_المغرب #Bookstagram"))
spack(26,4,"18:30",["elle-et-lui","si-c-etait-a-refaire","l-etrange-voyage-de-monsieur-daldry","marc-levy-9"],"Marc Levy","4 romans pour voyager et aimer","fr")
spackph(26,5,"22:15","photos/PACK حجر الشمس/hajar-al-shams-ar-kie-pack-1.jpg","حجر الشمس",["سماء بلا ضياء","إعصار بلا قرار","نار بلا شرار"],"ar")

# ───── Vendredi 27
sphoto(27,"photos/Et que Dieu me pardonne/et-que-dieu-me-pardonne-aesthetic-1.jpg","Et que Dieu me pardonne","fr")
post(27,"12:00","awwal-marra-atadabbar","أول مرة أتدبر القرآن",[ph("photos/أول مرة أتدبر القرآن/awwal-marra-atadabbar-aesthetic-1.jpg"),pg("photos/أول مرة أتدبر القرآن/awwal-marra-atadabbar-page-1.jpg")],
 cap('ar',"📖 أول مرة أتدبر القرآن – عادل محمد خليل\n\nدليلك لفهم وتدبر القرآن من سورة الفاتحة إلى سورة الناس: فوائد ولطائف ومعانٍ قريبة من القلب، بأسلوب بسيط يناسب الجميع.\n\nرفيق جميل لكل جمعة 🤍 اسحب لتقرأ صفحة منه 👈",
 "#iRead #ireadma #أول_مرة_أتدبر_القرآن #تدبر_القرآن #القرآن_الكريم #كتب_عربية #كتب_المغرب #Bookstagram"))
sext(27,"without-merit","photos/Without Merit/without-merit-page-1.jpg","Without Merit","Colleen Hoover",[0.1,0.466,0.86,0.597],"en")
sab(27,"atomic-habits","the-compound-effect","Atomic Habits or The Compound Effect?","Two books, one idea: small steps, big results. Your pick?","Answer by message","Atomic Habits ou The Compound Effect ?")
spack(27,4,"18:30",["al-jallad-tahta-jildi","mumtali-bil-faragh"],"عماد رشاد عثمان","الجلاد تحت جلدي · ممتلئ بالفراغ","ar",True)
post(27,"21:25","pack-antikhristos-ar","Pack · أنتيخريستوس 1 و 2",[ph("photos/PACK أنتيخريستوس/antikhristos-ar-kie-pack-1.jpg")],
 cap('ar',"🔥 باقة جديدة · أنتيخريستوس 1 و 2\n\nأنتيخريستوس · أنتيخريستوس II\n\nالرواية التي أثارت الجدل لـ د. أحمد خالد مصطفى مع جزئها الثاني: رحلة مظلمة بين التاريخ والأسرار والأساطير… هل تجرؤ على قراءتها؟ 🕯️\n\n📚 الجزآن معًا بثمن مخفض",
 "#iRead #ireadma #أنتيخريستوس #أحمد_خالد_مصطفى #روايات #كتب_عربية #كتب_المغرب #Bookstagram",True),kind='post')
spack(27,5,"22:15",["wild-eyes-elsie-silver","wild-side-elsie-silver","wildcard-elsie-silver"],"Rose Hill","Wild Eyes · Wild Side · Wildcard","en",True)

# ───── Samedi 28
sphoto(28,"photos/The Secret Fiancée/the-secret-fiancee-aesthetic-1.jpg","The Secret Fiancée","en")
post(28,"12:00","nazariyat-al-taghafful","نظرية التغافل",[ph("photos/نظرية التغافل/nazariyat-al-taghafful-aesthetic-1.jpg"),pg("photos/نظرية التغافل/nazariyat-al-taghafful-page-2.jpg"),pg("photos/نظرية التغافل/nazariyat-al-taghafful-page-1.jpg")],
 cap('ar',"🌿 نظرية التغافل – ميل روبينز وسوير روبينز\n\nالنسخة العربية من The Let Them Theory: دعهم يفعلون ما يريدون، واصرف طاقتك على ما يمكنك التحكم فيه. فكرة بسيطة غيّرت حياة الملايين.\n\nاسحب لتقرأ 👈\n\n📚 متوفر أيضًا في باقة «ثقي بنفسك» بثمن مخفض",
 "#iRead #ireadma #نظرية_التغافل #ميل_روبينز #تطوير_الذات #كتب_عربية #كتب_المغرب #Bookstagram"))
sext(28,"le-prince","photos/Le Prince/leprince-page-4.jpg","Le Prince","Nicolas Machiavel",[0,0.247,1,0.686],"fr")
scover(28,"un-rien-peut-tout-changer","Un rien peut tout changer !","James Clear","La version française d'Atomic Habits.","fr")
post(28,"16:30","unuthat-taghiya","أنوثة طاغية",[ph("photos/أنوثة طاغية/unuthat-taghiya-aesthetic-2.jpg"),pg("photos/أنوثة طاغية/unuthat-taghiya-page-1.jpg",[0.075,0,1,1])],
 cap('ar',"🌸 أنوثة طاغية – هالة بنت محمد غبان\n\nلكل أنثى حقيقية، محبة، قادرة على النجاح: كتاب عن الثقة بالنفس والأنوثة، وعن التغيير الذي يبدأ من الداخل.\n\nاسحب لتقرأ صفحة منه 👈\n\n📚 متوفر أيضًا في باقة «ثقي بنفسك» بثمن مخفض",
 "#iRead #ireadma #أنوثة_طاغية #هالة_غبان #تطوير_الذات #كتب_عربية #كتب_المغرب #Bookstagram"))
spack(28,4,"18:30",["plus-rien-ne-pourra-me-blesser","reflechissez-riche-journal","365-lois"],"Mental de champion","Goggins, Napoleon Hill et Robert Greene","fr")
spackph(28,5,"22:15","photos/PACK Dark Romantasy/dark-romantasy-kie-pack-1.jpg","Dark Romantasy",["Phantasma","Heartless Hunter","The Atlas Complex"],"en")

P.sort(key=lambda x:x['publish_at'])
json.dump(P,open('plan.json','w'),ensure_ascii=False,indent=1)
print(len(P), sum(1 for x in P if x['kind']!='story'))
