SELECT
  app_count,
  os_count,
  device_count,
  channel_count,
  next_1_ip_app_device_os_click,
  next_2_ip_app_device_os_click,
  prev_1_ip_app_device_os_click,
  prev_2_ip_app_device_os_click,
  next_1_ip_app_device_os_channel_click,
  next_2_ip_app_device_os_channel_click,
  prev_1_ip_app_device_os_channel_click,
  prev_2_ip_app_device_os_channel_click,
  next_1_ip_device_os_click,
  next_2_ip_device_os_click,
  prev_1_ip_device_os_click,
  prev_2_ip_device_os_click,
  clicks_ip_device_os_app,
  clicks_ip_device_os,
  clicks_ip_device_os_app_hour,
  clicks_ip_device_os_channel,
  day,
  hour_cos,
  hour_sin,
  attributed_time,
  is_attributed
FROM
  `kaggle_views.features`
WHERE
  is_train = 1
  AND (day=7
    OR day = 8)