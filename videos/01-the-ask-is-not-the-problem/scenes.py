"""
Scenes for the Module 1 video: "The ask is not the problem".

Each scene is a list of beats. A beat is (html, caption, seconds). Beats in a scene
cross-fade into each other, so a "build" is just the same layout with one more
element visible. Captions are the narration; SCRIPT.md has the same words for
anyone who wants to record a voice-over.
"""

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1280px; height: 720px; overflow: hidden; }
body { font-family: Inter, sans-serif; background: #f6f1e9; color: #0f2e33; position: relative; }
.stage { position: absolute; inset: 0 0 120px 0; display: flex; flex-direction: column;
         align-items: center; justify-content: center; padding: 40px 80px; }
.kicker { font-size: 20px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: #e8833a; margin-bottom: 14px; }
h1 { font-family: 'Inter Display', Inter, sans-serif; font-size: 64px; font-weight: 800; line-height: 1.05; text-align: center; color: #0f5257; }
h2 { font-family: 'Inter Display', Inter, sans-serif; font-size: 44px; font-weight: 800; line-height: 1.1; text-align: center; color: #0f5257; margin-bottom: 28px; }
.sub { font-size: 24px; color: #4a5f62; margin-top: 18px; text-align: center; }
.caption { position: absolute; left: 0; right: 0; bottom: 0; height: 120px; background: #0f2e33;
           color: #fff; font-size: 27px; line-height: 1.35; display: flex; align-items: center;
           justify-content: center; text-align: center; padding: 0 110px; font-weight: 500; }
.card { background: #fff; border-radius: 18px; box-shadow: 0 1px 0 rgba(15,46,51,.08); border: 1px solid #e3dccf;
        padding: 26px 32px; font-size: 24px; line-height: 1.5; width: 920px; }
.card .head { font-size: 17px; color: #6b7c7e; margin-bottom: 12px; }
.mark { background: rgba(232,131,58,.22); padding: 0 6px; border-radius: 6px; font-weight: 700; }
.hide { visibility: hidden; }
.row { display: flex; gap: 22px; align-items: stretch; }
.box { background: #fff; border: 1px solid #e3dccf; border-radius: 16px; padding: 22px 24px; width: 330px; }
.box b { display: block; font-size: 26px; margin-bottom: 8px; color: #0f5257; }
.box span { font-size: 20px; color: #4a5f62; line-height: 1.4; }
.ladder { display: flex; flex-direction: column; gap: 12px; align-items: center; }
.rung { background: #fff; border: 1px solid #e3dccf; border-radius: 14px; padding: 14px 26px; font-size: 25px; min-width: 640px; text-align: center; }
.rung.hot { background: #0f5257; color: #fff; border-color: #0f5257; font-weight: 700; }
.arrow { font-size: 24px; color: #e8833a; line-height: 1; font-weight: 700; }
.why { font-size: 17px; color: #e8833a; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.steps { display: flex; flex-direction: column; gap: 12px; width: 900px; }
.step { display: flex; align-items: center; gap: 20px; background: #fff; border: 1px solid #e3dccf; border-radius: 14px; padding: 14px 22px; font-size: 25px; }
.step .n { flex: 0 0 46px; height: 46px; border-radius: 50%; background: #0f5257; color: #fff; display: grid; place-items: center; font-weight: 800; }
.step.warn { border: 2px solid #e8833a; }
.big { font-family: 'Inter Display', Inter, sans-serif; font-size: 110px; font-weight: 800; color: #0f5257; line-height: 1; }
.big.q { color: #e8833a; }
.stat { background: #fff; border: 1px solid #e3dccf; border-radius: 18px; padding: 30px 34px; width: 470px; text-align: center; }
.stat .label { font-size: 22px; color: #4a5f62; margin-top: 12px; line-height: 1.35; }
.grid2 { position: relative; width: 760px; height: 400px; border-left: 3px solid #0f2e33; border-bottom: 3px solid #0f2e33; }
.grid2 .ax { position: absolute; font-size: 18px; color: #4a5f62; font-weight: 600; }
.grid2 .mid-v { position: absolute; left: 50%; top: 0; bottom: 0; border-left: 2px dashed #cfc6b6; }
.grid2 .mid-h { position: absolute; top: 50%; left: 0; right: 0; border-top: 2px dashed #cfc6b6; }
.dot { position: absolute; display: flex; align-items: center; gap: 10px; font-size: 21px; font-weight: 700; }
.dot i { flex: 0 0 46px; width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; color: #fff; font-style: normal; font-size: 16px; }
.logo { width: 120px; height: 120px; margin-bottom: 28px; }
.prompt { font-family: 'DejaVu Sans Mono', monospace; background: #0f2e33; color: #f6f1e9; border-radius: 14px; padding: 18px 26px; font-size: 26px; margin-top: 26px; }
"""

LOGO = """<svg class="logo" viewBox="0 0 48 48"><rect x="2" y="2" width="44" height="44" rx="11" fill="#0f5257"/>
<circle cx="24" cy="24" r="12.5" fill="none" stroke="#f6f1e9" stroke-width="3"/><circle cx="24" cy="24" r="4" fill="#e8833a"/>
<path d="M24 5.5v7M24 35.5v7M5.5 24h7M35.5 24h7" stroke="#f6f1e9" stroke-width="3" stroke-linecap="round"/></svg>"""


def vis(show):
    return "" if show else " hide"


def title():
    return [(f'<div class="stage">{LOGO}<div class="kicker">FDE Field Program · Mission 1</div>'
             f'<h1>The chatbot that wasn\'t</h1><div class="sub">Discovery and decomposition</div></div>',
             "Mission 1. Before you build anything, find out what's really going on.", 5.5)]


def email():
    def html(hl):
        a = ' class="mark"' if hl else ""
        return (f'<div class="stage"><div class="kicker">Monday, 7:52 am</div><div class="card">'
                f'<div class="head">From: Dana Okafor, VP Operations · Ridgeway Medical Supply</div>'
                f'Our support team is drowning in "where\'s my order?" calls. What I\'m picturing is '
                f'<span{a}>an AI chatbot on our customer portal</span> that answers order-status questions 24/7.'
                f'<br><br>Operationally we\'re in decent shape. <span{a}>We ship about 94% of orders on time.</span>'
                f'<br><br>We have $180K approved.</div></div>')
    return [(html(False), "Meet Dana, VP of Operations at Ridgeway Medical Supply. Your new client.", 5.5),
            (html(True), "She knows what she wants: an AI chatbot. And she says 94% of orders are on time.", 6.5)]


def slack():
    return [(f'<div class="stage"><div class="kicker">Ten minutes later · Slack</div><div class="card">'
             f'<div class="head">Renee Alvarez · Customer Support Lead</div>'
             f'a chatbot isn\'t going to fix this. people don\'t call because they can\'t find tracking. '
             f'<span class="mark">they call because the order is LATE and nobody told them.</span></div></div>',
             "Then Renee, who runs support, messages you. She says customers are furious about late orders.", 7)]


def whos_right():
    return [('<div class="stage"><h1>Who\'s right?</h1><div class="sub">94% on time… and furious customers.</div></div>',
             "Both can't be fully right. Your first job is to find out which, before writing a single line of code.", 6.5)]


def ladder():
    rungs = ["Build an AI chatbot", "Fewer \"where's my order?\" calls", "Orders are late, and nobody tells customers",
             "Credits paid to hospitals, and hospitals that leave"]
    caps = ["Lesson one: the ask is not the problem. A chatbot is a solution Dana imagined.",
            "Ask: if this worked perfectly, what would be different? Fewer calls.",
            "Why do customers call? Because orders are late, and nobody warned them.",
            "And what does that cost? Money, and hospitals walking away. That's the real problem."]
    beats = []
    for k in range(1, 5):
        parts = []
        for i, r in enumerate(rungs):
            show = i < k
            hot = " hot" if i == 3 and show else ""
            if i:
                parts.append(f'<div class="arrow{vis(show)}">↓ <span class="why">what would be different?</span></div>' if i == 1
                             else f'<div class="arrow{vis(show)}">↓ <span class="why">why?</span></div>' if i == 2
                             else f'<div class="arrow{vis(show)}">↓ <span class="why">what does it cost?</span></div>')
            parts.append(f'<div class="rung{hot}{vis(show)}">{r}</div>')
        beats.append((f'<div class="stage"><h2>The ask is not the problem</h2><div class="ladder">{"".join(parts)}</div></div>',
                      caps[k - 1], 6.5 if k < 4 else 7.5))
    return beats


def hats():
    boxes = [("Engineer", "Can we build it, with this data, in this environment?"),
             ("Consultant", "Is this the right problem? Who has to say yes?"),
             ("Product scout", "What here should become part of our product?")]
    caps = ["An FDE wears three hats. The engineer asks: can we actually build this, here?",
            "The consultant asks: is this the right problem, and who has to say yes?",
            "And the product scout asks: what should we take back to our own product?"]
    beats = []
    for k in range(1, 4):
        cells = "".join(f'<div class="box{vis(i < k)}"><b>{t}</b><span>{d}</span></div>' for i, (t, d) in enumerate(boxes))
        beats.append((f'<div class="stage"><h2>Wear three hats</h2><div class="row">{cells}</div></div>', caps[k - 1], 6))
    return beats


def people():
    # (initials, colour, name, top %, left %): top = high power, right = high interest
    dots = [("DO", "#0f5257", "Dana", 6, 62), ("GT", "#5b6c8f", "Greg", 14, 12), ("LM", "#8a5a83", "Linda", 32, 30),
            ("RA", "#e8833a", "Renee", 68, 70)]
    def html(show_hector):
        d = "".join(f'<div class="dot" style="top:{t}%;left:{l}%"><i style="background:{c}">{ini}</i>{n}</div>'
                    for ini, c, n, t, l in dots)
        h = (f'<div class="dot{vis(show_hector)}" style="top:44%;left:103%"><i style="background:#6f7d3c">?</i>'
             f'<span>Boise manager<br><span style="font-weight:500;font-size:17px;color:#e8833a">not invited</span></span></div>')
        return (f'<div class="stage"><h2>Map the people</h2><div class="grid2" style="width:700px;transform:translateX(-110px)">'
                f'<div class="mid-v"></div><div class="mid-h"></div>'
                f'<div class="ax" style="left:-10px;top:-30px">&#8593; power: can stop or fund it</div>'
                f'<div class="ax" style="right:0;bottom:-34px">interest: changes their day &#8594;</div>{d}{h}</div></div>')
    return [(html(False), "Next, map the people. Who can fund or stop this? Whose day does it change?", 6.5),
            (html(True), "And notice who's missing. Boise has been rough since summer, and nobody invited its manager.", 7)]


def two_numbers():
    def html(show_q, show_twin):
        twin = (f'<div class="sub{vis(show_twin)}" style="margin-top:30px">Real-world twin: USAID\'s medicine shipments have the same trap. '
                f'<b style="color:#e8833a">Find it.</b></div>')
        return (f'<div class="stage"><h2>Same company. Two "on-time" numbers.</h2><div class="row">'
                f'<div class="stat"><div class="big">94%</div><div class="label">shipped within 1 day<br>of the order</div></div>'
                f'<div class="stat{vis(show_q)}"><div class="big q">??%</div><div class="label">delivered by the date<br>we promised</div></div>'
                f'</div>{twin}</div>')
    return [(html(False, False), "Now the trap. Dana's 94% measures when orders leave the warehouse.", 6),
            (html(True, False), "Customers feel when orders arrive. That number lives in the carrier data, and you'll calculate it.", 7.5),
            (html(True, True), "Always ask how a number is calculated. Real data has the same trap; you'll find it in the lab.", 7)]


def decompose():
    steps = ["Clarify the goal", "Stakeholders and metrics", "Inputs: data, owners, mess", "Subproblems, riskiest first",
             "Walking skeleton: value in days"]
    caps = ["Then decompose. Step one: clarify the goal, and what success looks like.",
            "Two: who wins, who loses, who decides, and how it's measured today.",
            "Three: the inputs. What data exists, who owns it, and how messy it is.",
            "Four: break it into pieces, and tackle the riskiest assumption first.",
            "Five: the walking skeleton. The thinnest version that proves value in days.",
            "The classic mistake, in interviews and on the job: jumping to step five first."]
    beats = []
    for k in range(1, 7):
        rows = "".join(f'<div class="step{" warn" if k == 6 and i == 4 else ""}{vis(i < k)}"><div class="n">{i + 1}</div>{s}</div>'
                       for i, s in enumerate(steps))
        beats.append((f'<div class="stage"><h2>Decompose before you solve</h2><div class="steps">{rows}</div></div>',
                      caps[k - 1], 6 if k < 6 else 6.5))
    return beats


def mission():
    items = ["Check Dana's numbers against the data", "Run the kickoff call with Dana (role-play)",
             "Write a short scope she'll sign", "Two timed decomposition drills"]
    rows = "".join(f'<div class="step"><div class="n">{i + 1}</div>{s}</div>' for i, s in enumerate(items))
    return [(f'<div class="stage"><div class="kicker">Your mission</div><div class="steps" style="width:820px">{rows}</div>'
             f'<div class="prompt">&gt; Teach me Module 1</div></div>',
             "Your mission: check the numbers, interview Dana, and write a scope she'll sign. Your AI tutor is ready.", 8)]


def end():
    return [(f'<div class="stage">{LOGO}<h1>Ask before you build.</h1><div class="sub">FDE Field Program · open source · '
             f'Ridgeway Medical Supply is fictional</div></div>', "See you on the kickoff call.", 4.5)]


SCENES = [title(), email(), slack(), whos_right(), ladder(), hats(), people(), two_numbers(), decompose(), mission(), end()]
