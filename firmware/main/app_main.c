/*
 * SPDX-FileCopyrightText: 2026 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdio.h>
#include <inttypes.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "nvs_flash.h"
#include "esp_err.h"
#include "esp_log.h"
#include "esp_mac.h"
#include "esp_wifi.h"
#include "esp_netif.h"
#include "esp_event.h"

#include "esp_wifi_sensing.h"

#include "protocol_examples_common.h"
#include "led_control.h"
#include "web_serial_monitor.h"

static const char *TAG = "wifi_sensing_demo";
static esp_wifi_sensing_fsm_handle_t s_hms = NULL;
static uint8_t s_mac_ap[6] = {0};

static void wifi_event_handler(void *arg, esp_event_base_t event_base, int32_t event_id, void *event_data)
{
    (void)arg;
    (void)event_data;

    if (event_base == WIFI_EVENT) {
        if (event_id == WIFI_EVENT_STA_CONNECTED) {
            led_set_wifi_connected(true);
        } else if (event_id == WIFI_EVENT_STA_DISCONNECTED) {
            led_set_wifi_connected(false);
        }
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        led_set_wifi_connected(true);
    }
}

static void on_motion_event(esp_wifi_sensing_fsm_handle_t handle,
                            const uint8_t peer_mac[6],
                            esp_wifi_sensing_fsm_event_t event,
                            uint32_t data,
                            void *usr_data)
{
    (void)handle;
    (void)usr_data;
    bool is_ap_channel = (memcmp(peer_mac, s_mac_ap, 6) == 0);
    if (!is_ap_channel) {
        return;
    }
    if (event == ESP_WIFI_SENSING_FSM_EVENT_ACTIVE) {
        led_notify_ap_active();
        ESP_LOGI(TAG, "[%s] ACTIVE peer=" MACSTR " data=%" PRIu32,
                 "AP", MAC2STR(peer_mac), data);
    } else if (event == ESP_WIFI_SENSING_FSM_EVENT_INACTIVE) {
        led_notify_ap_inactive();
        ESP_LOGI(TAG, "[%s] INACTIVE peer=" MACSTR,
                 "AP", MAC2STR(peer_mac));
    }
}

static void demo_init(void)
{
    /*
     * Follow the public component workflow:
     * 1. Resolve the connected AP.
     * 2. Create one FSM handle.
     * 3. Add the AP channel only.
     * 4. Register ACTIVE / INACTIVE callbacks.
     * 5. Start the FSM and optionally enable router-ping-assisted sampling.
     */
    wifi_ap_record_t ap_info = {0};
    ESP_ERROR_CHECK(esp_wifi_sta_get_ap_info(&ap_info));
    memcpy(s_mac_ap, ap_info.bssid, 6);
    ESP_LOGI(TAG, "peer mac (AP BSSID): " MACSTR, MAC2STR(ap_info.bssid));

    esp_wifi_sensing_fsm_config_t cfg = DEFAULT_ESP_WIFI_SENSING_FSM_CONFIG();
    cfg.max_channel_num = 1;

    ESP_ERROR_CHECK(esp_wifi_sensing_fsm_create(&cfg, &s_hms));

    /* Motion events must originate from the connected AP channel only. */
    ESP_ERROR_CHECK(esp_wifi_sensing_fsm_add_channel(s_hms, ap_info.bssid));

    /* Register the same callback for both state transitions to keep logging symmetric. */
    ESP_ERROR_CHECK(esp_wifi_sensing_fsm_register_event_cb(s_hms, ESP_WIFI_SENSING_FSM_EVENT_ACTIVE, on_motion_event, NULL));
    ESP_ERROR_CHECK(esp_wifi_sensing_fsm_register_event_cb(s_hms, ESP_WIFI_SENSING_FSM_EVENT_INACTIVE, on_motion_event, NULL));
    ESP_ERROR_CHECK(esp_wifi_sensing_fsm_control(s_hms, ESP_WIFI_SENSING_FSM_CTRL_START, NULL));

    ESP_LOGI(TAG,
             "default config: motion_detection_sensitivity=%.3f active_jitter_min=%.3f hold=%" PRIu32 "ms confirm=%d ping=%" PRIu32 "Hz",
             cfg.default_channel_config.sensitivity,
             cfg.default_channel_config.active_jitter_min,
             cfg.default_channel_config.active_filter_ms,
             CONFIG_ESP_WIFI_SENSING_CONFIRM_COUNT,
             cfg.ping_frequency_hz);

    esp_err_t ping_err = esp_wifi_sensing_fsm_ping_router_start(s_hms);
    if (ping_err == ESP_OK) {
        ESP_LOGI(TAG, "router ping started");
    } else if (ping_err == ESP_ERR_INVALID_STATE) {
        ESP_LOGW(TAG, "router ping start failed: Wi-Fi STA not connected or no gateway");
    } else {
        ESP_LOGE(TAG, "router ping start failed: %s", esp_err_to_name(ping_err));
    }
}

void app_main(void)
{
    /* Standard ESP-IDF bring-up followed by Wi-Fi connection and sensing start. */
    ESP_ERROR_CHECK(nvs_flash_init());
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    ESP_ERROR_CHECK(led_init());
    ESP_ERROR_CHECK(esp_event_handler_register(WIFI_EVENT, WIFI_EVENT_STA_CONNECTED, wifi_event_handler, NULL));
    ESP_ERROR_CHECK(esp_event_handler_register(WIFI_EVENT, WIFI_EVENT_STA_DISCONNECTED, wifi_event_handler, NULL));
    ESP_ERROR_CHECK(esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, wifi_event_handler, NULL));
    led_set_wifi_connected(false);
    ESP_ERROR_CHECK(example_connect());
    /* Disable Wi-Fi power save to keep CSI sampling cadence stable. */
    ESP_ERROR_CHECK(esp_wifi_set_ps(WIFI_PS_NONE));
    demo_init();

#if CONFIG_ESP_WIFI_SENSING_WEB_SERIAL_ENABLE
    /* Web UI also maps esp-radar train (TRAIN_START/STOP/REMOVE) and streams wander / train thresholds. */
    /* Export only the AP channel to the browser monitor UI. */
    web_serial_monitor_peer_t serial_peers[] = {
        { .name = "AP" },
    };
    memcpy(serial_peers[0].mac, s_mac_ap, sizeof(s_mac_ap));
    web_serial_monitor_config_t serial_cfg = {
        .fsm = s_hms,
        .peers = serial_peers,
        .peer_num = sizeof(serial_peers) / sizeof(serial_peers[0]),
        .stream_period_ms = CONFIG_ESP_WIFI_SENSING_WEB_SERIAL_STREAM_PERIOD_MS,
    };
    ESP_ERROR_CHECK(web_serial_monitor_init(&serial_cfg));
#endif

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
