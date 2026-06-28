<?php

if (!defined('ABSPATH')) {
    exit;
}

function showbiz_winners_shortcode() {

    $html = '
    <div class="showbiz-winners">

        <h2>🏆 ENTERTAINMENT WINNERS &amp; LOSERS OF THE DAY</h2>

        <p>
        Every day ShowBiz.com highlights the biggest winners, losers
        and trends shaping today\'s entertainment industry.
        </p>

        <p>
        <strong>🏆 Winner:</strong> Christopher Nolan
        </p>

        <p>
        The announcement of his next film became today\'s biggest
        entertainment story.
        </p>

        <p>
            <a href="/entertainment-winners-losers/">
                <strong>Read Full Report →</strong>
            </a>
        </p>

    </div>';

    return $html;
}

add_shortcode('showbiz_winners', 'showbiz_winners_shortcode');