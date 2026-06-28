<?php

if (!defined('ABSPATH')) {
    exit;
}

function showbiz_winners_shortcode() {

    $report = get_option('showbiz_daily_report');

    if (!$report || empty($report['winner'])) {
        return '
        <div class="showbiz-winners">
            <h2>🏆 ENTERTAINMENT WINNERS &amp; LOSERS OF THE DAY</h2>
            <p>Today\'s report is being prepared.</p>
        </div>';
    }

    // This matches YOUR JSON format
    $winner = $report['winner'] ?? '';
    $reason = $report['winner_reason'] ?? '';

    ob_start();
    ?>

    <div class="showbiz-winners">

        <h2>🏆 ENTERTAINMENT WINNERS &amp; LOSERS OF THE DAY</h2>

        <p>
            Every day ShowBiz.com highlights the biggest winners,
            losers and trends shaping today's entertainment industry.
        </p>

        <p>
            <strong>🏆 Winner:</strong>
            <?php echo esc_html($winner); ?>
        </p>

        <p>
            <?php echo esc_html($reason); ?>
        </p>

        <p>
            <a href="/entertainment-winners-losers/">
                <strong>Read Full Report →</strong>
            </a>
        </p>

    </div>

    <?php

    return ob_get_clean();
}

add_shortcode('showbiz_winners', 'showbiz_winners_shortcode');