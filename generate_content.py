from datetime import datetime
from pathlib import Path

today = datetime.now().strftime("%B %d, %Y")

content_folder = Path("content")
content_folder.mkdir(exist_ok=True)

# HOME PAGE

home_html = f"""

<h1>ShowBiz.com</h1>

<div style="
background:linear-gradient(135deg,#1b1f4b,#163b6d);
padding:40px;
border-radius:20px;
margin-bottom:30px;">

<p style="
color:#ff66cc;
font-weight:bold;
letter-spacing:2px;">
SHOWBIZ.COM
</p>

<h1>Entertainment Portal</h1>

<p>
Your VIP pass to movies, television, music, streaming and celebrity culture.
</p>

<p>
<strong>Updated:</strong> {today}
</p>

</div>

<h2>🔥 Featured Story</h2>

<img src="https://showbiz.com/wp-content/uploads/2026/06/Image-scaled.jpg"
style="
width:100%;
height:350px;
object-fit:cover;
border-radius:12px;
margin-bottom:20px;">

<div style="border:1px solid #333;padding:20px;border-radius:12px;margin-bottom:20px;">
<h3>Current Biggest Entertainment Stories</h3>
<ul>
<li>Summer blockbuster season drives strong theater attendance</li>
<li>Major artists continue adding dates to global concert tours</li>
<li>Streaming platforms compete with high-profile original series</li>
<li>Television franchises expand across broadcast and streaming</li>
<li>Celebrity fashion trends dominate red carpet conversations</li>
</ul>
</div>

<div style="
display:flex;
flex-wrap:wrap;
gap:25px;
margin-top:30px;">

<div style="
flex:1 1 calc(50% - 25px);
min-width:300px;
box-sizing:border-box;
border:1px solid #333;
padding:20px;
border-radius:12px;">
<img src="https://showbiz.com/wp-content/uploads/2026/06/m2LtjUO8U9TINyQZTTrR7cmB7phHkP6PMEs4NI2czNWqKojXwAnq2H-Qpe2sK3agaeQFO4eOQ-pP0Xbc9IY4Q-Hk2WEXXrxSSJvPZpaBFYad2LqRgQa57Yr7qjAaHybOHOXczLTu2SCLgZTLDFL9gd2lvYrE4QACQ7wTNHtsfPykpRXvspjzh36ejyr7bnlP.jpeg"
style="width:100%;height:220px;object-fit:cover;border-radius:10px;margin-bottom:15px;">
<h3>🎬 Movies & Streaming</h3>
<p>Summer Movie Season Gains Momentum</p>
</div>

<div style="
flex:1 1 calc(50% - 25px);
min-width:300px;
box-sizing:border-box;
border:1px solid #333;
padding:20px;
border-radius:12px;">
<img src="https://showbiz.com/wp-content/uploads/2026/06/pE7oGzzNpvEUFNFn3qiadOL_-BPMTqIAo2asmGAewI5BFH18vkljFF5uHPIQQZRMza6kdO62fCNRNgmOrXvOCBLDs6S_ioLJGL-28qxB0-lLQZLbs9itU_U4heoXlWc7rgmHRNPvYY8Q6mGD3fwXuCDv6Q9Vd6MRuG0xqA9pAllPe_8DB3QtEPvbFE-Hdkzo-scaled.jpeg"
style="width:100%;height:220px;object-fit:cover;border-radius:10px;margin-bottom:15px;">
<h3>🎵 Music & Tours</h3>
<p>Concert Demand Remains Strong</p>
</div>

<div style="
flex:1 1 calc(50% - 25px);
min-width:300px;
box-sizing:border-box;
border:1px solid #333;
padding:20px;
border-radius:12px;">
<img src="https://showbiz.com/wp-content/uploads/2026/06/4L1vnkD0SvnuDyWwkQtFXd6BwMuRqC50UQ3Bd6OI0gD-NckuZUjVXL9QTQ-U9jBpvnQGvfZHJ7RsC6SIDe_YPsJniInB-Lrpw0sA68wYKbDCRzhLNAhr-Ih-ZjQjgR9_g2PtLtWz7O3A5yRK4S9pekfgjIQQfRsjZAcaKGtQ9prpR8Q0f9MIiHe4TNqo7tJM.jpeg"
style="width:100%;height:220px;object-fit:cover;border-radius:10px;margin-bottom:15px;">
<h3>📺 Television</h3>
<p>Television Franchises Continue Expanding</p>
</div>

<div style="
flex:1 1 calc(50% - 25px);
min-width:300px;
box-sizing:border-box;
border:1px solid #333;
padding:20px;
border-radius:12px;">
<img src="https://showbiz.com/wp-content/uploads/2026/06/cl9FOE1BMXoLrc1fgqEbpSZWis_G5iBlc9If0yKVCZftL94LL3K3LOJhDUVdHMKqBZOQMuuLPMIDxZ7hJwlDYSqbSSjJ3oj4nim5rOdQOPus3JbE4HDRYDXhdk9zYUeN69_eUHt8GqkeYGvKEci_3gdCWzaHDZhPAeo6bj7cahiwBCybvvAe_42wBny9KQz4.jpeg"
style="width:100%;height:220px;object-fit:cover;border-radius:10px;margin-bottom:15px;">
<h3>✨ Style</h3>
<p>Red Carpet Fashion Trends</p>
</div>

</div>
"""

# ENTERTAINMENT NEWS

entertainment_news_html = f"""

<h1>Entertainment News Today</h1>

<p><strong>Updated:</strong> {today}</p>

<h2>🔥 Featured Story</h2>

<img src="https://showbiz.com/wp-content/uploads/2026/06/Image-scaled.jpg"
style="
width:100%;
height:350px;
object-fit:cover;
border-radius:12px;
margin-bottom:20px;">

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
