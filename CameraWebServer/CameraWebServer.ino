#include "esp_camera.h"
#include <WiFi.h>

// ------------------  SELECT YOUR BOARD  ------------------
#define CAMERA_MODEL_AI_THINKER          // << change if you use ESP_EYE, WROVER_KIT, etc.
// ---------------------------------------------------------
#include "camera_pins.h"

// ------------------  WIFI CREDENTIALS  -------------------
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
// ---------------------------------------------------------

void startCameraServer();
void setupLedFlash(int pin);

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  // --------  CAMERA CONFIG  --------
  camera_config_t config;
  config.ledc_channel   = LEDC_CHANNEL_0;
  config.ledc_timer     = LEDC_TIMER_0;
  config.pin_d0         = Y2_GPIO_NUM;
  config.pin_d1         = Y3_GPIO_NUM;
  config.pin_d2         = Y4_GPIO_NUM;
  config.pin_d3         = Y5_GPIO_NUM;
  config.pin_d4         = Y6_GPIO_NUM;
  config.pin_d5         = Y7_GPIO_NUM;
  config.pin_d6         = Y8_GPIO_NUM;
  config.pin_d7         = Y9_GPIO_NUM;
  config.pin_xclk       = XCLK_GPIO_NUM;
  config.pin_pclk       = PCLK_GPIO_NUM;
  config.pin_vsync      = VSYNC_GPIO_NUM;
  config.pin_href       = HREF_GPIO_NUM;
  config.pin_sccb_sda   = SIOD_GPIO_NUM;
  config.pin_sccb_scl   = SIOC_GPIO_NUM;
  config.pin_pwdn       = PWDN_GPIO_NUM;
  config.pin_reset      = RESET_GPIO_NUM;
  config.xclk_freq_hz   = 20000000;
  config.pixel_format   = PIXFORMAT_JPEG;
  config.frame_size     = FRAMESIZE_QVGA;      // 320 × 240  → smooth FPS
  config.jpeg_quality   = 12;                  // 0‑63 (lower = better)
  config.fb_count       = 2;                   // two frame‑buffers
  config.fb_location    = CAMERA_FB_IN_PSRAM;  // store FB in PSRAM
  config.grab_mode      = CAMERA_GRAB_LATEST;
  // ----------------------------------

  // Init camera
  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("❌ Camera init failed");
    while (true) delay(1000);
  }

  sensor_t* s = esp_camera_sensor_get();
  if (s->id.PID == OV3660_PID) {   // ESP‑EYE quirks
    s->set_vflip(s, 1);
    s->set_brightness(s, 1);
    s->set_saturation(s, -2);
  }

#if defined(LED_GPIO_NUM)
  setupLedFlash(LED_GPIO_NUM);
#endif

  // Wi‑Fi
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);
  Serial.print("Connecting WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
  }
  Serial.println("\n✅ WiFi connected");

  // Start web server (provides / and /stream)
  startCameraServer();

  Serial.print("🔗 Control page:  http://");
  Serial.println(WiFi.localIP());
  Serial.print("📹 MJPEG stream:  http://");
  Serial.print(WiFi.localIP()); Serial.println(":81/stream");
}

void loop() {
  delay(10000);   // everything handled by web‑server task
}
