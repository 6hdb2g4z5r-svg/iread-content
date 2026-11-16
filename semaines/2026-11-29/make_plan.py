import json
CTA={'fr':"👉 Commandez dès maintenant via DM, WhatsApp ou sur www.iread.ma ✅",'en':"👉 Order now via DM, WhatsApp or on www.iread.ma ✅",'ar':"👉 اطلبه الآن عبر الرسائل الخاصة أو واتساب أو من موقعنا www.iread.ma ✅",'arp':"👉 اطلبها الآن عبر الرسائل الخاصة أو واتساب أو من موقعنا www.iread.ma ✅"}
DEL={'fr':"🚚 Livraison gratuite dès 3 livres · Paiement à la livraison",'en':"🚚 Free delivery from 3 books · Cash on delivery",'ar':"🚚 توصيل مجاني ابتداءً من 3 كتب · الدفع عند الاستلام"}
def cap(lang,body,tags,pack=False):
    return f"{body}\n\n{DEL[lang]}\n\n{tags}\n\n{CTA['arp' if (pack and lang=='ar') else lang]}"
P=[]
def T(d,h):
    m="11" if d>=29 else "12"
    return f"2026-{m}-{d:02d}T{h}:00+00:00"
def D(d): return f"2026-{'11' if d>=29 else '12'}-{d:02d}"
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
def spack(d,n,h,slugs,title,sub,lang,new=False): st(d,n,h,"Pack · "+title,"story_pack",{"cover_paths":[f"couvertures/{s}.jpg" for s in slugs],"title":title,"sub":sub,"dark":True,"kicker":PK[lang][1 if new else 0],"lang":lang,"cta":PK[lang][2]})
def spackph(d,n,h,photo,title,books,lang): st(d,n,h,"Pack · "+title,"story_pack_photo",{"photo_path":photo,"title":title,"books":books,"kicker":PK[lang][1],"lang":lang,"cta":PK[lang][2]})

B=json.load(open('boxes.json'))  # boxes de recadrage (vérifiées à la main)
def bx(k): return B.get(k)

# ───── Dimanche 29
sphoto(29,"photos/L'Attentat/l-attentat-aesthetic-1.jpg","L'Attentat","fr")
post(29,"12:00","inna-allah-maana","إن الله معنا",[ph("photos/إن الله معنا/inna-allah-maana-aesthetic-1.jpg"),pg("photos/إن الله معنا/inna-allah-maana-page-2.jpg",bx('inna2')),pg("photos/إن الله معنا/inna-allah-maana-page-1.jpg",bx('inna1'))],
 cap('ar',"🤍 إن الله معنا – فهد البشارة\n\nمن كاتب «فاستجبنا له»: كتاب يذكّرك في كل صفحة بأنك لست وحدك، وبأن الله معك في الضيق قبل الفرج.\n\nكلمات بسيطة تعيد الطمأنينة إلى القلب 🌙 اسحب لتقرأ صفحتين منه 👈",
 "#iRead #ireadma #إن_الله_معنا #فهد_البشارة #كتب_دينية #كتب_عربية #كتب_المغرب #Bookstagram"))
sext(29,"miracle-morning","photos/Miracle Morning/miracle-morning-page-1.jpg","Miracle Morning","Hal Elrod",bx('mm1'),"fr")
sab(29,"un-appartement-a-paris","elle-et-lui","Musso ou Levy ?","Deux plumes, deux Paris. Lequel ce week-end ?","Réponds en message","Musso ou Levy ?")
post(29,"16:30","crooked-kingdom","Crooked Kingdom",[ph("photos/Crooked Kingdom/crooked-kingdom-aesthetic-2.jpg"),pg("photos/Crooked Kingdom/crooked-kingdom-page-1.jpg",bx('ck1'))],
 cap('en',"🐦‍⬛ Crooked Kingdom – Leigh Bardugo\n\nThe heist is done. The payment never came. Betrayed and left for dead, Kaz Brekker and his crew are back in Ketterdam for revenge… and a fight for the soul of the city.\n\nThe sequel to Six of Crows, full of twists, loyalty and that Kaz & Inej slow burn 🖤 Swipe to read the page 👉",
 "#iRead #ireadma #CrookedKingdom #LeighBardugo #SixOfCrows #Grishaverse #BooksMorocco #Bookstagram"))
spack(29,4,"18:30",["the-hunger-games","catching-fire","mockingjay","sunrise-on-the-reaping"],"Hunger Games","The saga in 4 books, Sunrise on the Reaping included","en",True)
spack(29,5,"22:15",["1984-ar","mazraat-al-hayawan","al-umm-gorky","l-alchimiste-ar"],"كلاسيكيات عالمية","1984 · مزرعة الحيوان · الأم · الخيميائي","ar")

# ───── Lundi 30
sphoto(30,"photos/العرين/al-arin-kie-aesthetic-1.jpg","العرين","ar")
sext(30,"start-with-why","photos/Start With Why/start-with-why-page-2.jpg","Start With Why","Simon Sinek",bx('sww2'),"en")
scover(30,"la-nuit-sacree","La Nuit sacrée","Tahar Ben Jelloun","Le prix Goncourt 1987, un grand roman marocain.","fr")
spack(30,4,"18:30",["le-roi-du-silence","l-enfant-aux-cailloux","la-voisine-sans-histoire"],"Nuits blanches garanties","3 thrillers impossibles à lâcher","fr")
post(30,"21:25","pack-frissons-ar","Pack · رعب وتشويق",[ph("photos/PACK Frissons en arabe/frissons-ar-kie-pack-1.jpg")],
 cap('ar',"🕯️ باقة رعب وتشويق\n\nخوف 2 · الفيل الأزرق · الأسوأ · بحيرة الدماء\n\nأربع روايات عربية لعشاق الرعب والغموض: أسامة المسلم، أحمد مراد، عثمان عابد وعبدالله بوموزة… لا تقرأها وحدك في الليل 😶\n\n📚 الكتب الأربعة معًا بثمن مخفض",
 "#iRead #ireadma #روايات_رعب #الفيل_الأزرق #أسامة_المسلم #كتب_عربية #كتب_المغرب #Bookstagram",True),kind='post')
spack(30,5,"22:15",["taafayt","al-wahsh","kitab-al-raha","mulahazat-kawkab-mutawattir"],"اعتنِ بنفسك","4 كتب للراحة والتعافي","ar")

# ───── Mardi 1er
sphoto(1,"photos/La Peste/lapeste-aesthetic-3.jpg","La Peste","fr")
post(1,"12:00","liannaka-allah","لأنك الله",[ph("photos/لأنك الله: رحلة إلى السماء السابعة/liannaka-allah-aesthetic-2.jpg"),pg("photos/لأنك الله: رحلة إلى السماء السابعة/liannaka-allah-page-2.jpg",bx('lia2')),pg("photos/لأنك الله: رحلة إلى السماء السابعة/liannaka-allah-page-1.jpg",bx('lia1'))],
 cap('ar',"☁️ لأنك الله: رحلة إلى السماء السابعة – علي بن جابر الفيفي\n\nرحلة مع أسماء الله الحسنى: الصمد، الوكيل، اللطيف… في كل اسم طمأنينة جديدة، وفي كل صفحة باب للأمل.\n\nكتاب يقرأ بالقلب قبل العين 🤍 اسحب لتقرأ صفحتين منه 👈",
 "#iRead #ireadma #لأنك_الله #علي_الفيفي #أسماء_الله_الحسنى #كتب_عربية #كتب_المغرب #Bookstagram"))
sext(1,"al-jallad-tahta-jildi","photos/الجلاد تحت جلدي/al-jallad-tahta-jildi-page-1.jpg","الجلاد تحت جلدي","د. عماد رشاد عثمان",bx('jal1'),"ar")
sab(1,"1984-ar","mazraat-al-hayawan","1984 أم مزرعة الحيوان؟","روايتان لجورج أورويل، بأيهما تبدأ؟","أجب في رسالة","1984 أم مزرعة الحيوان ؟")
post(1,"16:30","dark-psychology-and-manipulation","Dark Psychology and Manipulation",[ph("photos/Dark Psychology and Manipulation/dark-psychology-and-manipulation-aesthetic-1.jpg"),pg("photos/Dark Psychology and Manipulation/dark-psychology-and-manipulation-page-2.jpg",bx('dp2')),pg("photos/Dark Psychology and Manipulation/dark-psychology-and-manipulation-page-1.jpg")],
 cap('en',"🕶️ Dark Psychology and Manipulation – William Cooper\n\nGuilt trips, playing the victim, charm used as a weapon… Learn how manipulators work, so you can spot them and protect yourself.\n\nAn eye-opening read you will think about every time someone \"just wants to help\" 👀 Swipe to read two pages 👉",
 "#iRead #ireadma #DarkPsychology #Manipulation #Psychology #SelfDefense #BooksMorocco #Bookstagram"))
spack(1,4,"18:30",["if-we-ever-meet-again","if-the-sun-never-sets","if-love-had-a-price","if-we-were-perfect"],"If Love","The 4 books of the If Love series","en",True)
spackph(1,5,"22:15","photos/PACK Frissons en arabe/frissons-ar-kie-pack-1.jpg","رعب وتشويق",["خوف 2","الفيل الأزرق","الأسوأ","بحيرة الدماء"],"ar")

# ───── Mercredi 2
sphoto(2,"photos/Le Prince/leprince-aesthetic-2.jpg","Le Prince","fr")
post(2,"12:00","shadow-and-bone","Shadow and Bone",[ph("photos/Shadow and Bone/shadow-and-bone-aesthetic-1.jpg"),pg("photos/Shadow and Bone/shadow-and-bone-page-2.jpg",bx('sab2'))],
 cap('en',"🦌 Shadow and Bone – Leigh Bardugo\n\nAlina Starkov is an orphan and a mapmaker… until an attack on the Shadow Fold reveals a power she never knew she had. Suddenly the Darkling wants her by his side.\n\nThe first book of the Grishaverse, where it all begins ✨ Swipe to read the page 👉",
 "#iRead #ireadma #ShadowAndBone #LeighBardugo #Grishaverse #Fantasy #BooksMorocco #Bookstagram"))
sext(2,"talk-like-ted","photos/Talk Like TED/talk-like-ted-page-4.jpg","Talk Like TED","Carmine Gallo",bx('ted4'),"en")
scover(2,"al-fil-al-azraq","الفيل الأزرق","أحمد مراد","رواية نفسية تشد أنفاسك حتى آخر صفحة","ar")
spack(2,4,"18:30",["mamlakat-al-ashrar","mamlakat-al-malunin","mamlakat-al-murabin"],"مملكة الأشرار","الثلاثية كاملة بالعربية","ar")
spack(2,5,"22:15",["the-first-90-days","the-1-page-marketing-plan","six-thinking-hats","limitless-jim-kwik"],"Career Boost","4 books to level up at work","en",True)

# ───── Jeudi 3
sphoto(3,"photos/The Wicked King/wicked-king-aesthetic-7.jpg","The Wicked King","en")
post(3,"12:00","al-layali-al-bayda","الليالي البيضاء",[ph("photos/الليالي البيضاء/al-layali-al-bayda-aesthetic-2.jpg",0.6),pg("photos/الليالي البيضاء/al-layali-al-bayda-page-1.jpg",bx("lay1")),pg("photos/الليالي البيضاء/al-layali-al-bayda-page-4.jpg",bx('lay4'))],
 cap('ar',"🌙 الليالي البيضاء – فيودور دوستويفسكي\n\nحالم وحيد يجوب شوارع بطرسبورغ في الليالي البيضاء، حتى يلتقي ناستينكا… أربع ليالٍ فقط تكفي لتغيّر قلبه إلى الأبد.\n\nرواية قصيرة عن الوحدة والحب والحلم، تُقرأ في جلسة واحدة 🤍 اسحب لتقرأ صفحتين منها 👈\n\n📚 متوفرة أيضًا في باقة دوستويفسكي بثمن مخفض",
 "#iRead #ireadma #الليالي_البيضاء #دوستويفسكي #روايات_عالمية #كتب_عربية #كتب_المغرب #Bookstagram"))
sext(3,"rasail-min-al-nabi","photos/رسائل من النبي ﷺ/rasail-min-al-nabi-page-1.jpg","رسائل من النبي ﷺ","أدهم شرقاوي",bx('ras1'),"ar")
sab(3,"it-ends-with-us","layla","It Ends with Us or Layla?","Two Colleen Hoover novels, two kinds of heartbreak. Your pick?","Answer by message","It Ends with Us ou Layla ?")
spack(3,4,"18:30",["le-bazar-du-zebre-a-pois","cupidon-a-des-ailes-en-carton","le-spleen-du-pop-corn"],"Dose de bonne humeur","3 romans feel-good pour l'hiver","fr")
spack(3,5,"22:15",["a-court-of-thorns-and-roses","a-court-of-mist-and-fury","a-court-of-wings-and-ruin","a-court-of-frost-and-starlight","a-court-of-silver-flames"],"ACOTAR 1 to 5","The complete saga by Sarah J. Maas","en",True)

# ───── Vendredi 4
sphoto(4,"photos/السجيل/al-sijjil-aesthetic-2.jpg","السجيل","ar")
post(4,"12:00","six-of-crows","Six of Crows",[ph("photos/Six of Crows/six-of-crows-aesthetic-2.jpg"),pg("photos/Six of Crows/six-of-crows-page-4.jpg",bx('soc4'))],
 cap('en',"🐦‍⬛ Six of Crows – Leigh Bardugo\n\nA convict, a sharpshooter, a runaway, a spy, a Heartrender and a thief. Six dangerous outcasts, one impossible heist: break into the Ice Court.\n\nThe Grishaverse duology everyone recommends, followed by Crooked Kingdom 🖤 Swipe to read the page 👉",
 "#iRead #ireadma #SixOfCrows #LeighBardugo #KazBrekker #Grishaverse #BooksMorocco #Bookstagram"))
sext(4,"the-lean-startup","photos/The Lean Startup/lean-startup-page-3.jpg","The Lean Startup","Eric Ries",bx('lean3'),"en")
scover(4,"plus-rien-ne-pourra-me-blesser","Plus rien ne pourra me blesser","David Goggins","Le mental d'acier d'un ancien Navy SEAL, en français.","fr")
spack(4,4,"18:30",["heartless-marissa-meyer","the-house-saphir"],"Marissa Meyer","Heartless · The House Saphir","en",True)
spackph(4,5,"22:15","photos/PACK Inheritance Games/inheritance-games-kie-pack-1.jpg","Inheritance Games",["The Final Gambit","The Brothers Hawthorne","Games Untold","The Grandest Game"],"en")

# ───── Samedi 5
sphoto(5,"photos/Chanson douce/chansondouce-aesthetic-3.jpg","Chanson douce","fr")
sext(5,"abi-alladhi-akrah","photos/أبي الذي أكره/abi-alladhi-akrah-page-1.jpg","أبي الذي أكره","",bx('abi1'),"ar")
sab(5,"l-attentat","les-amants-de-casablanca","Khadra ou Ben Jelloun ?","Deux grandes plumes du Maghreb. Laquelle ce week-end ?","Réponds en message","L'Attentat ou Les amants de Casablanca ?")
spack(5,4,"18:30",["brutal-prince","stolen-heir","bloody-heart","broken-vow","heavy-crown"],"Brutal Birthright","The 5 books by Sophie Lark","en",True)
post(5,"21:25","pack-inheritance-games","Pack · Inheritance Games",[ph("photos/PACK Inheritance Games/inheritance-games-kie-pack-1.jpg")],
 cap('en',"♟️ NEW PACK · Inheritance Games\n\nThe Final Gambit · The Brothers Hawthorne · Games Untold · The Grandest Game\n\nRiddles, secrets, a billion-dollar fortune and the Hawthorne brothers: Jennifer Lynn Barnes's addictive puzzle saga continues 🔑\n\n📚 The 4 books together at a discounted pack price",
 "#iRead #ireadma #InheritanceGames #JenniferLynnBarnes #TheGrandestGame #YAThriller #BooksMorocco #Bookstagram",True),kind='post')
spack(5,5,"22:15",["la-peste","la-chute","la-mort-heureuse"],"Albert Camus","La Peste · La Chute · La Mort heureuse","fr")

P.sort(key=lambda x:x['publish_at'])
json.dump(P,open('plan.json','w'),ensure_ascii=False,indent=1)
print(len(P), sum(1 for x in P if x['kind']!='story'))
