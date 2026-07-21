"""
===========================================
ShowBiz Guide CSS
Version 3.3
===========================================

Shared CSS used by all ShowBiz Guides.

Author:
    ShowBiz Automation
"""

GUIDE_CSS = """
<style>

.showbiz-guide{
    max-width:1100px;
    margin:0 auto;
    padding:30px;
    line-height:1.8;
}


.showbiz-updated{
    color:#8d8d8d;
    font-size:14px;
    margin-bottom:40px;
}


/*
===========================================
Global Images
===========================================
*/

.showbiz-guide img{
    max-width:180px;
    height:auto;
}


/*
===========================================
Headings
===========================================
*/

.showbiz-guide h2{

    color:#ff4fc4;

    font-size:30px;

    margin-top:55px;

    margin-bottom:35px;

    padding-bottom:12px;

    border-bottom:2px solid rgba(255,79,196,.30);

}


.showbiz-guide h3{

    font-size:26px;

    margin:0 0 20px;

}


.showbiz-guide p{

    margin-bottom:18px;

}


/*
===========================================
Movie Card Component
===========================================
*/

.showbiz-movie-card{

    display:flex;

    align-items:flex-start;

    gap:25px;

    margin:35px 0;

    padding:25px;

    border-radius:18px;

    border:1px solid rgba(255,255,255,.15);

    background:rgba(255,255,255,.04);

}


.showbiz-movie-poster{

    flex:0 0 180px;

}


.showbiz-movie-poster img{

    display:block;

    width:180px;

    height:auto;

    border-radius:12px;

    box-shadow:0 10px 24px rgba(0,0,0,.30);

}


.showbiz-movie-info{

    flex:1;

    max-width:none;

}


.showbiz-movie-content p{

    margin-bottom:18px;

}


.showbiz-movie-trailer{

    margin-top:20px;

}


/*
===========================================
Movie Divider
===========================================
*/

.showbiz-movie-divider{

    height:1px;

    margin:40px 0;

    background:rgba(255,255,255,.10);

}


/*
===========================================
Buttons
===========================================
*/

.showbiz-trailer-button,
.showbiz-ticket-button{

    display:inline-block;

    margin-top:15px;

    padding:12px 22px;

    background:#ff4fc4;

    color:#fff;

    text-decoration:none;

    font-weight:700;

    border-radius:8px;

}

.showbiz-trailer-button:hover,
.showbiz-ticket-button:hover{

    opacity:.90;

}

.showbiz-ticket-buttons{

    margin-top:18px;

}


/*
===========================================
Editor's Pick
===========================================
*/

.showbiz-editors-pick{

    display:inline-block;

    padding:8px 16px;

    border-radius:999px;

    background:#ff4fc4;

    color:#fff;

    font-weight:700;

    margin-bottom:30px;

}


/*
===========================================
Mobile
===========================================
*/

@media (max-width:768px){

    .showbiz-guide{

        padding:20px;

    }


    .showbiz-movie-card{

        display:block;

        padding:25px;

    }


    .showbiz-movie-poster{

        margin-bottom:30px;

    }


    .showbiz-movie-poster img{

        width:180px;

    }


    .showbiz-guide h2{

        font-size:26px;

    }


    .showbiz-guide h3{

        font-size:24px;

    }

}

</style>
"""