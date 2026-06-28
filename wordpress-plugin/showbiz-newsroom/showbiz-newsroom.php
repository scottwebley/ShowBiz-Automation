<?php
/**
 * Plugin Name: ShowBiz Newsroom
 * Plugin URI: https://showbiz.com
 * Description: Dynamic newsroom components for ShowBiz.com.
 * Version: 1.1.0
 * Author: ShowBiz Enterprises
 */

if (!defined('ABSPATH')) {
    exit;
}

define('SHOWBIZ_NEWSROOM_VERSION', '1.1.0');
define('SHOWBIZ_NEWSROOM_PATH', plugin_dir_path(__FILE__));

require_once SHOWBIZ_NEWSROOM_PATH . 'includes/shortcode-winners.php';


/*
|--------------------------------------------------------------------------
| REST API
|--------------------------------------------------------------------------
|
| Allows the Python automation to update the homepage teaser.
|
*/

add_action('rest_api_init', function () {

    register_rest_route(
        'showbiz/v1',
        '/daily-report',
        array(
            'methods'  => 'POST',
            'callback' => 'showbiz_save_daily_report',
            'permission_callback' => function () {
                return current_user_can('edit_posts');
            }
        )
    );

});


function showbiz_save_daily_report(WP_REST_Request $request)
{
    $report = $request->get_json_params();

    if (!$report) {
        return new WP_Error(
            'invalid_report',
            'No report received.',
            array('status' => 400)
        );
    }

    update_option(
        'showbiz_daily_report',
        $report,
        false
    );

    return array(
        'success' => true
    );
}