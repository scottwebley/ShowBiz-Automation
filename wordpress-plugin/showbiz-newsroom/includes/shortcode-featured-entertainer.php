<?php

if (!defined('ABSPATH')) {
    exit;
}

function showbiz_featured_entertainer_shortcode()
{
    $featured = get_option('showbiz_featured_entertainer');

    if (!$featured || empty($featured['name'])) {
        return '
        <div class="showbiz-featured-entertainer">
            <h2>⭐ FEATURED ENTERTAINER OF THE WEEK</h2>
            <p>This week\'s Featured Entertainer is being prepared.</p>
        </div>';
    }

    $name = $featured['name'] ?? '';
    $headline = $featured['headline'] ?? '';
    $url = $featured['url'] ?? '#';

    ob_start();
    ?>

    <div class="showbiz-featured-entertainer">

        <h2>⭐ FEATURED ENTERTAINER OF THE WEEK</h2>

        <p>
            <strong>
                <a href="<?php echo esc_url($url); ?>">
                    <?php echo esc_html(strtoupper($name)); ?>
                </a>
            </strong>
        </p>

        <p>
            <?php echo esc_html($headline); ?>
        </p>

        <p>
            <a href="<?php echo esc_url($url); ?>">
                <strong>Learn More →</strong>
            </a>
        </p>

    </div>

    <?php

    return ob_get_clean();
}

add_shortcode(
    'showbiz_featured_entertainer',
    'showbiz_featured_entertainer_shortcode'
);