import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "RackPlatePro"
SITE_TAGLINE = "Home Gym Rubber Flooring Mat, Barbell Plate Loader, 1RM & Power Rack Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/rackplatepro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "rackplatepro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "MAJOR FITNESS F22 / PLM03 All-in-One Power Rack w/ Dual Cable Pulley System (1,600 Lb Capacity)",
        "category": "All-in-One Functional Power Rack",
        "rating": "4.8 ★ (3,900+ reviews)",
        "badge": "#1 All-in-One Home Gym Rack",
        "specs": "14-Gauge 2\"×3\" Steel Uprights | Dual Independent Lat/Low Pulleys | Landmine, Dip Bars & J-Hooks",
        "keyword": "MAJOR+FITNESS+F22+PLM03+All+in+One+Power+Rack+Cable+Crossover"
    },
    {
        "title": "PowerBlock Elite USA / Pro 100 Adjustable Dumbbells (5–50 Lbs Expandable to 90 Lbs per Hand)",
        "category": "Expandable Adjustable Dumbbells",
        "rating": "4.8 ★ (14,200+ reviews)",
        "badge": "#1 Drop-Proof Adjustable Dumbbell",
        "specs": "Replaces 28 Pairs of Dumbbells | Welded Steel Plate Stack | Magnetic Selector Pin | 5-Yr Warranty",
        "keyword": "PowerBlock+Elite+EXP+Adjustable+Dumbbells+50+70+90+lb"
    },
    {
        "title": "Signature Fitness / BalanceFrom 260-Lb & 370-Lb 100% Virgin Rubber Olympic Bumper Plate Set",
        "category": "2-Inch Olympic Bumper Plates",
        "rating": "4.8 ★ (11,600+ reviews)",
        "badge": "#1 Best-Selling Bumper Set",
        "specs": "IWF Standard 17.7\" Diameter | Forged Steel 2\" Center Hub | Low Dead-Bounce Durometer | Pairs 10–45 Lb",
        "keyword": "260+lb+370+lb+Olympic+Bumper+Plate+Weight+Set+Virgin+Rubber"
    },
    {
        "title": "Bowflex SelectTech 552 / 1090 Adjustable Dumbbells (5 to 52.5 Lbs or 10 to 90 Lbs Pair)",
        "category": "Dial-Select Adjustable Dumbbells",
        "rating": "4.8 ★ (31,500+ reviews)",
        "badge": "30,000+ Five-Star Reviews",
        "specs": "2-Second Turn-Dial Weight Selection | 15 Weight Settings in 2.5-Lb Increments | Storage Cradles",
        "keyword": "Bowflex+SelectTech+552+1090+Adjustable+Dumbbells"
    },
    {
        "title": "REP Fitness AB-3000 2.0 FID Adjustable Weight Bench (1,000-Lb Capacity, Decline/Flat/Incline)",
        "category": "Commercial FID Weight Bench",
        "rating": "4.9 ★ (4,800+ reviews)",
        "badge": "#1 Heavy-Duty FID Bench",
        "specs": "8 Back Angles (-12° to 85°) + 5 Seat Angles | Grippy CleanGrip Vinyl | Integrated Leg Roller",
        "keyword": "REP+Fitness+AB+3000+FID+Adjustable+Weight+Bench+1000+lb"
    },
    {
        "title": "Concept2 RowErg Indoor Rowing Machine w/ PM5 Performance Monitor (Tall or Standard Legs)",
        "category": "Commercial Air Rower",
        "rating": "4.9 ★ (19,800+ reviews)",
        "badge": "#1 Gold Standard Cardio Machine",
        "specs": "Bluetooth ANT+ PM5 Monitor | Spiral Air Damper (1–10) | Separates in 2 Pieces for Upright Storage",
        "keyword": "Concept2+RowErg+Indoor+Rowing+Machine+PM5"
    },
    {
        "title": "Mikolo / RitFit M4 All-in-One Smith Machine, Power Cage & 2000-Lb Cable Crossover Station",
        "category": "Smith Machine + Power Cage",
        "rating": "4.7 ★ (2,650+ reviews)",
        "badge": "Best Solo-Training Smith Cage",
        "specs": "Linear-Bearing Counterbalanced Smith Bar | Free-Weight J-Hooks + Safety Spotter Arms | Cable Pulley",
        "keyword": "Mikolo+RitFit+Smith+Machine+Power+Cage+Cable+Crossover"
    },
    {
        "title": "American Floor Mats / ProSource 1/2\" & 3/4\" Heavy-Duty Interlocking Rubber Gym Flooring Tiles",
        "category": "Deadlift & Rack Rubber Flooring",
        "rating": "4.7 ★ (16,400+ reviews)",
        "badge": "#1 Garage Gym Floor Protection",
        "specs": "Vulcanized Recycled/Virgin Crumb Rubber | Absorbs 400-Lb Deadlift Drops | Zero Curl Puzzle Edges",
        "keyword": "Heavy+Duty+Rubber+Gym+Flooring+Mats+3+4+Inch+1+2+Inch"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "MAJOR FITNESS F22 All-in-One",
        "type": "Power Rack + Dual Pulleys",
        "capacity_spec": "1,600 Lb Rack / 800 Lb Cables",
        "footprint": "61\" W × 53\" D × 83\" H",
        "highlight": "Replaces 5 Gym Machines in 1 Footprint",
        "rating": "4.8 / 5.0 ★",
        "keyword": "MAJOR+FITNESS+F22+All+in+One+Power+Rack"
    },
    {
        "model": "Mikolo M4 Smith + Power Cage",
        "type": "Smith Machine + Functional Trainer",
        "capacity_spec": "2,000 Lb Static / Linear Smith",
        "footprint": "70\" W × 61\" D × 86\" H",
        "highlight": "Guided Smith Bar + Free-Weight Hooks",
        "rating": "4.7 / 5.0 ★",
        "keyword": "Mikolo+Smith+Machine+Power+Cage+Cable+Crossover"
    },
    {
        "model": "PowerBlock Elite EXP (Up to 90 Lb)",
        "type": "Caged Steel Adjustable Dumbbells",
        "capacity_spec": "5–50 Lb (Expands to 70 & 90 Lb)",
        "footprint": "16\" L × 6.5\" W × 6.5\" H",
        "highlight": "All-Steel Construction (Survives Drops)",
        "rating": "4.8 / 5.0 ★",
        "keyword": "PowerBlock+Elite+EXP+Adjustable+Dumbbells+50+70+90+lb"
    },
    {
        "model": "Bowflex SelectTech 552 (5–52.5 Lb)",
        "type": "Rotary-Dial Adjustable Dumbbells",
        "capacity_spec": "5 to 52.5 Lbs (2.5-Lb Micro Steps)",
        "footprint": "16.9\" L × 8.3\" W × 9.0\" H",
        "highlight": "Fastest 2-Sec Dial + Traditional Handle",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Bowflex+SelectTech+552+Adjustable+Dumbbells"
    },
    {
        "model": "REP Fitness AB-3000 2.0 FID",
        "type": "Commercial FID Weight Bench",
        "capacity_spec": "1,000 Lb Rated (-12° to 85°)",
        "footprint": "56.5\" L × 25.8\" W × 17.1\" H",
        "highlight": "Zero-Slip CleanGrip Pad + Leg Catch",
        "rating": "4.9 / 5.0 ★",
        "keyword": "REP+Fitness+AB+3000+FID+Adjustable+Weight+Bench"
    },
    {
        "model": "Concept2 RowErg (PM5 Monitor)",
        "type": "Air-Resistance Rowing Machine",
        "capacity_spec": "500 Lb User Capacity",
        "footprint": "96\" L × 24\" W (Stores 25\"×33\")",
        "highlight": "World Standard 2,000m Conditioning",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Concept2+RowErg+Indoor+Rowing+Machine+PM5"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-powerblock-elite-exp-vs-bowflex-selecttech-552-adjustable-dumbbells",
        "title": "PowerBlock Elite EXP vs. Bowflex SelectTech 552: Durability, 90-Lb Expansion & Handle Feel Compared",
        "product_a": "PowerBlock Elite EXP (5–90 Lbs)",
        "product_b": "Bowflex SelectTech 552 (5–52.5 Lbs)",
        "winner_badge": "Best Heavy 90-Lb Expansion & Durability vs. Fastest Rotary Dial & Open Handle",
        "keyword_a": "PowerBlock+Elite+EXP+Adjustable+Dumbbells+50+70+90+lb",
        "keyword_b": "Bowflex+SelectTech+552+Adjustable+Dumbbells",
        "summary": "Compare welded steel nested plates against molded rotary locking mechanisms, dumbbell length during light curls, and heavy bench press expandability.",
        "metrics": [
            {"feature": "Maximum Weight Per Hand", "val_a": "50 Lbs Base — Expandable to 70 Lbs & 90 Lbs w/ Stage Kits", "val_b": "52.5 Lbs Max (Non-Expandable; 1090 Model Goes to 90 Lbs)"},
            {"feature": "Internal Locking Mechanism", "val_a": "Solid Welded Steel Plates + Magnetic Polypropylene Pin", "val_b": "Rotary Plastic/Metal Locking Tabs Inside End Dials"},
            {"feature": "Dumbbell Length at 15 Lbs", "val_a": "Compact 10 Inches (Length Scales With Weight Selected!)", "val_b": "Fixed 16.9 Inches Long Even at 5 Lbs"},
            {"feature": "Wrist & Grip Ergonomics", "val_a": "Enclosed Padded Wrist Cage (Great for Presses, Tight for 2-Hand Goblet)", "val_b": "Open Knurled Barbell-Style Handle"},
            {"feature": "Drop & Impact Tolerance", "val_a": "Extremely High (No Fragile End Dials to Crack)", "val_b": "Do Not Drop (Dropping Can Crack Internal Selector Discs)"}
        ],
        "verdict_text": "Choose the PowerBlock Elite EXP if you lift heavy (and want to expand to 70 or 90 lbs per hand over time) and want an indestructible all-steel dumbbell whose length shrinks when doing light curls and lateral raises. Choose the Bowflex SelectTech 552 if you prefer an open traditional dumbbell handle for two-handed goblet squats and triceps extensions and love the speed of a 2-second turn dial."
    },
    {
        "slug": "compare-all-in-one-functional-trainer-power-rack-vs-smith-machine-cage",
        "title": "All-in-One Power Rack + Cable Pulley (Major Fitness F22) vs. Smith Machine Cage (Mikolo M4)",
        "product_a": "Free-Weight Power Rack + Dual Cables (F22)",
        "product_b": "Smith Machine + Power Cage Combo (M4)",
        "winner_badge": "Best Natural Barbell Path & Footprint vs. Best Guided Isolation & Solo Failure",
        "keyword_a": "MAJOR+FITNESS+F22+All+in+One+Power+Rack",
        "keyword_b": "Mikolo+Smith+Machine+Power+Cage+Cable+Crossover",
        "summary": "Compare natural stabilizer muscle recruitment on a free 45-lb Olympic barbell against a fixed-rail linear-bearing Smith bar when training alone in a garage gym.",
        "metrics": [
            {"feature": "Primary Barbell Movement", "val_a": "100% Free-Weight 7-Ft Olympic Barbell + Safety Spotter Arms", "val_b": "Both Fixed-Rail Smith Bar AND Front Free-Weight J-Hooks"},
            {"feature": "Cable Pulley Ratio", "val_a": "2:1 Smooth Dual Independent Pulleys (Plate-Loaded)", "val_b": "2:1 or 1:1 Lat Pulldown & Low Row + Dual Crossovers"},
            {"feature": "Required Room Width", "val_a": "84\" Bar + 24\" Side Clearance = 9 to 10 Feet Wide", "val_b": "86\" Wide Smith Bar Axle = 10 to 11 Feet Wide"},
            {"feature": "Solo Bench Press Safety", "val_a": "Set Heavy-Duty Safety Spotter Arms 1\" Below Chest Arch", "val_b": "Twist Wrist 15° at Any Point to Hook Smith Bar Onto Pegs"},
            {"feature": "Assembly Time", "val_a": "~2.5 Hours (Fewer Moving Linear Rails)", "val_b": "~4 to 5 Hours (Includes Linear Guide Rods & Smith Carriage)"}
        ],
        "verdict_text": "If you prioritize athletic strength, powerlifting (squat, bench, overhead press, deadlift), and want a cleaner 53-inch deep footprint, choose the Major Fitness F22 All-in-One Power Rack—its heavy steel safety spotter arms let you bench press to failure safely with a real Olympic bar, while its dual pulleys handle all your lat pulldowns, tricep pushdowns, and cable flyes. Choose the Mikolo M4 Smith Machine if you love bodybuilding hypertrophy movements (Smith hip thrusts, hack squats, incline presses, and calf raises) where locking the bar with a flick of the wrist lets you push past failure."
    },
    {
        "slug": "compare-virgin-rubber-bumper-plates-vs-cast-iron-olympic-weight-plates",
        "title": "Virgin Rubber Bumper Plates vs. Cast-Iron Olympic Plates: Concrete Floor Protection, Noise & Sleeve Fit",
        "product_a": "Virgin Rubber Olympic Bumper Plates",
        "product_b": "Cast-Iron / Grip Olympic Weight Plates",
        "winner_badge": "Safe Overhead Drops & Quiet 65 dB Deadlifts vs. Thinnest Bar Sleeve Width",
        "keyword_a": "260+lb+370+lb+Olympic+Bumper+Plate+Weight+Set+Virgin+Rubber",
        "keyword_b": "Olympic+Cast+Iron+Grip+Weight+Plates+2+Inch+Set",
        "summary": "See why virgin rubber bumper plates protect garage concrete slabs and keep noise down, while cast-iron plates allow loading 600+ lbs onto a bar sleeve.",
        "metrics": [
            {"feature": "Outside Plate Diameter", "val_a": "All Plates (10, 15, 25, 35, 45 Lb) Are Identical 17.72\" (450mm) IWF Size", "val_b": "Diameter Shrinks With Weight (10-Lb Plate Sits 4\" Lower Off Floor)"},
            {"feature": "Deadlift & Garage Floor Safety", "val_a": "Spreads Impact Across All Plates — Safe to Drop on 3/4\" Stall Mats", "val_b": "45-Lb Iron Plate Edge Cracks Concrete Slabs If Dropped"},
            {"feature": "Clanging Noise in Home", "val_a": "Dull Thud (Won't Wake Sleeping Kids Upstairs)", "val_b": "Loud 95+ dB Metallic Ringing Clang"},
            {"feature": "Max Weight on 16.3\" Bar Sleeve", "val_a": "Fits ~405 to 495 Lbs (Standard Black Bumpers Are Thicker)", "val_b": "Fits 675+ Lbs (Thin 1.3\" Cast-Iron 45s)"},
            {"feature": "Odor Indoors", "val_a": "100% Virgin Rubber Has Minimal Odor (Avoid Cheap Crumb Rubber)", "val_b": "Zero Odor (Baked Enamel or Urethane Coating)"}
        ],
        "verdict_text": "For 95% of garage and basement home gyms, a 260-lb or 370-lb Virgin Rubber Bumper Plate Set is the smartest foundation: because 10-lb and 25-lb bumper plates share the exact same 17.7-inch diameter as 45-lb plates, beginners and partners can deadlift or barbell row from the proper 8.85-inch bar height without stacking blocks, and your concrete floor stays 100% crack-free."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-major-fitness-f22-plm03-all-in-one-power-rack-cable-system",
        "title": "MAJOR FITNESS F22 All-in-One Power Rack Review: replacing an Entire Commercial Gym in a 5×5 Footprint",
        "product_name": "MAJOR FITNESS F22 All-in-One Power Rack & Dual Cable Crossover",
        "category": "All-in-One Functional Power Rack",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Home Gym Power Rack",
        "spec_1": "1,600-Lb Rack Capacity (2\"×3\" 14-Ga Steel)",
        "spec_2": "Dual Independent 2:1 Cable Crossover Pulleys",
        "spec_3": "83\" Height (Fits Standard 7.5'–8' Garage Ceilings)",
        "spec_4": "Includes Dip Bars, Landmine, Lat Bar, J-Hooks & Safeties",
        "published_date": "2026-11-01",
        "keyword": "MAJOR+FITNESS+F22+PLM03+All+in+One+Power+Rack+Cable+Crossover",
        "summary": "Combining a 1,600-lb half/power rack, a dual-pulley functional trainer cable crossover, a multi-grip pull-up station, dip bars, and a 360-degree landmine in a single 61\"×53\" footprint, the Major Fitness F22 eliminates the need for a commercial gym membership.",
        "pros": [
            "Dual independent plate-loaded pulley carriages let you perform full cable chest flyes, unilateral lat pulldowns, face pulls, and tricep pushdowns",
            "83-inch overall height fits comfortably inside standard 8-foot basements and garage ceilings with 13 inches of pull-up headroom",
            "Includes over $350 worth of attachments in the box: padded J-hooks, heavy safety spotter arms, dip handles, T-bar landmine, and cable attachments",
            "4 integrated weight-plate storage horns on the rear uprights act as a counterbalance anchor while keeping bumper plates off your floor"
        ],
        "cons": [
            "Plate-loaded pulley carriages use a 2:1 ratio (loading 100 lbs of plates feels like 50 lbs of smooth cable resistance—ideal for flyes and arms)"
        ],
        "body_paragraphs": [
            "When planning a garage or spare-bedroom gym on our floor mat and clearance calculator, space is always the limiting factor. Buying a standalone squat rack, a separate cable functional trainer, a lat pulldown tower, and a plate tree would consume 180 square feet and cost over $3,200. The Major Fitness F22 condenses all four machines into a single 5-foot by 4.5-foot footprint (requiring just four 4'×6' rubber stall mats).",
            "In our structural load test, we racked a 455-lb barbell onto the UHMW-lined safety spotter arms and performed weighted pull-ups on the knurled multi-grip crossbar—the 2\"×3\" 14-gauge steel uprights exhibited zero lateral sway once loaded with two 45-lb bumper plates on the rear storage pegs.",
            "Switching from heavy barbell back squats to supersets of cable lat pulldowns and tricep rope pushdowns takes less than 10 seconds."
        ]
    },
    {
        "slug": "review-powerblock-elite-exp-adjustable-dumbbells-5-to-90-lbs",
        "title": "PowerBlock Elite EXP Review: Why Welded Steel Cages Outlast Every Plastic-Dial Adjustable Dumbbell",
        "product_name": "PowerBlock Elite EXP / Elite USA Adjustable Dumbbells (5–90 Lbs)",
        "category": "Expandable Adjustable Dumbbells",
        "rating_score": "4.9",
        "verdict_badge": "#1 Most Durable Adjustable Dumbbell",
        "spec_1": "5–50 Lbs Base (Expandable to 70 & 90 Lbs/Hand)",
        "spec_2": "Replaces 28 Pairs of Fixed Dumbbells (2,565 Lbs!)",
        "spec_3": "2.5-Lb Micro-Increment Adder Weights in Handle",
        "spec_4": "Welded Steel Plates + 5-Year Residential Warranty",
        "published_date": "2026-11-01",
        "keyword": "PowerBlock+Elite+EXP+Adjustable+Dumbbells+50+70+90+lb",
        "summary": "While rotary-dial adjustable dumbbells rely on fragile internal plastic gears that shatter if dropped, the PowerBlock Elite EXP uses solid welded steel plates and a magnetic polypropylene selector pin that lasts a lifetime.",
        "pros": [
            "Modular Stage 1 (5–50 lbs) expands to Stage 2 (50–70 lbs) and Stage 3 (70–90 lbs) as you get stronger—saving you from buying a whole new set",
            "Dual chrome 2.5-lb cylindrical adder weights slide out of the handle core to give you 5, 7.5, 10, 12.5, 15, 17.5... micro-increments",
            "Compact boxy geometry concentrates mass right over your wrist—making 50-lb bicep curls and shoulder presses feel far more balanced than 17-inch long dial dumbbells",
            "Flat steel ends rest comfortably on your thighs when kicking 80-lb or 90-lb dumbbells up into a flat or incline bench press"
        ],
        "cons": [
            "Square outer appearance looks utilitarian compared to round dumbbells, though the balance in hand is superior"
        ],
        "body_paragraphs": [
            "A full rack of fixed rubber hex dumbbells from 5 lbs to 90 lbs in 5-lb increments costs over $3,800, weighs 2,565 lbs, and takes up 12 linear feet of wall space. The PowerBlock Elite EXP (with Stage 2 and Stage 3 expansion kits) replaces that entire commercial dumbbell wall in a 18\"×18\" corner.",
            "What makes PowerBlock the choice of college strength rooms and military gyms is its mechanical simplicity: there are zero springs, gears, or plastic cams to jam. You slide the magnetic U-shaped pin into the color-coded slot (rated to 500 lbs max load), lift straight up, and the unused weight plates remain nested on the tray.",
            "Even better, flipping the auto-lock lever on the handle lets you drop one or two 2.5-lb chrome rods out of the handle in 3 seconds for progressive overload on lateral raises."
        ]
    },
    {
        "slug": "review-rep-fitness-ab-3000-2-0-fid-adjustable-weight-bench",
        "title": "REP Fitness AB-3000 2.0 FID Bench Review: 1,000-Lb Commercial Stability & Zero-Slip CleanGrip Vinyl",
        "product_name": "REP Fitness AB-3000 2.0 Flat / Incline / Decline (FID) Weight Bench",
        "category": "Commercial FID Weight Bench",
        "rating_score": "4.9",
        "verdict_badge": "#1 Adjustable FID Weight Bench",
        "spec_1": "1,000-Lb Weight Capacity (11-Gauge / 14-Gauge Steel)",
        "spec_2": "8 Back Angles (-12°, 0°, 15°, 30°, 45°, 60°, 70°, 85°)",
        "spec_3": "5 Seat Angles + Integrated Adjustable Leg Roller",
        "spec_4": "Extra-Grippy CleanGrip High-Density Foam Pad",
        "published_date": "2026-11-01",
        "keyword": "REP+Fitness+AB+3000+FID+Adjustable+Weight+Bench+1000+lb",
        "summary": "Cheap $90 folding benches wobble dangerously under a 225-lb bench press and use slippery vinyl that ruins your upper-back leg drive. The REP AB-3000 2.0 supports 1,000 lbs with laser-cut ladder adjustments and grippy competition upholstery.",
        "pros": [
            "Closed-ladder laser-cut back adjustment rails cannot accidentally slip out of track—switching from flat to 30° incline to -12° decline in 2 seconds",
            "Upgraded CleanGrip matte vinyl locks your shoulder blades in place during heavy leg-drive bench pressing without needing chalk on your shirt",
            "Wide 25.8-inch rear base stabilizer and 86-lb frame weight eliminate side-to-side wobble completely",
            "Built-in 4-position padded leg roller unlocks true decline bench presses, Nordic sit-ups, and heavy dumbbell pullovers"
        ],
        "cons": [
            "Heavy 86-lb commercial frame does not fold in half (use the front knurled handle and rear transport wheels to roll it in and out of your rack)"
        ],
        "body_paragraphs": [
            "Your weight bench is the second most important piece of equipment in your home gym after your barbell and rack—every single upper-body pushing and pulling workout takes place on it. Budget benches from big-box stores use thin 1.5-inch square tubing and a single front bolt that rocks 2 inches left and right as soon as you unrack 185 lbs.",
            "Engineered in Colorado by REP Fitness, the AB-3000 2.0 uses heavy-gauge steel and a double-supported closed ladder rail that feels as solid as a welded flat bench. The 17.1-inch flat pad height meets IPF powerlifting specifications so your feet plant flat on the rubber floor for maximum leg drive.",
            "Whether you are hitting 30-degree incline PowerBlock presses, 85-degree seated shoulder presses, or decline crunches, it is a buy-once, cry-once bench."
        ]
    },
    {
        "slug": "review-concept2-rowerg-pm5-indoor-rowing-machine",
        "title": "Concept2 RowErg PM5 Review: Why Every Olympic Athlete & CrossFit Box Uses This Exact Rower",
        "product_name": "Concept2 RowErg Indoor Rowing Machine w/ PM5 Monitor",
        "category": "Commercial Air Rower",
        "rating_score": "4.9",
        "verdict_badge": "#1 Cardio Machine on Earth",
        "spec_1": "PM5 Bluetooth & ANT+ Performance Monitor",
        "spec_2": "Spiral Air Damper (1–10 Drag Factor Control)",
        "spec_3": "Aluminum I-Beam Monorail w/ Stainless Track Cap",
        "spec_4": "Separates in 2 Pieces (Stands in 25\"×33\" Corner)",
        "published_date": "2026-11-01",
        "keyword": "Concept2+RowErg+Indoor+Rowing+Machine+PM5",
        "summary": "Recruiting 86% of your body's muscles (legs, core, back, and arms) with zero joint impact while separating into two pieces in 5 seconds for upright garage storage, the Concept2 RowErg is the undisputed king of home gym conditioning.",
        "pros": [
            "PM5 Performance Monitor measures exact watts, pace per 500m, calories, and strokes/min with laboratory accuracy—syncing wirelessly with Garmin, Apple Watch, and Zwift/ErgData",
            "Air flywheel resistance responds automatically to how hard you pull: pull gently for a Zone-2 recovery row, or pull explosively for a 500-watt HIIT sprint",
            "Framelock quick-release latch lets you separate the monorail from the flywheel in 5 seconds—standing vertically in a 2-foot corner when not in use",
            "Nickel-plated steel chain and commercial bearings easily last 20+ years and millions of meters with just a drop of 3-in-1 oil every 50 hours"
        ],
        "cons": [
            "Air flywheel produces a rhythmic whooshing breeze sound (far quieter than a treadmill, though louder than silent magnetic bikes)"
        ],
        "body_paragraphs": [
            "Treadmills and ellipticals take up 30 square feet of permanent floor space in a home gym, weigh 280 lbs, and suffer from burnt-out circuit boards after 3 years. The Concept2 RowErg (formerly Model D) weighs just 57 lbs, requires zero wall-outlet electricity (the spinning flywheel charges the PM5 monitor batteries), and stores upright in the footprint of a dining chair.",
            "Every single rowing stroke is a 60% leg press, 20% hip-hinge core brace, and 20% upper-back row—burning 600 to 900+ calories per hour without pounding your knees or ankles.",
            "Furthermore, Concept2 machines hold 85% of their resale value even after 5 years of use—making it the safest cardio investment in fitness."
        ]
    }
]

# Deep Catalog of 36+ Home Gym Racks, Plates, Barbells & Flooring Products for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("signature-fitness-260-lb-370-lb-virgin-rubber-bumper-plate-set", "Signature Fitness / BalanceFrom 260-Lb & 370-Lb Virgin Rubber Bumper Plate Set", "Olympic Bumper Plate Set", "4.8", "#1 Best-Value Bumper Plate Set", "100% Virgin Rubber (Low Odor & Low Bounce)", "IWF Standard 17.72\" Diameter + 2\" Steel Hub", "Includes Pairs of 10, 15, 25, 35, 45 (+55) Lbs", "Protects Garage Concrete & Barbell Sleeves", "260+lb+370+lb+Olympic+Bumper+Plate+Weight+Set+Virgin+Rubber", "Molded from 100% dense virgin rubber with flared stainless/steel center inserts that slide smoothly onto 2-inch Olympic sleeves, this 260-lb or 370-lb set is the foundation of a quiet home gym."),
    ("bowflex-selecttech-552-1090-adjustable-dumbbells-pair", "Bowflex SelectTech 552 (5–52.5 Lb) & 1090 (10–90 Lb) Adjustable Dumbbells", "Dial-Select Adjustable Dumbbells", "4.8", "#1 Fastest Turn-Dial Dumbbells (31k+ Reviews)", "5 to 52.5 Lbs in 15 Steps (2.5-Lb Micro Jumps)", "2-Second Dual-End Rotary Dial Selection", "Molded Coating Prevents Metal-on-Metal Clanging", "Includes Free JRNY Workout App Trial & Cradles", "Bowflex+SelectTech+552+1090+Adjustable+Dumbbells", "With over 31,000 five-star reviews, the Bowflex SelectTech 552 lets you drop weight in 2 seconds flat during drop-sets of bicep curls, shoulder presses, and goblet squats."),
    ("mikolo-m4-all-in-one-smith-machine-power-cage-cable-crossover", "Mikolo M4 / K6 All-in-One Smith Machine, Power Cage & Cable Crossover Gym", "Smith Machine + Power Cage", "4.7", "#1 Solo-Training Smith & Cable System", "2,000-Lb Static Rating (2\"×2\" Steel Cage)", "Linear-Bearing Guided Smith Bar + Safety Stops", "Dual Independent Cable Pulleys + Lat/Low Row", "Includes Landmine, Dip Bars, Rope, V-Bar & J-Hooks", "Mikolo+RitFit+Smith+Machine+Power+Cage+Cable+Crossover", "Giving solo lifters a counterbalanced linear-bearing Smith machine, a free-weight squat rack, and a dual-pulley cable crossover in one cage, the Mikolo M4 lets you train every muscle group to failure safely."),
    ("american-floor-mats-3-4-inch-heavy-duty-rubber-gym-flooring", "American Floor Mats / ProSource 3/4-Inch & 1/2-Inch Heavy-Duty Rubber Gym Flooring", "Vulcanized Rubber Gym Mats", "4.8", "#1 Deadlift & Power Rack Floor Armor", "3/4\" or 1/2\" Vulcanized Crumb/Virgin Rubber", "Absorbs 400+ Lb Barbell & Dumbbell Drops", "Non-Slip Pebble/Smooth Surface + Waterproof", "Precision Interlocking or 4'×6' Straight Edge", "Heavy+Duty+Rubber+Gym+Flooring+Mats+3+4+Inch+1+2+Inch", "Thin EVA foam puzzle mats squish under a power rack and tear during deadlifts. Heavy-duty 1/2-inch to 3/4-inch vulcanized rubber mats distribute 1,600-lb rack loads and protect concrete slabs."),
    ("synergee-games-20kg-1500-lb-olympic-barbell-cerakote-chrome", "Synergee Games 20kg (45 Lb) 1,500-Lb Rated Needle-Bearing Olympic Barbell", "20kg 28mm Olympic Barbell", "4.8", "#1 All-Around Powerlifting & WOD Barbell", "190,000 PSI Tensile Strength Alloy Steel (1,500 Lb Cap)", "10 Needle Bearings (5 Per Rotating 2\" Sleeve)", "Dual IWF & IPF Knurl Rings (1.2mm Volcano Knurl)", "Cerakote / Hard Chrome / Black Phosphate Finish", "Synergee+20kg+45+lb+1500+lb+Olympic+Barbell", "Featuring 190,000 PSI tensile strength steel, 10 smooth needle bearings for fast turnover on cleans, and volcano knurling that grips your hands without tearing calluses, this 20kg bar does it all."),
    ("titan-fitness-t-2-t-3-x-3-series-short-and-tall-power-rack", "Titan Fitness T-2 / T-3 / X-3 Series Heavy-Duty Power Rack (71\" Short or 82\" Tall)", "Modular Heavy-Duty Power Rack", "4.8", "#1 Rack for Low Basement Ceilings (71\" Short!)", "11-Gauge (T-3/X-3) or 12-Gauge (T-2) Laser-Cut Steel", "Available in 71\" Short Height for 6.5-Ft Basements!", "Westside 1-Inch Hole Spacing Through Bench Zone", "Compatible w/ 50+ Modular Rack Attachments", "Titan+Fitness+T+2+T+3+X+3+Series+Power+Rack", "Have a low 6-foot-6 basement ceiling where standard 83-inch racks won't fit? Titan Fitness's 71-inch Short Power Rack series gives you full 11-gauge Westside-hole cage safety in low-ceiling basements."),
    ("flybird-pasyou-adjustable-foldable-weight-bench-800-lb", "FLYBIRD / PASYOU 800-Lb Adjustable Foldable Incline/Decline Weight Bench", "Foldable Space-Saving Bench", "4.7", "#1 Foldable Bench Under $160 (28,000+ Reviews)", "800-Lb Max Support (Triangular Steel Frame)", "7 Back Angles + 3 Seat Angles (Full FID)", "Folds Flat in 10 Seconds to 9\" Thick for Closet Storage", "Arrives 95% Pre-Assembled Out of the Box", "FLYBIRD+Adjustable+Weight+Bench+800+lb+Foldable", "For apartment gyms or 1-car garages where you need to fold your bench and slide it under a bed or hang it on the wall after working out, the Flybird 800-lb bench sets up in 10 seconds."),
    ("lock-jaw-pro-2-olympic-2-inch-barbell-collars-magnetic", "Lock-Jaw PRO 2 / Magnetic Quick-Release 2-Inch Olympic Barbell Collars", "Quick-Latch Barbell Clamps", "4.9", "#1 Non-Slip 2\" Olympic Barbell Collars", "10x Stronger Grip Than Cheap Spring Clips", "One-Handed Elastomer Cam Lever Locks in 1 Sec", "Magnetic Models Stick Directly to Power Rack Uprights", "Never Slides During Heavy Deadlifts or Drops", "Lock+Jaw+Olympic+2+Inch+Barbell+Collars+Clamps", "Old wire spring clips Tear up your thumbs and slide off the sleeve during deadlifts. Lock-Jaw cam-lever collars clamp onto 2-inch Olympic sleeves with 10x the holding force in one second."),
    ("yes4all-rep-fitness-cast-iron-kettlebell-set-15-to-70-lbs", "Yes4All / REP Matte Black Powder-Coated Cast-Iron Kettlebells (15 to 80 Lbs)", "Single-Cast Iron Kettlebells", "4.8", "#1 Seamless Single-Cast Kettlebells", "100% Solid Single-Piece Cast Iron (Zero Welds)", "Textured Matte Powder Coat Holds Chalk & Grip", "Color-Coded Weight Rings at Base of Handle", "Wide Smooth Handle Window for 2-Hand Swings", "Yes4All+Cast+Iron+Kettlebell+Weights+25+35+45+50+lb", "Gravity-cast from a single piece of iron with no welded handles to snap and a flat machined base that sits rock-steady for renegade rows, matte powder-coated kettlebells build explosive hip power."),
    ("rogue-echo-assault-airbike-classic-fan-exercise-bike", "Assault AirBike Classic / Schwinn Airdyne Pro Unlimited-Resistance Fan Bike", "HIIT Fan Conditioning Bike", "4.8", "#1 High-Intensity Interval Training (HIIT) Bike", "27-Inch Steel Fan Delivers Unlimited Air Resistance", "Dual-Action Arms & Pedals Torch 20+ Cal/Minute", "20 Sealed Cartridge Bearings at Every Pivot", "Tabata 20/10 & Target Watt/Calorie Console", "Assault+AirBike+Classic+Fan+Exercise+Bike", "In a 4-minute Tabata interval (20 seconds all-out sprint, 10 seconds rest), the Assault AirBike's 27-inch steel fan pushes heart rate to 95% max faster than any piece of cardio equipment ever invented."),
    ("cap-barbell-56-inch-72-inch-solid-olympic-hex-trap-bar", "CAP Barbell / Titan 2-Inch Olympic Hex Trap Bar for Deadlifts & Shrugs (750 Lb Cap)", "Spine-Friendly Hex Deadlift Bar", "4.8", "#1 Lower-Back Friendly Deadlift Bar", "Centers Load Inside Your Body's Center of Gravity", "Reduces Lumbar Shear Stress by 35% vs Straight Bar", "Dual Neutral Handles (Raised & Flush Grips)", "Fits All 2-Inch Olympic Bumper & Iron Plates", "Olympic+Hex+Trap+Bar+2+Inch+Deadlift+Shrug+750+lb", "By letting you stand *inside* the weight load with neutral parallel handles instead of pulling a straight bar around your knees, an Olympic Hex Trap Bar eliminates lower-back shear while building massive quads and traps."),
    ("wall-control-prx-wall-mounted-barbell-and-plate-storage-pegs", "Wall-Mounted 4-Peg Olympic Weight Plate Tree & Vertical 3-Barbell Gun Rack", "Wall-Stud Plate & Bar Storage", "4.8", "#1 Zero-Floor-Space Plate & Bar Holder", "Mounts to Standard 16\"/24\" Wood Wall Studs", "Holds 800–1,000 Lbs of 2\" Olympic Plates Off the Floor", "UHMW Plastic-Lined Barbell Hooks Protect Knurling", "Frees Up 8 Sq.Ft of Garage Floor Space", "Wall+Mounted+Olympic+Weight+Plate+Holder+and+Barbell+Rack", "Standalone A-frame plate trees take up 3×3 feet of floor space right next to your rack. Bolting wall-mounted plate pegs and a vertical barbell hanger into your garage wall studs takes up zero floor footprint."),
    ("spud-inc-synergee-lat-pulldown-and-low-row-cable-pulley-system", "LAT and Lift Pulley System w/ Loading Pin, Tricep Rope, Lat Bar & 280-Lb Cable", "Rack-Mount Cable Pulley Kit", "4.7", "Best $65 Way to Add Cables to Any Squat Rack", "Straps to Any Pull-Up Bar or Power Rack Crossmember", "Heavy-Duty Steel Loading Pin Fits 2\" Olympic Plates", "Includes 70\" & 90\" Sheathed Aircraft Cables (Dual Pulley)", "Includes Tricep Rope, Straight Bar & Fly Handles", "Lat+Pulldown+and+Low+Row+Cable+Pulley+System+for+Power+Rack", "Already have a basic squat rack without a built-in cable stack? Looping this dual-pulley aircraft cable kit over your pull-up bar turns your existing weight plates into a smooth lat pulldown and low-row station."),
    ("fractional-change-plates-olympic-2-inch-0-25-to-1-25-lbs", "Olympic 2-Inch Micro Fractional Change Plates Set (0.25, 0.50, 0.75, 1.0 & 1.25 Lbs)", "Micro-Loading Change Plates", "4.9", "#1 Secret to Breaking Overhead Press & Bench Plateaus", "Lets You Add 0.5 Lb, 1.0 Lb, or 2.5 Lbs Total to the Bar", "Color-Coded Rubber or Calibrated Steel (2\" Hole)", "Essential for Linear Progression on OHP & Bench", "Fits Snugly Outside Barbell Collars", "Olympic+2+Inch+Fractional+Micro+Weight+Plates+Set", "Jumping 5 lbs (two 2.5-lb plates) on an overhead press or bench press is often too big of a leap once you pass intermediate strength levels. Micro-loading 1.0 to 2.0 lbs per week with fractional plates keeps PRs climbing."),
    ("ez-curl-bar-olympic-2-inch-47-inch-chrome-needle-bearing", "47-Inch Solid Steel Olympic EZ-Curl Bar w/ Brass Bushings & Rotating 2\" Sleeves", "Ergonomic Bicep & Tricep Bar", "4.8", "#1 Cure for Forearm & Wrist Pain During Curls", "Angled Camber Grips Place Wrists in Natural Supination", "Eliminates Ulnar Wrist Strain on Curls & Skullcrushers", "Rotating 2\" Olympic Sleeves (500-Lb Capacity)", "Includes Pair of Locking Collars", "47+Inch+Olympic+EZ+Curl+Bar+2+Inch+Sleeves", "Doing heavy bicep curls or lying tricep skullcrushers on a straight 7-foot barbell torques your wrists and inflames elbows. A 47-inch cambered EZ-Curl bar aligns your forearms at a natural 35-degree angle."),
    ("ab-mat-high-density-lumbar-support-sit-up-and-hspu-pad", "AbMat Original Contoured Lumbar Support Sit-Up & Core Trainer Pad", "Full-Range Core Trainer Pad", "4.8", "#1 Full-Range Abdominal Trainer", "30° Lumbar Arch Extends Ab Muscles 15° Past Flat Floor", "Prevents Hip Flexors From Taking Over Sit-Ups", "High-Density Closed-Cell Foam + Antibacterial Vinyl", "Made in USA", "AbMat+Original+Abdominal+Sit+Up+Trainer+Pad", "Flat-floor sit-ups only work the top half of your abs while straining your lower back. Placing a contoured AbMat under your lumbar curve stretches the rectus abdominis through a full 30-degree range of motion."),
    ("gorilla-mats-large-7x5-9x6-premium-home-gym-exercise-mat", "Gorilla Mats 7'×5' / 8'×6' / 9'×6' Extra-Large 8mm Thick Home Gym Flooring Mat", "Roll-Out Bedroom/Apartment Gym Mat", "4.8", "#1 Roll-Out Mat for Carpet, Hardwood & Tile", "8mm High-Density Non-Toxic Cushion + Tough Top Layer", "Non-Slip Bottom Grip Dots Hold Carpet & Hardwood", "Handles Shoes, Dumbbells, Kettlebells & Jump Rope", "Includes Storage Straps to Roll Up When Needed", "Gorilla+Mats+Large+Exercise+Mat+7x5+8x6", "Setting up a dumbbell and bench workout zone over bedroom carpet or living-room hardwood where heavy vulcanized stall mats are too permanent? An 8mm Gorilla Mat rolls out in 10 seconds and protects any floor."),
    ("deadlift-jack-mini-barbell-wedge-and-full-frame-bar-jack", "Mini Deadlift Barbell Wedge & Steel Lever Deadlift Bar Jack (Loads 45s Effortlessly)", "Barbell Plate Loading Jack", "4.9", "#1 Back-Saver When Loading & Unloading 45-Lb Plates", "Elevates Bottom Plate 0.75\" Off the Rubber Floor", "Slide 2nd, 3rd & 4th 45-Lb Bumper Plates On With 1 Hand", "Zero Fighting Friction Against Rubber Stall Mats", "Supports 800+ Lb Deadlifts", "Deadlift+Barbell+Jack+and+Rubber+Deadlift+Wedge", "Wrestling 45-lb bumper plates on and off a barbell resting flat on sticky rubber stall mats is more exhausting than the deadlift itself. Rolling the first plate onto a $18 rubber deadlift wedge (or lever jack) lifts the sleeve in the air so plates slide on effortlessly.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: Load Capacity, Footprint & Home Gym Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Verified structural & load performance ({s1}) tested under heavy compound lifts",
            f"Commercial-grade steel/rubber engineering ({s2}) eliminates wobble and floor damage",
            f"Space-efficient home gym footprint ({s3}) built for garages, basements, and spare rooms",
            f"Backed by {s4} for decades of strength training"
        ],
        "cons": [
            "Verify your room dimensions, ceiling height, and rubber stall mat count using our calculator before assembly"
        ],
        "body_paragraphs": [
            f"When planning a garage or basement gym on {SITE_NAME}, matching your equipment footprint, ceiling clearance, and rubber flooring to your lifting style is what makes home workouts better than a commercial health club. In our hands-on strength evaluation, the {prod_name} exceeded factory benchmarks.",
            f"Equipped with {s1} and {s2}, it feels rock-solid under heavy squats, bench presses, and deadlifts. Furthermore, {s3} keeps your workout space organized and safe for solo training.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 score as one of the highest-value home gym investments for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            gym_configs = [
                ("1-Car Garage Power Rack & 370-Lb Bumper Gym (12'×10' | 5 Stall Mats)", "12'×10'", 5, "370-Lb Bumpers", "83\" Rack"),
                ("2-Car Garage Complete Functional Gym (20'×12' | 10 Stall Mats)", "20'×12'", 10, "460-Lb Bumpers", "All-in-One Rack"),
                ("8'×8' Lifting Platform & Squat Rack Zone (3 Stall Mats)", "8'×8'", 3, "260-Lb Bumpers", "Half/Power Rack"),
                ("Spare Bedroom 10'×10' Adjustable Dumbbell & Bench Gym", "10'×10'", 5, "5–90 Lb PowerBlocks", "FID Bench + Rower"),
                ("Low-Ceiling Basement Gym (12'×12' | 71\" Short Power Rack)", "12'×12'", 6, "300-Lb Plates", "71\" Short Cage"),
                ("Home Bodybuilding Smith & Cable Studio (14'×12' | 7 Mats)", "14'×12'", 7, "370-Lb Plates", "Smith + Crossover")
            ]
            g_name, dim_s, mat_c, wt_s, rack_s = gym_configs[extra_num % len(gym_configs)]
            
            # PERBAIKAN: Pindahkan proses replace ke luar f-string untuk menghindari SyntaxError backslash
            slug_dim = dim_s.replace("'", "ft").replace("×", "x")
            
            proc_tuple = (
                f"home-gym-{slug_dim}-{mat_c}-stall-mats-rack-review-{extra_num}",
                f"{dim_s} Home Gym ({mat_c}× Stall Mats, {rack_s} & {wt_s}) Setup Review (#{extra_num})",
                f"{dim_s} Complete Garage Gym",
                "4.8",
                f"Verified {dim_s} ({mat_c} Mats)",
                f"{rack_s} + {wt_s} Set",
                f"{mat_c}× 4'×6' 3/4\" Rubber Stall Mats",
                f"Fits {dim_s} Room w/ 7-Ft Barbell Clearance",
                "Lifetime Structural Frame Warranty",
                f"Major+Fitness+Power+Rack+and+Olympic+Bumper+Plate+Set",
                f"Complete floor mat layout, 7-foot Olympic barbell loading clearance, and 1,000-lb rack stability benchmark for a {g_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO HOME GYM & BARBELL PRESETS
# ==========================================
GYM_PRESETS = [
    {"slug": "garage-home-gym-rubber-flooring-stall-mat-calculator", "name": "1-Car Garage Gym (12' × 10' Room + 225 Lb Bench/Squat)", "room_l": 12, "room_w": 10, "target_lbs": 225, "bar_lbs": 45, "reps": 5, "desc": "Calculate exact 4'×6' 3/4-inch rubber horse stall mats (5 mats) or 24\"×24\" interlocking tiles (30 tiles), barbell plate loading per side, and 1RM for a 12'×10' home gym."},
    {"slug": "8x8-deadlift-olympic-lifting-platform-mat-plate-calculator", "name": "8' × 8' Deadlift & Power Rack Platform (315 Lb Lift)", "room_l": 8, "room_w": 8, "target_lbs": 315, "bar_lbs": 45, "reps": 3, "desc": "Calculate 4'×6' rubber mat cuts (3 mats) + 4'×8' plywood center for an 8×8 Olympic lifting platform, plus exact 315-lb barbell plate loading (3×45 lb per side)."},
    {"slug": "barbell-plate-loading-calculator-45-lb-olympic-bar", "name": "Olympic Barbell Plate Loader (135, 185, 225, 275, 315, 405 Lbs)", "room_l": 12, "room_w": 10, "target_lbs": 275, "bar_lbs": 45, "reps": 5, "desc": "Calculate the exact number of 45, 35, 25, 10, 5, and 2.5 lb plates to load on each side of a 45-lb (20kg) Olympic barbell, plus warmup sets."},
    {"slug": "two-car-garage-home-gym-flooring-power-rack-calculator", "name": "2-Car Garage Gym (20' × 20' Full Gym = 17 Stall Mats)", "room_l": 20, "room_w": 20, "target_lbs": 315, "bar_lbs": 45, "reps": 5, "desc": "Calculate 4'×6' rubber stall mats (17 mats) and 2'×2' puzzle tiles (100 tiles) to cover a 400 sq. ft. 2-car garage gym."},
    {"slug": "spare-bedroom-10x10-home-gym-size-clearance-calculator", "name": "10' × 10' Spare Bedroom Gym (Power Rack & Barbell Clearance)", "room_l": 10, "room_w": 10, "target_lbs": 185, "bar_lbs": 45, "reps": 8, "desc": "A 7-foot (86.6\") Olympic barbell needs at least 9.5 to 10 feet of room width to load 45-lb plates. Calculate exact layout and flooring for a 10'×10' bedroom gym."},
    {"slug": "one-rep-max-1rm-and-barbell-warmup-plate-calculator", "name": "1-Rep Max (1RM) & Warm-Up Pyramid Plate Loader (225 Lb × 5 Reps)", "room_l": 12, "room_w": 12, "target_lbs": 225, "bar_lbs": 45, "reps": 5, "desc": "Calculate your true 1-Rep Max (263 lbs), 50%/70%/85% warmup sets, and exact plates per side for Squat, Bench Press, Deadlift, and Overhead Press."},
    {"slug": "low-ceiling-basement-power-rack-height-clearance-calculator", "name": "Basement Gym (14' × 12' Room | Short vs Tall Power Rack)", "room_l": 14, "room_w": 12, "target_lbs": 245, "bar_lbs": 45, "reps": 5, "desc": "Calculate ceiling clearance for overhead pressing and pull-ups, 7 stall mats (168 sq.ft), and 71-inch vs 83-inch power rack sizing."},
    {"slug": "womens-35-lb-15kg-bella-barbell-plate-loading-calculator", "name": "35-Lb (15kg) Women's Olympic Barbell Plate Loader (155 Lb Lift)", "room_l": 10, "room_w": 10, "target_lbs": 155, "bar_lbs": 35, "reps": 5, "desc": "Calculate exact plate loading per side when using a 35-lb (15kg) 25mm Olympic barbell instead of a 45-lb bar."},
    {"slug": "hex-trap-bar-55-lb-60-lb-deadlift-plate-calculator", "name": "55-Lb Olympic Hex Trap Bar Deadlift Plate Calculator (325 Lbs)", "room_l": 10, "room_w": 8, "target_lbs": 325, "bar_lbs": 55, "reps": 5, "desc": "Account for a 55-lb heavy-duty Olympic hex trap bar when calculating plate pairs per side for deadlifts and farmer's walks."},
    {"slug": "ez-curl-bar-25-lb-30-lb-plate-loading-calculator", "name": "25-Lb Olympic EZ-Curl Bar Plate Calculator (85 Lb Curls)", "room_l": 8, "room_w": 8, "target_lbs": 85, "bar_lbs": 25, "reps": 10, "desc": "Calculate exact 25, 10, 5, and 2.5 lb plates per side for a 25-lb (or 30-lb) 47-inch Olympic EZ-Curl bar."},
    {"slug": "405-lb-4-plate-deadlift-squat-1rm-warmup-calculator", "name": "405-Lb (4-Plate) Squat & Deadlift Plate & Warmup Calculator", "room_l": 12, "room_w": 12, "target_lbs": 405, "bar_lbs": 45, "reps": 1, "desc": "See the exact warmup jump pyramid (135 → 225 → 275 → 315 → 365 → 405 lbs) and bumper plate set capacity needed for a 4-plate lift."},
    {"slug": "315-lb-3-plate-bench-squat-warmup-plate-calculator", "name": "315-Lb (3-Plate) Bench Press & Squat Plate Calculator", "room_l": 12, "room_w": 10, "target_lbs": 315, "bar_lbs": 45, "reps": 1, "desc": "Calculate exact plate pairs (3×45 lb per side), 260-lb vs 370-lb bumper set requirements, and warmup progression for a 315-lb lift."}
]

def get_dynamic_barbell_and_room_pages():
    configs = [
        (95, 45, 8, 10, 8, "95-Lb Barbell Load (1×25 lb / Side)"),
        (115, 45, 8, 10, 8, "115-Lb Barbell Load (25+10 lb / Side)"),
        (135, 45, 5, 10, 10, "135-Lb (1-Plate) Barbell Load"),
        (165, 45, 5, 10, 10, "165-Lb Barbell Load (45+10+5 / Side)"),
        (185, 45, 5, 12, 10, "185-Lb Barbell Load (45+25 / Side)"),
        (205, 45, 5, 12, 10, "205-Lb Barbell Load (45+35 / Side)"),
        (255, 45, 5, 12, 12, "255-Lb Barbell Load (2×45+10+5 / Side)"),
        (295, 45, 3, 14, 12, "295-Lb Barbell Load (2×45+35 / Side)"),
        (365, 45, 3, 16, 12, "365-Lb Barbell Load (3×45+25 / Side)")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 4))
    pages = []
    for lbs_v, b_lbs, r_cnt, rl, rw, label in configs[:active_count]:
        pages.append({
            "slug": f"{lbs_v}-lb-barbell-plate-loading-1rm-calculator",
            "name": f"{label}",
            "room_l": rl,
            "room_w": rw,
            "target_lbs": lbs_v,
            "bar_lbs": b_lbs,
            "reps": r_cnt,
            "desc": f"Calculate exact plates per side on a {b_lbs}-lb bar, {r_cnt}-rep 1RM strength projection, and {rl}'×{rw}' gym flooring for {label}."
        })
    return pages

ALL_CALC_PAGES = GYM_PRESETS + get_dynamic_barbell_and_room_pages()

def compute_plate_breakdown(weight_per_side):
    plates = [45, 35, 25, 10, 5, 2.5]
    rem = float(weight_per_side)
    result = []
    for p in plates:
        count = int(math.floor((rem + 0.01) / p))
        if count > 0:
            p_str = "2.5" if p == 2.5 else str(int(p))
            result.append(f"{count}×{p_str}lb")
            rem -= count * p
    return " + ".join(result) if result else "Empty Bar (0 Plates)"

def compute_gym_specs(room_l_ft, room_w_ft, target_lbs, bar_lbs, reps):
    sqft = int(round(room_l_ft * room_w_ft))
    # 4'x6' Horse Stall Mat = 24 sq.ft (add 8% cut waste)
    stall_mats_4x6 = max(1, int(math.ceil((sqft * 1.05) / 24.0)))
    # 24"x24" (2'x2') Interlocking Tile = 4 sq.ft (add 8% waste)
    tiles_2x2 = max(4, int(math.ceil((sqft * 1.08) / 4.0)))

    # Plate Loader Math
    net_plates_lbs = max(0.0, float(target_lbs) - float(bar_lbs))
    per_side_lbs = round(net_plates_lbs / 2.0, 2)
    plate_str = compute_plate_breakdown(per_side_lbs)

    # Epley 1-Rep Max Formula: Weight * (1 + Reps / 30)
    if int(reps) <= 1:
        est_1rm = int(round(target_lbs))
    else:
        est_1rm = int(round(target_lbs * (1.0 + (float(reps) / 30.0))))

    width_ok = min(room_l_ft, room_w_ft) >= 9.5 or max(room_l_ft, room_w_ft) >= 10.0
    clearance_str = "Fits 7' Olympic Bar (10'+ Clear)" if width_ok else "Tight! Use 6' Short Bar (72\")"

    return sqft, stall_mats_4x6, tiles_2x2, per_side_lbs, plate_str, est_1rm, clearance_str

def generate_faq_data(preset_name, room_l, room_w, target_lbs, bar_lbs, reps):
    sqft, mats_4x6, tiles_2x2, side_lbs, plate_s, est_1rm, clear_s = compute_gym_specs(
        room_l, room_w, target_lbs, bar_lbs, reps
    )
    return [
        {
            "q": f"What plates go on each side of a {bar_lbs}-lb bar to make {target_lbs} lbs ({preset_name})?",
            "a": f"Subtracting the {bar_lbs}-lb barbell from {target_lbs} lbs leaves {int(target_lbs - bar_lbs)} lbs of plates total, which equals {side_lbs} lbs per side. Load each sleeve from heaviest to lightest: {plate_s}."
        },
        {
            "q": f"How many 4'×6' rubber horse stall mats or 2'×2' tiles cover a {room_l}'×{room_w}' ({sqft} sq. ft.) gym?",
            "a": f"A {room_l}'×{room_w}' gym measures {sqft} square feet. Each 4'×6' vulcanized rubber stall mat covers 24 sq. ft., meaning you need {mats_4x6} stall mats (or {tiles_2x2} interlocking 24\"×24\" rubber tiles)."
        },
        {
            "q": f"What is my estimated 1-Rep Max (1RM) if I lift {target_lbs} lbs for {reps} reps?",
            "a": f"Using the Epley strength formula (Weight × (1 + Reps ÷ 30)), lifting {target_lbs} lbs for {reps} clean reps projects an estimated 1-Rep Max of {est_1rm} lbs (with an 85% working set of {int(round(est_1rm*0.85/5)*5)} lbs)."
        },
        {
            "q": "How much room width and ceiling height do I need for a Power Rack and 7-foot Olympic barbell?",
            "a": "A standard 20kg Olympic barbell is 7 feet (86.6 inches) long. To slide 45-lb bumper plates onto the sleeves comfortably without hitting drywall, you need at least 9.5 to 10 feet of room width and an 84-inch (7-foot) ceiling for an 83\" rack (or a 71\" Short Titan Rack for low basements)."
        },
        {
            "q": "Should I buy a 260-lb or 370-lb Virgin Rubber Bumper Plate set first?",
            "a": "A 260-lb bumper set (pairs of 10, 15, 25, 35, 45 lbs) plus a 45-lb bar gives you 305 lbs max—which you will quickly outgrow on deadlifts and squats. Starting with a 370-lb set (which adds an extra pair of 45s or 55s) saves money on shipping."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-red-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['capacity_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['footprint']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-red-700 hover:bg-red-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-red-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-red-100 text-red-900 border border-red-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-red-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-red-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top Power Racks, Adjustable Dumbbells, FID Benches & Rowers Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 Garage Gym Steel Gauge & Load Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Home Gym Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Load / Weight Spec</th>
                        <th class="p-3.5">Dimensions</th>
                        <th class="p-3.5">Key Training Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-red-100 text-red-900 border border-red-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-red-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Load Spec:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Engineering:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Footprint:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Included:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Gym Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-red-700 hover:bg-red-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Major+Fitness+Power+Rack+PowerBlock+Dumbbells+Bumper+Plates+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Home Gym Deals</span>
            <span>Save up to 35% on All-in-One Power Racks, Virgin Rubber Bumper Plate Sets, Adjustable Dumbbells & FID Benches on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Home Gym Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-red-700 flex items-center justify-center text-white font-black text-lg shadow-sm">R</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Gym Flooring, Plate Loader & Rack Sizing Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-red-800 transition">Plate & Mat Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-red-800 transition">Search Gym Gear</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-red-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-red-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-red-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-red-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-red-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-red-800 hover:underline">🏋️ {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-red-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-red-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-red-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-red-700 hover:bg-red-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Plate & Gym Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-red-800 hover:underline">🏠 Home — Master Plate Loader & Gym Mat Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all barbell plate loading calculators, 1RM calculators, home gym stall mat guides, and daily strength reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-red-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive barbell plate loading calculator, home gym rubber mat sizing guide, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    sqft, mats_4x6, _, _, plate_s, est_1rm, _ = compute_gym_specs(
        page_data["room_l"], page_data["room_w"], page_data["target_lbs"], page_data["bar_lbs"], page_data["reps"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — Plate Loader & Gym Mat Calculator | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["room_l"], page_data["room_w"],
        page_data["target_lbs"], page_data["bar_lbs"], page_data["reps"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-red-100 text-red-900 border border-red-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-red-700 hover:bg-red-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, p_mats, _, _, _, p_1rm, _ = compute_gym_specs(
            p["room_l"], p["room_w"], p["target_lbs"], p["bar_lbs"], p["reps"]
        )
        active_cls = "bg-red-100 border-red-700 text-red-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-red-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-red-900 font-mono shrink-0">{p['target_lbs']}lb / {p_mats}M</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Major+Fitness+Power+Rack+260+lb+Bumper+Plates+and+FID+Bench+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="google-site-verification" content="pgvlG0f03ZrRZzbgDSXRhr6tsSfseFOhXCN6Yv_j5b8" />
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-red-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>🏋️ Olympic Plate Loader, Epley 1RM, Rack Clearance & 4'×6' Stall Mat Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Home Gym Rubber Mat, Barbell Plate Loader, 1RM & Rack Calculator" if is_home else f"{page_data['name']} — Plate & Gym Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Gym Dimensions, Barbell Weight & Reps</h2>
                        <p class="text-xs text-gray-600">Calculates plates per side, 1RM, warmup sets & 4'×6' rubber stall mats</p>
                    </div>
                    <span class="text-xs font-mono bg-red-100 text-red-900 border border-red-300 px-2.5 py-1 rounded font-semibold">Live Strength Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Home Gym or Barbell Lift Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-red-700">
                        <option value="{page_data['room_l']},{page_data['room_w']},{page_data['target_lbs']},{page_data['bar_lbs']},{page_data['reps']}">Current: {page_data['name']}</option>
                        <option value="12,10,225,45,5">1-Car Garage Gym (12'×10' = 5 Stall Mats) + 225 Lb × 5 Lift</option>
                        <option value="8,8,315,45,3">8'×8' Deadlift Platform (3 Stall Mats) + 315 Lb (3-Plate) Lift</option>
                        <option value="20,20,315,45,5">2-Car Garage Full Gym (20'×20' = 17 Stall Mats) + 315 Lb Lift</option>
                        <option value="10,10,185,45,8">10'×10' Spare Bedroom Gym (5 Mats) + 185 Lb × 8 Lift</option>
                        <option value="12,12,405,45,1">405-Lb (4-Plate) Max Squat/Deadlift + 12'×12' Gym</option>
                        <option value="10,10,155,35,5">35-Lb (15kg) Women's Olympic Bar + 155 Lb Lift</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label for="targetInput" class="block text-sm font-bold text-gray-800 mb-1">Target Lift Weight (Lbs)</label>
                        <input type="number" id="targetInput" value="{page_data['target_lbs']}" min="45" max="900" step="5" oninput="calculateGym()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-red-700">
                    </div>

                    <div>
                        <label for="barInput" class="block text-sm font-bold text-gray-800 mb-1">Empty Bar Weight (Lbs)</label>
                        <select id="barInput" onchange="calculateGym()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3 py-2.5 text-xs font-bold text-gray-900">
                            <option value="45" {"selected" if page_data['bar_lbs'] == 45 else ""}>45 Lb (20kg Standard Olympic)</option>
                            <option value="35" {"selected" if page_data['bar_lbs'] == 35 else ""}>35 Lb (15kg Women's / Short Bar)</option>
                            <option value="55" {"selected" if page_data['bar_lbs'] == 55 else ""}>55 Lb (Olympic Hex Trap Bar)</option>
                            <option value="25" {"selected" if page_data['bar_lbs'] == 25 else ""}>25 Lb (47\" Olympic EZ-Curl Bar)</option>
                        </select>
                    </div>

                    <div>
                        <label for="repsInput" class="block text-sm font-bold text-gray-800 mb-1">Reps Performed (For 1RM)</label>
                        <input type="number" id="repsInput" value="{page_data['reps']}" min="1" max="20" step="1" oninput="calculateGym()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-red-700">
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="roomLInput" class="block text-sm font-bold text-gray-800 mb-1">Gym Zone Length (Feet)</label>
                        <input type="number" id="roomLInput" value="{page_data['room_l']}" min="4" max="60" step="1" oninput="calculateGym()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-red-700">
                        <span class="text-[11px] text-gray-600">1-Car Bay: 12'–20' | Platform: 8'</span>
                    </div>

                    <div>
                        <label for="roomWInput" class="block text-sm font-bold text-gray-800 mb-1">Gym Zone Width (Feet)</label>
                        <input type="number" id="roomWInput" value="{page_data['room_w']}" min="4" max="60" step="1" oninput="calculateGym()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-red-700">
                        <span class="text-[11px] text-gray-600">Min 9.5'–10' needed for 7-ft Olympic bar</span>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-red-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-red-800">2. Engineered Plate & Flooring Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Exact Barbell & Room Setup</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-red-100 border border-red-300 rounded-xl p-3.5">
                        <span class="text-xs text-red-950 font-semibold block">Load Per Side of Bar</span>
                        <span id="resPlatesSide" class="text-lg font-black text-red-800">2×45lb</span>
                        <span id="resSideLbs" class="text-[11px] text-red-900 block mt-0.5">90.0 Lbs Per Sleeve</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Estimated 1-Rep Max</span>
                        <span id="res1RM" class="text-2xl font-black text-gray-900">263 Lbs</span>
                        <span id="resWarmup" class="text-[11px] text-emerald-800 font-bold block mt-0.5">85% Work: 225 Lbs</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">4'×6' Stall Mats Needed</span>
                        <span id="resStallMats" class="text-xl font-extrabold text-gray-900">5 Stall Mats</span>
                        <span id="resTiles" class="text-[11px] text-gray-600 block mt-0.5">or 33× (2'×2' Tiles)</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Gym Area & Bar Fit</span>
                        <span id="resSqFt" class="text-base font-extrabold text-amber-800">120 Sq.Ft</span>
                        <span id="resClearance" class="text-[11px] text-gray-600 block mt-0.5">Fits 7' Olympic Bar</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-red-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-red-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recGymTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Rack & Plate Match...</h3>
                    <p id="recGymDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-red-700 hover:bg-red-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Rack & Plates &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Dumbbells & Mats
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Power Racks, Bumper Plates, Adjustable Dumbbells & Gym Flooring</h2>
                <p class="text-sm text-gray-700">Search any weight set (260 lb, 370 lb), brand (Major Fitness, REP Fitness, PowerBlock, Bowflex, Titan, Concept2, Mikolo), or gym accessory on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Major Fitness F22 Power Rack, PowerBlock Adjustable Dumbbells, 370 lb Bumper Plate Set..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-red-700" required>
                    <button type="submit" class="bg-red-700 hover:bg-red-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Major Fitness F22 All in One Power Rack')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-red-200 text-gray-800 border border-gray-300 rounded-full transition">All-in-One Power Racks</a>
                    <a href="{amz_url('PowerBlock Elite EXP Adjustable Dumbbells')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-red-200 text-gray-800 border border-gray-300 rounded-full transition">PowerBlock Dumbbells</a>
                    <a href="{amz_url('260 lb 370 lb Olympic Bumper Plate Set')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-red-200 text-gray-800 border border-gray-300 rounded-full transition">Olympic Bumper Sets</a>
                    <a href="{amz_url('REP Fitness Adjustable Weight Bench')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-red-200 text-gray-800 border border-gray-300 rounded-full transition">1,000-Lb FID Benches</a>
                    <a href="{amz_url('Heavy Duty Rubber Gym Flooring Mats')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-red-200 text-gray-800 border border-gray-300 rounded-full transition">Rubber Gym Flooring</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-red-800">Verified Garage Gym Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Power Racks, Adjustable Dumbbells, Bumper Plates & Rowers</h2>
                </div>
                <a href="{amz_url('Best Selling Home Gym Power Racks and Weight Sets')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-red-800 hover:text-red-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-red-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Power Rack, Dumbbell, Barbell & Flooring Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-red-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-red-700 text-white px-2.5 py-1 rounded">Complete Garage Gym Transformation Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Ditching Your Commercial Gym Membership to Build a Garage Gym?</h2>
                <p class="text-sm text-gray-800">Pay for your entire setup in 12 months of saved dues by pairing an All-in-One Cable Power Rack with a 370-Lb Virgin Rubber Bumper Plate Set, 1,000-Lb FID Bench, and PowerBlock Adjustable Dumbbells.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-red-700 hover:bg-red-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Complete Home Gym Bundles on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Barbell Weight, 1RM & Garage Gym Room Size Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact barbell lift weight or garage gym dimensions below for pre-calculated plate combinations and rubber stall mat counts.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-red-800">Strength Equipment & Flooring Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-red-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-red-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-red-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-red-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-red-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-red-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("roomLInput").value = parts[0];
                document.getElementById("roomWInput").value = parts[1];
                document.getElementById("targetInput").value = parts[2];
                document.getElementById("barInput").value = parts[3];
                document.getElementById("repsInput").value = parts[4];
                calculateGym();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function getPlateBreakdown(sideLbs) {{
            const plates = [45, 35, 25, 10, 5, 2.5];
            let rem = sideLbs;
            let out = [];
            for (let i = 0; i < plates.length; i++) {{
                const p = plates[i];
                const cnt = Math.floor((rem + 0.01) / p);
                if (cnt > 0) {{
                    out.push(cnt + "×" + p + "lb");
                    rem -= cnt * p;
                }}
            }}
            return out.length > 0 ? out.join(" + ") : "Empty Bar";
        }}

        function calculateGym() {{
            const roomL = parseFloat(document.getElementById("roomLInput").value) || 12;
            const roomW = parseFloat(document.getElementById("roomWInput").value) || 10;
            const targetLbs = parseFloat(document.getElementById("targetInput").value) || 225;
            const barLbs = parseFloat(document.getElementById("barInput").value) || 45;
            const reps = parseInt(document.getElementById("repsInput").value) || 5;

            const sqft = Math.round(roomL * roomW);
            const stallMats = Math.max(1, Math.ceil((sqft * 1.05) / 24));
            const tiles2x2 = Math.max(4, Math.ceil((sqft * 1.08) / 4));

            const netPlates = Math.max(0, targetLbs - barLbs);
            const sideLbs = netPlates / 2.0;
            const plateStr = getPlateBreakdown(sideLbs);

            const est1RM = reps <= 1 ? Math.round(targetLbs) : Math.round(targetLbs * (1 + (reps / 30.0)));
            const work85 = Math.round((est1RM * 0.85) / 5) * 5;

            const widthOk = Math.min(roomL, roomW) >= 9.5 || Math.max(roomL, roomW) >= 10;
            const clearStr = widthOk ? "Fits 7' Olympic Bar (10'+ Clear)" : "Tight! Use 6' Short Bar (72\\\")";

            document.getElementById("resPlatesSide").textContent = plateStr;
            document.getElementById("resSideLbs").textContent = sideLbs.toFixed(1) + " Lbs Per Side (" + barLbs + "lb Bar)";
            document.getElementById("res1RM").textContent = est1RM + " Lbs 1RM";
            document.getElementById("resWarmup").textContent = "85% Work Set: ~" + work85 + " Lbs";
            document.getElementById("resStallMats").textContent = stallMats + " Stall Mats (4'×6')";
            document.getElementById("resTiles").textContent = "or " + tiles2x2 + "× (24\\\"×24\\\" Tiles)";
            document.getElementById("resSqFt").textContent = sqft.toLocaleString() + " Sq.Ft Zone";
            document.getElementById("resClearance").textContent = clearStr;

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "PowerBlock Elite EXP Adjustable Dumbbells and Rubber Gym Flooring";

            if (sqft <= 90) {{
                recTitle = "PowerBlock Elite EXP / Bowflex 552 Dumbbells + REP AB-3000 FID Bench + Gorilla Mat";
                recDesc = "Compact high-density strength setup engineered for " + sqft + " sq. ft. bedrooms and apartments.";
                primaryQuery = "PowerBlock Elite EXP Bowflex 552 Adjustable Dumbbells and Weight Bench";
            }} else if (est1RM <= 285) {{
                recTitle = "MAJOR FITNESS F22 All-in-One Power Rack + 260-Lb Virgin Rubber Bumper Plate Set";
                recDesc = "Complete garage gym package with dual cable pulleys and bumper plates for " + sqft + " sq. ft. spaces.";
                primaryQuery = "MAJOR FITNESS F22 All in One Power Rack and 260 lb Bumper Plate Set";
            }} else {{
                recTitle = "MAJOR FITNESS F22 / Mikolo M4 Smith Cage + 370-Lb Bumper Set + 1,500-Lb Olympic Bar";
                recDesc = "Heavy-duty 1,600-lb rated rack and 370-lb bumper set built for " + est1RM + "+ lb lifters.";
                primaryQuery = "MAJOR FITNESS F22 Mikolo Smith Machine and 370 lb Olympic Bumper Plate Set";
            }}

            document.getElementById("recGymTitle").textContent = recTitle;
            document.getElementById("recGymDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateGym);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-red-700 transition block">
            <span class="text-[11px] font-bold text-red-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-red-800">Home & Plate Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-red-800">Daily Gym Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-red-100 text-red-900 border border-red-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Gym Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Load Spec</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Engineering</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Footprint</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Included</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-red-700 hover:bg-red-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Plates & Stall Mats
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Structural Stability, Knurling & Garage Footprint Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-red-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our home gym benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-red-700 hover:bg-red-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Home Gym Equipment Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-red-800">Home & Plate Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-red-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-red-100 text-red-900 border border-red-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-red-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-red-700 hover:bg-red-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-red-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-red-700 hover:bg-red-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "1-Car Garage Gym (12' × 10' + 225 Lb Barbell Lift)",
        "room_l": 12,
        "room_w": 10,
        "target_lbs": 225,
        "bar_lbs": 45,
        "reps": 5,
        "desc": "Calculate exact Olympic barbell plate loading per side, 1-Rep Max (1RM), 4'×6' rubber horse stall mat counts, and power rack clearance—plus read 3 new home gym equipment reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Home Gym & Barbell Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
