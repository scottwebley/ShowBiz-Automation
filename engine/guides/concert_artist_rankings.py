"""
===========================================
ShowBiz Concert Artist Rankings
Version 1.0
===========================================

Editorial importance scores for
major touring artists.

Higher numbers mean higher priority
when selecting concerts for the
ShowBiz Concert Guide.
"""

ARTIST_RANKINGS = {

    # Pop
    "Taylor Swift": 500,
    "Beyoncé": 500,
    "Lady Gaga": 490,
    "Adele": 490,
    "Bruno Mars": 485,
    "The Weeknd": 480,
    "Billie Eilish": 475,
    "Olivia Rodrigo": 475,
    "Ed Sheeran": 470,
    "Dua Lipa": 470,
    "Justin Timberlake": 460,
    "Katy Perry": 455,
    "P!nk": 455,
    "Harry Styles": 450,
    "Shawn Mendes": 445,
    "Miley Cyrus": 445,
    "Sabrina Carpenter": 445,
    "Chappell Roan": 440,
    "Charli XCX": 435,
    "Lorde": 430,

    # Rock
    "Bruce Springsteen": 500,
    "Paul McCartney": 500,
    "The Rolling Stones": 500,
    "Metallica": 495,
    "Bon Jovi": 490,
    "Coldplay": 490,
    "Foo Fighters": 485,
    "U2": 485,
    "Pearl Jam": 480,
    "Green Day": 475,
    "Red Hot Chili Peppers": 475,
    "Journey": 470,
    "Def Leppard": 470,
    "The Who": 470,
    "Eagles": 470,
    "Guns N' Roses": 470,
    "AC/DC": 470,
    "Imagine Dragons": 465,
    "Blink-182": 460,
    "Nickelback": 455,

    # Country
    "Morgan Wallen": 500,
    "Luke Combs": 495,
    "Chris Stapleton": 490,
    "Zach Bryan": 485,
    "Lainey Wilson": 480,
    "Carrie Underwood": 480,
    "Keith Urban": 475,
    "Jason Aldean": 470,
    "Thomas Rhett": 465,
    "Old Dominion": 460,
    "Brooks & Dunn": 460,
    "Tim McGraw": 460,
    "Kenny Chesney": 455,
    "Eric Church": 455,
    "Miranda Lambert": 450,
    "Little Big Town": 445,
    "Dierks Bentley": 445,
    "Scotty McCreery": 440,
    "Alabama": 440,

    # Latin
    "Bad Bunny": 500,
    "Karol G": 495,
    "Shakira": 495,
    "Rauw Alejandro": 485,
    "Peso Pluma": 480,
    "Fuerza Regida": 475,
    "Grupo Frontera": 470,
    "Luis Miguel": 470,
    "Marc Anthony": 470,
    "Alejandro Fernández": 465,
    "Maná": 465,
    "Los Tigres del Norte": 460,
    "J Balvin": 460,
    "Maluma": 455,
    "Aventura": 455,

    # Hip-Hop
    "Drake": 500,
    "Kendrick Lamar": 500,
    "Eminem": 500,
    "Travis Scott": 495,
    "J. Cole": 490,
    "Post Malone": 490,
    "Future": 485,
    "Lil Baby": 475,
    "Tyler, The Creator": 475,
    "21 Savage": 470,
    "Doja Cat": 470,
    "Megan Thee Stallion": 470,
    "Ice Cube": 465,
    "Wu-Tang Clan": 465,
    "Snoop Dogg": 465,
    "Nas": 460,

    # R&B / Soul
    "Usher": 490,
    "Janet Jackson": 485,
    "Lionel Richie": 470,
    "Babyface": 470,
    "John Legend": 465,
    "Alicia Keys": 465,
    "Earth, Wind & Fire": 465,
    "Boyz II Men": 460,
    "New Edition": 460,

    # Alternative
    "The Killers": 480,
    "Death Cab for Cutie": 460,
    "Arcade Fire": 455,
    "The Black Keys": 455,
    "Kings of Leon": 455,
    "Vampire Weekend": 455,
    "The National": 450,
    "Cage The Elephant": 450,
    "The Lumineers": 465,
    "Mumford & Sons": 465,
    "My Morning Jacket": 445,

    # Christian
    "Chris Tomlin": 450,
    "for KING + COUNTRY": 450,
    "Casting Crowns": 445,
    "MercyMe": 445,
    "CeCe Winans": 445,

    # EDM
    "Calvin Harris": 470,
    "Martin Garrix": 465,
    "Marshmello": 465,
    "Tiësto": 465,
    "Deadmau5": 460,
    "Illenium": 460,
    "Zedd": 460,

    # Jazz / Blues
    "Buddy Guy": 455,
    "Wynton Marsalis": 450,
    "Trombone Shorty": 450,
    "Diana Krall": 445,
    "Robert Cray": 445,

    # Legacy
    "Elton John": 500,
    "Billy Joel": 490,
    "Stevie Nicks": 485,
    "Neil Young": 480,
    "Rod Stewart": 480,
    "Santana": 470,
    "Chicago": 465,
    "The Doobie Brothers": 465,
    "Foreigner": 460,
    "Heart": 460,
    "REO Speedwagon": 455,
    "Steve Miller Band": 455,
    "Styx": 455,
    "Toto": 450,
    "James Taylor": 470,
}


def artist_score(title):
    """
    Return the highest editorial score
    for any artist found in a concert title.
    """

    if not title:
        return 0

    title_lower = title.lower()

    best = 0

    for artist, score in ARTIST_RANKINGS.items():

        if artist.lower() in title_lower:

            if score > best:
                best = score

    return best


if __name__ == "__main__":

    tests = [

        "Bon Jovi: Forever Tour",
        "Taylor Swift | The Eras Tour",
        "Death Cab for Cutie: I Built You A Tower World Tour",
        "Polo Urias - La Integridad Nortena",
        "EMO NIGHT",
        "Morgan Wallen: I'm The Problem Tour",

    ]

    print()
    print("========================================")
    print("SHOWBIZ ARTIST RANKINGS")
    print("========================================")
    print()

    for title in tests:

        print(
            f"{artist_score(title):>4}  {title}"
        )