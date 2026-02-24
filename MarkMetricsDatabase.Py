# MarkMetricsDatabase for Pro-Wrestlers: Made by monkmode

import pandas as pd
import spacy
from collections import Counter
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 50)

# Load existing CSV if it exists, otherwise create new dataframe
CSV_PATH = 'wrestling_markmetrics.csv'

if os.path.exists(CSV_PATH):
    wrestling_df = pd.read_csv(CSV_PATH)
    print(f"✓ Loaded {len(wrestling_df)} wrestlers from existing database.\n")
else:
    # List of Wrestlers
    wrestler_data = pd.Series([
                    'Rob Van Dam',
                    'Karl Gotch',
                    'CM Punk', 
                    'MJF', 
                    'Bryan Danielson', 
                    'Mitsuhara Misawa', 
                    'AJ Styles', 
                    'Kurt Angle', 
                    'Swerve Strickland', 
                    'Ric Flair',
                    'Shawn Michaels',
                    'Jeff Hardy',
                    'Samoa Joe',
                    'Brock Lesnar',
                    'Steve Austin',
                    'Mick Foley'], index = list(range(1, 17)), name = 'Wrestlers')

    # List of Wrestlers Nicknames
    nicknames_data = pd.Series([
                    "The Whole F'N Show",
                    'The God Of Pro Wrestling',
                    'Best in the World',
                    'Better Than You',
                    'American Dragon',
                    'Mr. Triple Crown',
                    'The Phenomenal One',
                    'The Wrestling Machnine',
                    'Swerve',
                    'The Nature Boy',
                    'The Heartbreak Kid',
                    'The Charismatic Enigma',
                    'The Samoan Submission Machine',
                    'The Beast',
                    'Bionic Redneck',
                    'Cactus Jack'], index = list(range(1,17)), name = 'Nicknames')

    bestmatch_data = pd.Series([
                    "Rob Van Dam v. Jerry Lynn @ Living Dangerously | March.21.1999",
                    "Karl Gotch & Lou Thesz v. Antonio Inoki & Seiji Sakaguchi @ NJPW | October.14.1973",
                    "CM Punk v. John Cena @ Money in The Bank | July.17.2011",
                    "MJF v. Bryan Danielson @ Revolution | March.5.2023",
                    "Bryan Danielson v. Nigel McGuinness @ Unified | August.12.2006",
                    "Mitsuhara Misawa v. Kenta Kobashi @ NOAH | March.1.2003",
                    "AJ Styles v. Brock Lesnar @ Survivor Series | November.19.2017",
                    "Kurt Angle v. Undertaker @ No Way Out | February.19.2006",
                    "Swerve Strickland v. Adam Page @ Full Gear | November.18.2023",
                    "Ric Flair v. Terry Funk @ Clash of Champions | November.15.1989",
                    "Shawn Michaels v. Undertaker @ Wrestlemania 25 | April.5.2009",
                    "Jeff Hardy v. CM Punk @ Night of Champions | July.26.2009",
                    "Samoa Joe v. Christopher Daniels v. AJ Styles @ Unbreakable | September.11.2005",
                    "Brock Lesnar v. Kurt Angle @ Smackdown | September.18.2003",
                    "Steve Austin v. Bret Hart @ Wrestlemania 13 | March.13.1997",
                    "Cactus Jack v. Triple H @ Royal Rumble | January.23.2000"], index = list(range(1,17)), name = 'Best Match')

    bestpromo_data = pd.Series([
                    """Rob Van Dam promo w/ Bill Alfonso @ One Night Stand 2005: Talk about the pressure, no sweat.
                    I didn't sweat it, you know why?
                    Because I was going to have the opportunity to come out and actually use my abilities and my skills to make sure that everybody watching went home happy. 
                    As long as I got the chance to do my part, that's all that mattered, you know why?
                    I'm the whole fuckin' show! Mister Pay-Per-View! Mr. Monday Night! You remember what RVD 4:20 means? I just smoked your ass!
                    Fonsi, how long did I defend that World Television Title?""",

                    """Karl Gotch Promo: To tell you the truth, the British would do very well. In America… you get top competition all the time… I love my work. I would wrestle for nothing if I had to!,
                    Among the men, I have a reputation for being 'gym crazy'… I'd rather spend hours there than go into the ring in poor shape.""",

                    """CM Punk's 'Pipebomb' @ Monday Night Raw 2011:  The only thing that's real is me and the fact that day in and day out, for almost six years, I have proved to everybody in the world that I am the best on this microphone, 
                    in that ring, even in commentary! Nobody can touch me! 
                    And yet no matter how many times I prove it, I'm not on your lovely little collector cups.
                    I'm not on the cover of the program. I'm barely promoted. I don't get to be in movies. I'm certainly not on any crappy show on the USA Network.
                    I'm not on the poster of WrestleMania. I'm not on the signature that's produced at the start of the show. I'm not on Conan O'Brian. I'm not on Jimmy Fallon.
                    But the fact of the matter is, I should be.  And trust me, this isn't sour grapes. But the fact that Dwayne is in the main event at WrestleMania next year and I'm not makes me sick!""", 

                    """MJF promo against William Regal @ AEW Dynamite 2022:  And now you have snuck into my company like a flea ridden rat by sticking to talents far better than you ever were, like a succubus!
                    And you know who I am? I'm MJF! Oh yeah! I'm the twenty-six year-old kid who's on top of this business, I'm a generational talent!
                    And I'm also the man who your former employers now, would be willing to take several human lives simply to get me to put pen to paper in the Bidding War of 2024.
                    I want you to look at me nice and good when I say this Regal, I read that email every single day, but not, not to put a chip on my shoulder, no no, I read that email whenever I need a good hearty laugh.
                    Because that's what you've become to me, Will: Nothing more than a joke. And you know who I'm about to become? The AEW Champion of the World! Because my name is Maxwell Jacob Friedman, and I'm better than you, and you know it!""",

                    """Daniel Bryan 'Fight For Your Dreams' promo @ Smackdown: Thank you guys very much. Now first, last week something horrific happened to Shane McMahon. And as General Manager, I will be addressing that situation, but unfortunately, the two people that I need to talk to are not here yet.
                    So with that said, I am gonna talk about something else.
                    A little over two years ago, when I was forced to retire, it was one of the hardest days of my life. 
                    But I focused on one thing: on being grateful. And I kept on focusing on trying to be grateful… There were times when I was depressed about not being able to do what I love to do. 
                    And I focused on being grateful. And I have a lot to be grateful for. … It's wonderful that you're grateful, but you need to fight and you need to fight for your dreams… YOU DON'T WALK OUT! 
                    … FIGHT FOR YOUR DREAMS, FIGHT FOR YOUR DREAMS, FIGHT FOR YOUR DREAMS AND IF YOU FIGHT FOR YOUR DREAMS, YOUR DREAMS WILL FIGHT FOR YOU!
                    Because every hard thing seems impossible until it becomes real. And over the last two months, I've asked WWE to relook at my case… they cleared me. … And lastly, but not leastly, I would like to say thank you… to Brie."
                    So, now onto the fun stuff, right? I don't know exactly when or where I will get back in this ring… but will Daniel Bryan compete in a WWE ring again?!""",

                    """Misawa promo @ Press Conference in 2000: I would like to see August at the earliest, and I would like to have the launch event in August and September.
                    Regarding the staff… they are employees. It's complicated… so please refrain from talking about it now. 
                    I wanted to make the current All Japan Pro Wrestling production… more modern for young people.
                    There were… fan letters asking for something like All Japan… so in that case we decided to do it ourselves.
                    The promotion… is called 'NOAH'—from Noah's Ark… taking twenty-five athletes and six staff members on board… set off on a great voyage without being swallowed by the flood.""",

                    """AJ Styles Promo against John Cena: I'm better than the Best in the World, I am the Phenomenal AJ Styles.""",

                    """Kurt Angle Promo against Justin Credible: You know… when one speaks your name very fast, it just sounds like just incredible.""",

                    """Swerve Strickland Promo @ AEW Rampage: But Swerve has not thrown every bullet that he has in the Chamber.""",

                    """Ric Flair 'Stylin and Profile' Promo: It's so hard for me to sit back here, in this studio'
                    Looking at a guy out here hollering my name.
                    When last year I spent more money on spilt liquor.
                    In bars from one side of this world to the other, than you made.
                    You're talking to the Rolex wearing, diamond ring wearing, kiss stealing (WOO!)
                    Wheeling dealing, Limousine riding, Jet Flying, son of a gun
                    And I'm having a hard time holding these alligators down
                    Woo!""",

                    """Shawn Michaels Promo @ WWE Raw in Montreal 2005: Who's your daddy, Montreal? … I am the SHOWSTOPPER…""",

                    """Jeff Hardy Promo @ Smackdown July 2005: Not goodbye forever… this is only goodbye for now…""",

                    """Samoa Joe Promo @ Smackdown: I came to put a champion to sleep. """,

                    """Brock Lesnar Promo: ...making him feel my pain.""",

                    """Steve Austin 3:16 Promo @ WWF King of the Ring tournament June.23.1996: Austin 3:16 says I just whipped your ass!""",

                    """Cactus Jack Promo: You sick sons of bitches…"""], index = list(range(1,17)), name = 'Best Promo')

    besttitle_data = pd.Series([
                    "ECW World Television Champion, longest reign in history",
                    "NWA World Tag Team Champion, with Rene Goulet",
                    "434-day WWE Champion, defeated John Cena at MITB 2011",
                    "AEW World Champion, defeated Jon Moxley at Full Gear 2022",
                    "ROH World Champion, reign during 2005-2006 era",
                    "Triple Crown Champion, AJPW, 1992 & 1995 reigns",
                    "TNA World Heavyweight Champion, defining run in 2013",
                    "WWE Champion, Olympic gold medalist turned top guy (2000)",
                    "AEW World Champion, defeated Samoa Joe at AEW Dynasty 2024",
                    "NWA World Heavyweight Champion, 10-time champion",
                    "WWE Champion, run leading to WrestleMania 12",
                    "World Heavyweight Champion, 2008 run post-CM Punk feud",
                    "ROH World Champion, early 2000s breakout star",
                    "WWE Universal Champion, dominant titleholder 2020–2022",
                    "WWF Champion, Attitude Era standard-bearer (1998–1999)",
                    "WWF Champion, 1999 feud with The Rock and Triple H"
                    ], index = list(range(1,17)), name= 'Best Title Run')

    wrestling_df = pd.concat([
        wrestler_data,
        nicknames_data,
        bestmatch_data,
        bestpromo_data,
        besttitle_data
    ], axis=1)

    wrestling_df.columns = [
        'Wrestler',
        'Nickname',
        'Best Match',
        'Best Promo', 
        'Best Title Run'
    ]

# Load spaCy NLP model
nlp = spacy.load('en_core_web_sm')


def display_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("   MARKMETRICS PRO-WRESTLING DATABASE")
    print("="*50)
    print("1. View All Wrestlers")
    print("2. Search for a Wrestler")
    print("3. Add New Wrestler")
    print("4. Analyze Promo Trends")
    print("5. Analyze Title Run Entities")
    print("6. Exit")
    print("="*50)


def view_all_wrestlers(df):
    """Display all wrestlers in a readable format."""
    print("\n📍 ALL WRESTLERS IN MARKMETRICS:\n")
    for idx, row in df.iterrows():
        print(f"{idx + 1}. {row['Wrestler']} - '{row['Nickname']}'")
    print()


def search_wrestler(df):
    """Search for a specific wrestler."""
    search_term = input("\nEnter wrestler name to search: ").strip().lower()
    results = df[df['Wrestler'].str.lower().str.contains(search_term, na=False)]
    
    if results.empty:
        print(f"❌ No wrestlers found matching '{search_term}'")
        return
    
    for idx, row in results.iterrows():
        print(f"\n{'='*50}")
        print(f"✦ {row['Wrestler']} - {row['Nickname']}")
        print(f"{'='*50}")
        print(f"Best Match: {row['Best Match']}")
        print(f"\nBest Promo:\n{row['Best Promo'][:200]}...\n")
        print(f"Best Title Run: {row['Best Title Run']}")
        print()


def add_new_wrestler(df):
    """Add a new wrestler to the database with validation."""
    print("\n" + "="*50)
    print("   ADD NEW WRESTLER TO MARKMETRICS")
    print("="*50)
    
    # Validate wrestler name isn't duplicate
    while True:
        name_new = input("\nEnter wrestler's name: ").strip()
        if not name_new:
            print("❌ Name cannot be empty. Try again.")
            continue
        if name_new.lower() in df['Wrestler'].str.lower().values:
            print(f"❌ '{name_new}' already exists in database. Try a different name.")
            continue
        break
    
    # Get other inputs with validation
    while True:
        nickname_new = input("Enter the wrestler's nickname: ").strip()
        if not nickname_new:
            print("❌ Nickname cannot be empty. Try again.")
            continue
        break
    
    while True:
        best_match_new = input("Enter the best match (e.g., 'X v. Y @ Event | Date'): ").strip()
        if not best_match_new:
            print("❌ Match cannot be empty. Try again.")
            continue
        break
    
    while True:
        best_promo_new = input("Enter the best promo: ").strip()
        if not best_promo_new:
            print("❌ Promo cannot be empty. Try again.")
            continue
        break
    
    while True:
        best_titlerun_new = input("Enter the best title run: ").strip()
        if not best_titlerun_new:
            print("❌ Title run cannot be empty. Try again.")
            continue
        break
    
    # Confirm before adding
    print(f"\n{'─'*50}")
    print(f"✓ Wrestler: {name_new}")
    print(f"✓ Nickname: {nickname_new}")
    print(f"✓ Best Match: {best_match_new}")
    print(f"✓ Best Title Run: {best_titlerun_new}")
    print(f"{'─'*50}")
    
    confirm = input("Confirm adding this wrestler? (y/n): ").strip().lower()
    
    if confirm == 'y':
        new_row = pd.DataFrame([{
            'Wrestler': name_new,
            'Nickname': nickname_new,
            'Best Match': best_match_new,
            'Best Promo': best_promo_new,
            'Best Title Run': best_titlerun_new
        }])
        
        updated_df = pd.concat([df, new_row], ignore_index=True)
        print(f"\n✅ {name_new} added successfully!")
        return updated_df
    else:
        print("\n❌ Wrestler not added.")
        return df


def analyze_promo_trends(df):
    """Analyze and display common words in promos."""
    print("\n" + "="*50)
    print("   PROMO WORD FREQUENCY ANALYSIS")
    print("="*50)
    
    # Clean and process promos
    df_clean = df.copy()
    df_clean['Best Promo'] = df_clean['Best Promo'].str.replace(r'\bpromo\b', '', case=False, regex=True)
    df_clean['Best Promo'] = df_clean['Best Promo'].str.replace(r'^.*?:', '', regex=True)
    
    bestpromo_doc = df_clean['Best Promo'].apply(nlp)
    bestpromo_tokens = []
    
    for doc in bestpromo_doc:
        bestpromo_tokens.extend([token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop])
    
    commonpromo_terms = Counter(bestpromo_tokens).most_common(20)
    
    print("\n🎤 Top 20 Most Common Words in Best Promos:\n")
    for i, (term, freq) in enumerate(commonpromo_terms, 1):
        print(f"{i:2d}. '{term}' - {freq} times")
    print()


def analyze_titlerun_entities(df):
    """Analyze named entities in title runs."""
    print("\n" + "="*50)
    print("   TITLE RUN ENTITY ANALYSIS")
    print("="*50)
    
    best_titlerun_doc = [nlp(text) for text in df['Best Title Run']]
    units = []
    
    for doc in best_titlerun_doc:
        units.extend([ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PERSON', 'DATE', 'EVENT']])
    
    unit_counts = Counter(units).most_common(20)
    
    print("\n🏆 Most Common Entities in Title Runs:\n")
    for i, (ent, count) in enumerate(unit_counts, 1):
        print(f"{i:2d}. {ent} - {count} occurrence(s)")
    print()


def main():
    """Main program loop."""
    global wrestling_df
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            view_all_wrestlers(wrestling_df)
        elif choice == '2':
            search_wrestler(wrestling_df)
        elif choice == '3':
            wrestling_df = add_new_wrestler(wrestling_df)
        elif choice == '4':
            analyze_promo_trends(wrestling_df)
        elif choice == '5':
            analyze_titlerun_entities(wrestling_df)
        elif choice == '6':
            print("\n💾 Saving database...")
            wrestling_df.to_csv(CSV_PATH, index=False)
            print("✅ Database saved successfully!")
            print("See you later, champion! 🏆\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
