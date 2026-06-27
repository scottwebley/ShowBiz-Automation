import subprocess

pages = [
    ("2146", "content/home.html"),
    ("2129", "content/entertainment_news.html"),
    ("2134", "content/movies_and_streaming.html"),
    ("2136", "content/music_and_tours.html"),
    ("2138", "content/television.html"),
    ("2140", "content/style.html"),
]

for page_id, content_file in pages:
    print(f"\nUpdating Page {page_id}...")
    subprocess.run(
        ["python3", "update_page.py", page_id, content_file]
    )

print("\n✅ All pages updated.")
