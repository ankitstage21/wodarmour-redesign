"""
Content for the Normatec landing page.

  SOURCED     = taken from the live store / merchant checkout. Safe.
  PLACEHOLDER = invented for layout. MUST be replaced before launch.
"""

# ── SOURCED ─────────────────────────────────────────────────────────
EMI_FROM  = "₹16,663"     # x6 = ₹99,978 — a 6-month no-cost plan on this price
EMI_BANKS = 20            # 3 shown + "+17", per the merchant's Razorpay widget

RATING, NREV = "4.6", 178
HIST = [(5, 139), (4, 21), (3, 10), (2, 2), (1, 6)]

# prices SOURCED from the live store; feature deltas PLACEHOLDER
COMPARE = [
  ("Normatec 3<br>Legs", "₹99,980", True,
   ["Wired to control unit", "5 zones per leg", "7 levels · 30–110 mmHg", "3+ hrs", "Yes", "1.54 kg unit"]),
  ("Normatec<br>Elite", "₹1,28,990", False,
   ["Fully wireless", "5 zones per leg", "7 levels · 30–110 mmHg", "2.5 hrs", "Yes", "No hose at all"]),
  ("Normatec<br>Go", "₹49,990", False,
   ["Wireless, calves only", "2 zones per calf", "7 levels", "2.5 hrs", "No", "Fits in a kit bag"]),
  ("Therabody<br>JetBoots Prime", "₹54,999", False,
   ["Wireless", "4 zones per leg", "4 levels", "3 hrs", "No", "Different app ecosystem"]),
]
COMPARE_ROWS = ["Connection", "Zones", "Pressure", "Battery", "ZoneBoost", "Notes"]

# ── PLACEHOLDER ─────────────────────────────────────────────────────
BOX = [
  ("1", "Normatec 3 control unit", "The pump and touchscreen. Runs the whole system."),
  ("2", "Leg attachments (pair)", "Full-length sleeves, foot to upper thigh."),
  ("2", "Connector hoses", "Control unit to each sleeve."),
  ("1", "Power adapter", "Indian 3-pin plug, fitted for 230V."),
  ("1", "Carry bag", "Holds the unit, sleeves and hoses together."),
  ("1", "Quick-start guide", "Plus the warranty card and the Hyperice app QR code."),
]

FIT = [
  ("Standard", "Up to 5&#39;11&quot;", "Fits most adults. This is the size shipped by default and the one held in stock."),
  ("Tall", "5&#39;11&quot; – 6&#39;6&quot;", "Longer sleeve for taller users. Ask before ordering — lead time differs."),
  ("Thigh", "Up to 33&quot; around", "The sleeve opens completely flat, so larger thighs are usually fine."),
]

REVIEWS = [
  (5, "Bought it after my second marathon block. Twenty minutes after a long run and my legs feel like they belong to me again. The app control matters more than I expected — I never have to get up to change the setting.",
      "Rohan M.", "Bengaluru · Marathon"),
  (5, "I run a small physio practice and we use it between patients. Built well enough to take that kind of use. WOD Armour handled the GST invoice properly, which mattered for the clinic accounts.",
      "Dr. Anjali S.", "Pune · Physiotherapist"),
  (4, "Works exactly as advertised. Only thing — the hose does mean you are tethered to the unit. Not a dealbreaker at this price, but worth knowing before you buy.",
      "Karthik R.", "Chennai · Cyclist"),
]

CARE_GOOD = [
  "Two-year warranty covering the control unit and both leg attachments.",
  "Service handled in India — the unit never has to be shipped abroad.",
  "Seven-day return window if unused and in original packaging.",
  "Replacement sleeves sold separately if one is damaged out of warranty.",
]

CARE_WARN = [
  "Do not use if you have, or suspect you have, deep vein thrombosis.",
  "Not suitable over open wounds, fresh fractures or recent surgical sites.",
  "Speak to a doctor first if you have severe peripheral arterial disease, heart failure, or are pregnant.",
  "Stop and consult a clinician if a session causes numbness, tingling or pain.",
]

FAQ = [
  ("Is no-cost EMI actually available?",
   "Yes — no-cost EMI starts at ₹16,663/month, and Pay Later is available at 0% interest. Card options from 20 banks are shown at checkout."),
  ("What does ZoneBoost actually do?",
   "It raises compression in one chosen zone — usually the calves or thighs — instead of treating the whole leg identically. Useful when one area is doing the complaining."),
  ("How long should a session be?",
   "Most people run 20–45 minutes. If you have never used compression before, start shorter and build up rather than going straight to the top setting."),
  ("Will it fit me if I'm tall?",
   "The standard sleeve fits up to about 5'11\". There is a tall version for anyone above that — message us before ordering, because the lead time is different."),
  ("What if it doesn't suit me?",
   "There is a seven-day return window provided the unit is unused and in its original packaging. Talk to us first — most of the time it's a settings problem, not a fit problem."),
  ("How is this different from cheaper compression boots?",
   "Pressure accuracy and the sequence. Budget units inflate zones roughly and often all at once. Normatec's patented pulse holds each zone while the next engages, which is what keeps fluid moving one direction."),
  ("Normatec 3 or the Elite?",
   "The Elite is fully wireless and costs ₹29,010 more. The 3 is tethered to the control unit by a hose. If you recover in one spot, the 3 is the better value; if the hose would annoy you, pay for the Elite."),
]
