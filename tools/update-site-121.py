# One-off site update for app v1.2.1 (UI 2.0). Run from the sofra-site repo root:
#   python tools/update-site-121.py
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(f): return open(os.path.join(ROOT, f), encoding='utf-8').read()
def wr(f, s): open(os.path.join(ROOT, f), 'w', encoding='utf-8', newline='\n').write(s)
def rep(s, a, b, f=''):
    assert a in s, f'{f}: missing -> {a[:80]}'
    return s.replace(a, b, 1)

PLAY = 'https://play.google.com/store/apps/details?id=com.thaliplan.app'
APPLE = 'https://apps.apple.com/app/id6797710095'
SITE = 'https://sofra.savvylabs.dev'

def ico(color, inner):
    return (f'<div class="ic tint-{color}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round" style="color:var(--{color})">{inner}</svg></div>')

# ───────────────────────── index.html ─────────────────────────
s = rd('index.html')
s = rep(s, "<title>Sofra — Your family's meal memory</title>",
        "<title>Sofra — Family meal planner that remembers what you cook</title>", 'index')
s = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="Sofra is a free family meal planner that plans your week from the meals your family already loves — with your own dish photos, tomorrow\'s plan every evening, a shared grocery list and kids lunchbox planning. No ads.">', s, 1)
s = re.sub(r'<meta property="og:description" content="[^"]*">',
           '<meta property="og:description" content="Your family\'s meals, remembered and planned. Plan the week from the dishes you already cook — free, no ads.">', s, 1)

# Kids card + new feature cards
old_kids = re.search(r'<div class="card"><div class="ic tint-kids">.*?<h3>Kids tiffin track</h3>.*?</div>\n', s).group(0)
new_cards = (
    old_kids.replace('<h3>Kids tiffin track</h3><p>Plan a separate kids-tiffin menu alongside family meals, with repeat-alerts to beat tiffin fatigue.</p>',
                     '<h3>Kids lunchbox planner</h3><p>Plan school lunchboxes on their own track. Sofra won\'t repeat a lunchbox within the week and nudges you when one shows up three times.</p>')
    + '    <div class="card">' + ico('terra', '<rect x="3" y="6" width="18" height="14" rx="2.5"/><circle cx="12" cy="13" r="3.5"/><path d="M8 6l1.5-2h5L16 6"/>')
    + '<h3>Your own dish photos</h3><p>Snap the dish you cooked and it shows everywhere — Home, calendar, dish library. No photo yet? Every dish gets its own warm illustration.</p></div>\n'
    + '    <div class="card">' + ico('kids', '<path d="M21 12.8A8.5 8.5 0 1 1 11.2 3a6.6 6.6 0 0 0 9.8 9.8z"/>')
    + '<h3>Tomorrow, every evening</h3><p>From mid-afternoon, Home shows tomorrow\'s lunch, dinner and the kids\' lunchbox. Anything still open is one tap to fill.</p></div>\n'
    + '    <div class="card">' + ico('sage', '<path d="M4 7h11M4 12h8M4 17h11"/><path d="M17 15l2 2 3-4"/>')
    + '<h3>Plans that never repeat</h3><p>Choose "don\'t repeat a dish within 7 days" and Sofra respects it — across sides and meals you already planned. Dishes you only ever order out are never suggested.</p></div>\n'
    + '    <div class="card">' + ico('terra', '<path d="M12 3l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.4 6.8 19.1l1-5.8L3.5 9.2l5.9-.8z"/>')
    + '<h3>Restaurant memory</h3><p>Rate the dishes you order and each place gets your family\'s own score — so next time you know what to order, and what to skip.</p></div>\n'
    + '    <div class="card">' + ico('sage', '<circle cx="9" cy="8" r="3"/><path d="M3 20c1-4 3.5-6 6-6s5 2 6 6"/><path d="M17 8l1.5 1.5L21 7"/>')
    + '<h3>Family admins</h3><p>Make another parent an admin, or remove someone who no longer shares your kitchen. A family always keeps at least one admin.</p></div>\n'
)
s = s.replace(old_kids, new_cards, 1)

# Spotlight: new Home copy
s = rep(s, '<img src="assets/screens/home.png" alt="Sofra home dashboard" loading="lazy">',
        '<img src="assets/screens/home.png" alt="Sofra Home: tonight\'s dinner with a photo, tomorrow\'s plan and this month at a glance" loading="lazy">', 'index')
s = rep(s, "<h3>Your kitchen at a glance</h3>\n        <p>Open Sofra to see the month in one calm dashboard: your home-cooked ratio, outside spend against budget, unique dishes, and today's meals. No setup, no clutter — just where things stand.</p>",
        "<h3>Tonight's meal, first</h3>\n        <p>Open Sofra and see what's for dinner — with a photo of your own cooking — and who planned it. Every evening, tomorrow's plan is waiting. This month's numbers sit right below, and the Plan button knows which days are still open.</p>", 'index')
s = rep(s, "<p>Tap once and Sofra drafts the week from what your family actually cooks — balanced across cuisines, skipping recent repeats. Swap anything you like, then send the ingredients straight to your grocery list.</p>",
        "<p>Tap once and Sofra drafts the week from what your family actually cooks — no dish repeats within the days you choose, cuisines mixed, kids' lunchboxes on their own track. Swap anything you like, then send the ingredients straight to your grocery list.</p>", 'index')
# Gallery: calendar caption + new profile tile
s = rep(s, "<figcaption><strong>Your weekly calendar</strong>The whole week at a glance, past and planned, with the veg / non-veg dot on every meal.</figcaption>",
        "<figcaption><strong>Your weekly calendar</strong>The whole week at a glance, past and planned — with your dish photos and the kids' lunchbox one switch away.</figcaption>", 'index')
s = rep(s, '    <figure><img src="assets/screens/share.png"',
        '    <figure><img src="assets/screens/profile.png" alt="Profile with photo, family and meal preferences" loading="lazy"><figcaption><strong>A simple profile</strong>Your photo and details up top, your family and meal preferences below. Invite with a code, give another parent admin rights.</figcaption></figure>\n'
        '    <figure><img src="assets/screens/share.png"', 'index')

# FAQ: new questions (problem-based searches) + FAQPage structured data
new_faq = [
    ("How do I stop cooking the same meals every week?",
     "Log what you eat for a week or two and let Sofra plan. It never repeats a dish within the days you choose (7 by default), and its \"haven't made in a while\" list brings back favourites you'd forgotten."),
    ("How does Sofra plan my week?",
     "It builds the week from dishes your family has actually cooked: it skips anything eaten recently, mixes cuisines, keeps weekend dinners for eating out if you like, and never suggests dishes you only ever order from restaurants."),
    ("Can I plan my kids' school lunchboxes?",
     "Yes. Kids lunchboxes have their own track on school days. Sofra plans them from your kids' own dishes, avoids repeats within the week, and reminds you when tomorrow's lunchbox isn't planned."),
    ("Does Sofra make a grocery list from my meal plan?",
     "Yes. One tap adds the week's ingredients to a single shared grocery list. Add anything else by hand and tick items off together as you shop."),
    ("Can I add photos of my own dishes?",
     "Yes, and it's optional. Add a photo when you log a meal or from any dish, and it appears across the app. Dishes without a photo get their own illustration."),
    ("Can more than one person manage our family?",
     "Yes. Admins can make other members admins, or remove someone from the family. A family always keeps at least one admin."),
    ("Does Sofra work with large text?",
     "Yes. Sofra adapts its layout when you use your phone's larger text settings, so labels and numbers stay readable instead of getting cut off."),
]
cards = ''.join(f'    <div class="card"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></div>\n' for q, a in new_faq)
s = rep(s, '    <div class="card"><h3>Is Sofra a recipe app?</h3>',
        cards + '    <div class="card"><h3>Is Sofra a recipe app?</h3>', 'index')
faq_block = s[s.index('<section id="faq">'):]
faq_block = faq_block[:faq_block.index('</section>')]
pairs = re.findall(r'<div class="card"><h3>(.*?)</h3><p>(.*?)</p></div>', faq_block)
def clean(t): return html.unescape(re.sub(r'<[^>]+>', '', t))
ld_faq = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in pairs]}
ld_app = {"@context": "https://schema.org", "@type": "MobileApplication", "name": "Sofra",
          "operatingSystem": "Android, iOS", "applicationCategory": "LifestyleApplication",
          "description": "Family meal planner that plans your week from the meals your family already cooks.",
          "url": SITE, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
          "sameAs": [PLAY, APPLE]}
ld = ('<script type="application/ld+json">' + json.dumps(ld_app, ensure_ascii=False) + '</script>\n'
      '<script type="application/ld+json">' + json.dumps(ld_faq, ensure_ascii=False) + '</script>\n')
s = rep(s, '</head>', ld + '</head>', 'index')

FOOTER_OLD = '    <a href="security.html">Security</a> ·\n'
FOOTER_NEW = ('    <a href="meal-planner-that-remembers.html">Meal planner that remembers</a> ·\n'
              '    <a href="weekly-meal-plan-grocery-list.html">Meal plan + grocery list</a> ·\n'
              '    <a href="kids-lunchbox-planner.html">Kids lunchbox planner</a> ·\n'
              '    <a href="security.html">Security</a> ·\n')
s = rep(s, FOOTER_OLD, FOOTER_NEW, 'index')
wr('index.html', s)

# ───────────────────────── features.html ─────────────────────────
f = rd('features.html')
f = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="Everything Sofra does: tonight\'s meal first with your own photos, tomorrow\'s plan, no-repeat auto-planning, grocery list, kids lunchbox planner, restaurant memory, family admins and more.">', f, 1)
f = rep(f, 'Log a full thali — a main plus sides', 'Log a full plate — a main plus sides', 'features')
f = rep(f, '<h3>Kids tiffin track</h3><p>Plan a separate kids menu alongside family meals, generated from the kids\' own dishes.</p>',
        '<h3>Kids lunchbox planner</h3><p>Plan school lunchboxes on their own track, generated from the kids\' own dishes — no repeats within the week, and a nudge when tomorrow\'s isn\'t planned.</p>', 'features')
f = rep(f, '"Sandwich three days running" — Sofra nudges you to mix up the tiffin.', '"Sandwich three days running" — Sofra nudges you to mix up the lunchbox.', 'features')
f = re.sub(r'the kids\' tiffin split', "the kids' lunchbox split", f)
NEW_SECTION = '''<section><div class="wrap">
  <div class="sec-head"><div class="eyebrow">New in 1.2.1</div><h2>A fresh Home &amp; smarter planning</h2></div>
  <div class="grid">
    <div class="card"><h3>Tonight's meal, first</h3><p>Home opens on your next meal — by time of day — with a photo of your own cooking and who planned it.</p></div>
    <div class="card"><h3>Tomorrow, every evening</h3><p>From mid-afternoon, tomorrow's lunch, dinner and kids' lunchbox are right on Home. Gaps are one tap to fill.</p></div>
    <div class="card"><h3>Your own dish photos</h3><p>Add a photo when logging or from any dish. Dishes without one get their own illustration, chosen from the dish type.</p></div>
    <div class="card"><h3>A smart Plan button</h3><p>It knows what's left: "Plan rest of week · 3 days still open", or "Plan next week" from Friday — and opens on the right week.</p></div>
    <div class="card"><h3>Never the same dish twice</h3><p>"Don't repeat a dish within 7 days" now counts sides and meals you already planned, and dishes you only order out are never suggested.</p></div>
    <div class="card"><h3>New-family setup</h3><p>A four-step checklist gets a new family going: log today's meal in one tap, pick favourites, invite everyone.</p></div>
    <div class="card"><h3>Restaurant ratings</h3><p>Every dish you rate counts, and each restaurant gets your family's own score from those ratings.</p></div>
    <div class="card"><h3>Family admins</h3><p>Give another parent admin rights, or remove someone from the family — a family always keeps at least one admin.</p></div>
    <div class="card"><h3>Large text friendly</h3><p>Layouts adapt to your phone's larger text settings so nothing important gets cut off.</p></div>
    <div class="card"><h3>Classic view</h3><p>Prefer the original dashboard? Switch to Classic view any time in Settings (available for a limited time).</p></div>
  </div>
</div></section>

'''
first_section = f.index('<section><div class="wrap">', f.index('class="hero plain"'))
f = f[:first_section] + NEW_SECTION + f[first_section:]
f = rep(f, '    <a href="security.html">Security</a> ·\n', FOOTER_NEW, 'features') if '    <a href="security.html">Security</a> ·\n' in f else f
wr('features.html', f)

# ───────────────────────── guide.html ─────────────────────────
g = rd('guide.html')
g = rep(g, """      <p>Your kitchen at a glance, the moment you open the app.</p>
      <ul>
        <li>A warm greeting and your "meal memory" tagline up top.</li>
        <li><strong>This month</strong> metric cards — home-cooked %, outside meals (dine-out + takeout), unique dishes, outside spend, kids tiffins. Tap any card to dive in, or the share icon to post it.</li>
        <li><strong>Today's meals</strong> — lunch, dinner (and kids tiffin) with cuisine thumbnails.</li>
        <li><strong>Dishes you haven't made in a while</strong> — your forgotten favourites, resurfaced.</li>
        <li>The <strong>+</strong> button logs a meal in seconds.</li>
      </ul>""", """      <p>Your next meal first — the moment you open the app.</p>
      <ul>
        <li>A greeting, your logging streak, and who in the family added which meal.</li>
        <li><strong>Next up</strong> — lunch until mid-afternoon, then <strong>Tonight</strong> — with your own dish photo (or its illustration), sides, and a <strong>Recipe</strong> button when the dish has one.</li>
        <li><strong>Earlier today / Later today</strong>, and from 2:30 PM a compact <strong>Tomorrow</strong> card with lunch, dinner and the kids' lunchbox.</li>
        <li><strong>This month</strong> — your home-cooked %, then outside food, unique dishes, budget left and kids lunchboxes. Tap any number to dive in, or share the home-cooked badge.</li>
        <li>Shortcuts: a smart <strong>Plan</strong> button that knows which days are open, <strong>Grocery list</strong>, <strong>Dish library</strong> and <strong>Restaurants</strong>.</li>
        <li>When nothing is planned yet, <strong>Quick ideas</strong> offer recent dishes and ones you haven't made in a while.</li>
        <li>New families see a short setup checklist instead. Prefer the original dashboard? Settings → Appearance → Home screen → <strong>Classic</strong>.</li>
      </ul>""", 'guide')
g = rep(g, '<li>Toggle <strong>Show kids tiffin</strong> to add and view a separate kids track per day.</li>',
        '<li>Flip the <strong>Kids lunchbox</strong> switch to add and view the kids\' lunchbox for each school day.</li>\n        <li>Calendar always opens on this week and scrolls to today; <strong>Today</strong> appears when you move to another week.</li>', 'guide')
g = rep(g, "<li>Turn on <strong>Include kids tiffin</strong> to plan the kids' menu from their own dishes.</li>",
        "<li>Flip the <strong>Kids lunchbox</strong> switch to plan school lunchboxes from the kids' own dishes.</li>\n        <li>After generating, a short note explains how the plan was made (no repeats within your chosen days, mixed cuisines, dine-out limit) with a link to change the rules.</li>", 'guide')
g = rep(g, '<li>A dedicated <strong>kids tiffin</strong> card with variety and repeat-alerts.</li>',
        '<li>A dedicated <strong>kids lunchbox</strong> card with variety and repeat-alerts.</li>', 'guide')
g = rep(g, 'who it\'s for (family or kids tiffin). For home meals, add the main dish plus sides for a full thali.',
        'who it\'s for (family or kids lunchbox). For home meals, add the main dish plus sides, and optionally a photo of the dish.', 'guide')
g = rep(g, '<p>Your identity, household name and invite code, and family members. Settings holds',
        '<p>Your photo and details in one compact card (tap the photo to change it), then your household, invite code and family members. Admins can make others admins or remove someone. Settings holds', 'guide')
g = rep(g, 'Settings holds appearance (auto / light / dark),', 'Settings holds appearance (auto / light / dark, and Enhanced or Classic home screen),', 'guide')
wr('guide.html', g)

# ───────────────────────── new SEO pages ─────────────────────────
tpl = rd('features.html')
head_end = tpl.index('<section class="hero plain">')
foot_start = tpl.index('<footer>')
HEAD = tpl[:head_end].replace(' class="active"', '')
FOOT = tpl[foot_start:]
CTA = f'''<section><div class="wrap">
  <div class="band">
    <h2>Try Sofra free</h2>
    <p class="lead">Free, no ads, private to your family. On iPhone and Android.</p>
    <div class="badges" style="margin-top:20px">
      <a href="{APPLE}" target="_blank" rel="noopener" aria-label="Download on the App Store"><img src="assets/badge-appstore.svg" alt="Download on the App Store" height="54"></a>
      <a href="{PLAY}" target="_blank" rel="noopener" aria-label="Get it on Google Play"><img src="assets/badge-googleplay.svg" alt="Get it on Google Play" height="54"></a>
    </div>
  </div>
</div></section>

'''
def page(fname, title, desc, eyebrow, h1, lede, img, img_alt, sections, faqs):
    h = HEAD
    h = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', h, 1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc)}">', h, 1)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    h = h.replace('</head>', f'<link rel="canonical" href="{SITE}/{fname}">\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n</head>', 1)
    body = f'''<section class="hero plain"><div class="wrap">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
</div></section>

<section><div class="wrap">
  <div class="screen">
    <div class="phone"><img src="assets/screens/{img}" alt="{html.escape(img_alt)}" loading="lazy"></div>
    <div class="body">
''' + ''.join(f'      <h2>{t}</h2>\n      <p>{p}</p>\n' for t, p in sections) + '''    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><div class="eyebrow">FAQ</div><h2>Common questions</h2></div>
  <div class="grid">
''' + ''.join(f'    <div class="card"><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></div>\n' for q, a in faqs) + '''  </div>
</div></section>

'''
    wr(fname, h + body + CTA + FOOT)

page('meal-planner-that-remembers.html',
     'A meal planner that remembers what your family cooks — Sofra',
     'Stop searching for recipes. Sofra plans your week from the meals your family already loves, never repeats a dish too soon, and brings back forgotten favourites.',
     'Meal planner', 'The meal planner that remembers what your family cooks',
     'Most meal planners push new recipes. Sofra does the opposite: it remembers what your family actually eats and plans the week from that.',
     'home.png', 'Sofra Home showing tonight\'s dinner and tomorrow\'s plan',
     [('Plan from your own history', 'Log meals in about ten seconds. After a week or two, one tap builds next week from dishes your family already loves — balanced across cuisines.'),
      ('No more "what should we cook?"', 'Home shows tonight\'s meal first, and every evening tomorrow\'s plan is ready. Anything still open is one tap to fill — or let Sofra decide.'),
      ('Never the same dinner twice in a row', 'Choose how long before a dish can come back (7 days by default). Sofra respects it across sides and already-planned meals.'),
      ('Bring back forgotten favourites', '"Haven\'t made in a while" surfaces dishes your family loved but stopped cooking.')],
     [('How do I stop cooking the same meals every week?', 'Let Sofra plan from your history: it never repeats a dish within the days you choose and resurfaces dishes you haven\'t made in a while.'),
      ('How do I plan meals my family will actually eat?', 'Plan from what they already eat. Sofra builds the week only from dishes your family has cooked, not from unfamiliar recipes.'),
      ('How does Sofra pick dishes?', 'It favours dishes you haven\'t had recently and your favourites, mixes cuisines, and skips anything you only ever order from restaurants.'),
      ('Is Sofra free?', 'Yes. Sofra is free, with no ads, on iPhone and Android.')])

page('weekly-meal-plan-grocery-list.html',
     'Weekly meal plan and grocery list in one — Sofra',
     'Plan a week of family meals and turn it into a shared grocery list in one tap. Free family meal planner for iPhone and Android.',
     'Meal plan + grocery list', 'Plan the week and the grocery list together',
     'Sofra drafts a week of meals from your family\'s own dishes, then adds every ingredient to one shared list.',
     'plan.png', 'A week planned in Sofra',
     [('A week in one tap', 'Generate a week of lunches and dinners from dishes your family cooks. Swap anything you like, then accept it to your calendar.'),
      ('Ingredients straight to your list', 'Each dish keeps its own ingredients. One tap adds the whole week to a single shared grocery list.'),
      ('Shop together', 'Everyone in the family sees the same list. Add extras by hand and tick items off as you go.'),
      ('Knows what\'s left to plan', 'The Plan button tells you how many days are still open this week, and from Friday it moves on to next week.')],
     [('How do I make a grocery list from a meal plan?', 'In Sofra, plan the week, then tap "Add week\'s ingredients to grocery". Every planned dish\'s ingredients land on one shared list.'),
      ('How do I plan a week of family dinners?', 'Log what you cook for a week or two, then let Sofra generate the week from those dishes, with no repeats and mixed cuisines.'),
      ('Can my family share the grocery list?', 'Yes. Everyone in your family sees and updates the same list in real time.'),
      ('Can I plan only dinners?', 'Yes. Choose which meals you plan — breakfast, lunch, dinner or snack — in your meal preferences.')])

page('kids-lunchbox-planner.html',
     'Kids lunchbox planner for school days — Sofra',
     'Plan school lunchboxes without repeats. Sofra keeps a kids lunchbox track alongside family meals and reminds you when tomorrow\'s isn\'t planned.',
     'Kids lunchbox planner', 'Plan school lunchboxes without repeats',
     'Kids lunchboxes get their own track in Sofra, planned from your kids\' own favourites on school days.',
     'calendar.png', 'Sofra calendar with the kids lunchbox switched on',
     [('Their own track', 'Flip the Kids lunchbox switch and every school day gets a lunchbox slot, separate from family meals.'),
      ('No repeats within the week', 'Auto-plan picks from dishes your kids have had before and avoids repeating one within the week.'),
      ('A nudge when it\'s missing', 'Home reminds you when tomorrow\'s lunchbox isn\'t planned, and flags a lunchbox packed three times in a week.'),
      ('Favourites that stick', 'Star your kids\' favourite lunchboxes and Sofra suggests them more often.')],
     [('How do I plan school lunches for the week?', 'Turn on the Kids lunchbox switch in Plan and generate the week. Sofra fills school days from your kids\' own dishes.'),
      ('How do I avoid packing the same lunch every day?', 'Sofra won\'t repeat a lunchbox within the week when you have enough dishes, and warns you when one comes up three times.'),
      ('Does it plan lunchboxes on weekends?', 'No. Lunchboxes are planned on school days only; you can still add one for any day by hand.'),
      ('Is Sofra only for Indian tiffins?', 'No. Pack any food from any cuisine — sandwiches, wraps, pasta, rice, anything your kids enjoy.')])

# ───────────────────────── sitemap + robots ─────────────────────────
pages = ['', 'features.html', 'guide.html', 'meal-planner-that-remembers.html', 'weekly-meal-plan-grocery-list.html',
         'kids-lunchbox-planner.html', 'privacy.html', 'terms.html', 'security.html']
wr('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
   + ''.join(f'  <url><loc>{SITE}/{p}</loc></url>\n' for p in pages) + '</urlset>\n')
wr('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
print('site updated')
