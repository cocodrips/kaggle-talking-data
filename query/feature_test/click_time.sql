SELECT
  click_id,
  is_train,
  TIMESTAMP_DIFF(LEAD(click_time, 1) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC), click_time, SECOND) AS next_1_ip_app_device_os_click,
  TIMESTAMP_DIFF(LEAD(click_time, 2) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC), click_time, SECOND) AS next_2_ip_app_device_os_click,
  TIMESTAMP_DIFF(click_time, LAG(click_time, 1) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC), SECOND) AS prev_1_ip_app_device_os_click,
  TIMESTAMP_DIFF(click_time, LAG(click_time, 2) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC), SECOND) AS prev_2_ip_app_device_os_click,

  TIMESTAMP_DIFF(LEAD(click_time, 1) OVER(PARTITION BY ip, app, device, os, channel ORDER BY click_time ASC), click_time, SECOND) AS next_1_ip_app_device_os_channel_click,
  TIMESTAMP_DIFF(LEAD(click_time, 2) OVER(PARTITION BY ip, app, device, os, channel ORDER BY click_time ASC), click_time, SECOND) AS next_2_ip_app_device_os_channel_click,
  TIMESTAMP_DIFF(click_time, LAG(click_time, 1) OVER(PARTITION BY ip, app, device, os, channel ORDER BY click_time ASC), SECOND) AS prev_1_ip_app_device_os_channel_click,
  TIMESTAMP_DIFF(click_time, LAG(click_time, 2) OVER(PARTITION BY ip, app, device, os, channel ORDER BY click_time ASC), SECOND) AS prev_2_ip_app_device_os_channel_click,

  TIMESTAMP_DIFF(LEAD(click_time, 1) OVER(PARTITION BY ip, device, os ORDER BY click_time ASC), click_time, SECOND) AS next_1_ip_device_os_click,
  TIMESTAMP_DIFF(LEAD(click_time, 2) OVER(PARTITION BY ip, device, os ORDER BY click_time ASC), click_time, SECOND) AS next_2_ip_device_os_click,
  TIMESTAMP_DIFF(click_time, LAG(click_time, 1) OVER(PARTITION BY ip, device, os ORDER BY click_time ASC), SECOND) AS prev_1_ip_device_os_click,
  TIMESTAMP_DIFF(click_time, LAG(click_time, 2) OVER(PARTITION BY ip, device, os ORDER BY click_time ASC), SECOND) AS prev_2_ip_device_os_click


  FROM
  `kaggle_views.merged`