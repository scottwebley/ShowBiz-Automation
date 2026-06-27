from datetime import datetime
from pathlib import Path

today = datetime.now().strftime("%B %d, %Y")

content_folder = Path("content")
content_folder.mkdir(exist_ok=True)

# HOME PAGE

home_html = f"""
<h1>ShowBiz.com</h1>

<h2>🎬 Current Biggest Entertainment Stories</h2>
<p>Your VIP pass to movies, TV, music, gaming and celebrity culture.</p>

<h2>🔥 Breaking News</h2>
<p>Major entertainment developments happening right now.</p>

<h2>🎬 Movies & Streaming</h2>
<p>Current movie recommendations and streaming highlights.</p>

<h2>🎵 Music & Tours</h2>
<p>Latest concert announcements and music industry news.</p>

<h2>📺 Television</h2>
<p>Trending television stories and streaming series updates.</p>

<h2>✨ Style</h2>
<p>Celebrity fashion, red carpet looks and style trends.</p>
"""

# ENTERTAINMENT NEWS

entertainment_news_html = f"""
<h1>Entertainment News Today</h1>

<p><strong>Updated:</strong> {today}</p>

<h2>🔥 Featured Story</h2>
<p>Major Streaming Platforms Continue Content Expansion</p>

<h2>🎬 Movies & Streaming</h2>
<p>Summer Movie Season Gains Momentum</p>

<h2>🎵 Music & Tours</h2>
<p>Concert Tours Drive Strong Ticket Demand</p>

<h2>📺 Television</h2>
<p>Television Franchises Expand Across Platforms</p>
"""

# MOVIES & STREAMING

movies_and_streaming_html = f"""
<h1>Movies & Streaming</h1>

<p><strong>Updated:</strong> {today}</p>

<h2>🎬 Box Office</h2>
<p>Major releases continue drawing audiences worldwide.</p>

<h2>🍿 Streaming</h2>
<p>New original content remains a major driver of subscriptions.</p>

<h2>⭐ Trending</h2>
<p>Fans continue discussing the biggest movie and streaming hits.</p>
"""

# MUSIC & TOURS

music_and_tours_html = f"""
<h1>Music & Tours</h1>

<p><strong>Updated:</strong> {today}</p>

<h2>🎵 Concert Tours</h2>
<p>Major artists continue adding tour dates worldwide.</p>

<h2>🎤 Live Shows</h2>
<p>Fans are returning to arenas, theaters and festivals.</p>

<h2>🎫 Ticket Demand</h2>
<p>Strong demand continues for top touring acts.</p>
"""

# TELEVISION

television_html = f"""
<h1>Television</h1>

<p><strong>Updated:</strong> {today}</p>

<h2>📺 Trending Series</h2>
<p>New series continue attracting viewers across platforms.</p>

<h2>🏆 Awards Buzz</h2>
<p>Industry attention focuses on standout performances.</p>

<h2>🔥 Fan Favorites</h2>
<p>Popular franchises remain strong audience draws.</p>
"""

# STYLE

style_html = f"""
<h1>Style</h1>

<p><strong>Updated:</strong> {today}</p>

<h2>✨ Red Carpet</h2>
<p>Celebrity fashion continues generating headlines.</p>

<h2>👗 Fashion Trends</h2>
<p>Designers showcase upcoming looks and collections.</p>

<h2>📸 Celebrity Style</h2>
<p>Stars influence current fashion and lifestyle trends.</p>
"""

# WRITE FILES

(content_folder / "home.html").write_text(home_html, encoding="utf-8")
(content_folder / "entertainment_news.html").write_text(entertainment_news_html, encoding="utf-8")
(content_folder / "movies_and_streaming.html").write_text(movies_and_streaming_html, encoding="utf-8")
(content_folder / "music_and_tours.html").write_text(music_and_tours_html, encoding="utf-8")
(content_folder / "television.html").write_text(television_html, encoding="utf-8")
(content_folder / "style.html").write_text(style_html, encoding="utf-8")

print("✅ Home page generated")
print("✅ Entertainment News generated")
print("✅ Movies & Streaming generated")
print("✅ Music & Tours generated")
print("✅ Television generated")
print("✅ Style generated")