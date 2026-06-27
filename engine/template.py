def page_header(title):

    return f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{title}</title>

<style>

body {{
    font-family: Arial, Helvetica, sans-serif;
    background:#111;
    color:white;
    margin:0;
}}

header {{
    background:#d10000;
    padding:25px;
}}

.container {{
    width:90%;
    max-width:1200px;
    margin:auto;
}}

.story {{
    background:#1b1b1b;
    margin:20px 0;
    padding:20px;
    border-radius:10px;
}}

.story h2 {{
    color:#ffcc00;
}}

.story p {{
    line-height:1.6;
}}

</style>

</head>

<body>

<header>

<div class="container">

<h1>{title}</h1>

</div>

</header>

<div class="container">
"""
def page_footer():

    return """

</div>

</body>

</html>

"""