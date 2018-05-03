SELECT
  app_count,
  os_count,
  device_count,
  channel_count next_1_ip_app_device_os_click,
  next_2_ip_app_device_os_click,
  next_3_ip_app_device_os_click,
  prev_1_ip_app_device_os_click,
  prev_2_ip_app_device_os_click,
  prev_3_ip_app_device_os_click,
  hour_cos,
  hour_sin,
  clicks_by_ip,
  clicks_by_ip_non_app,
  clicks_by_ip_hour,
  clicks_by_ip_prev_day,
  attributed_time,
  is_attributed
FROM
  `kaggle.features`
WHERE
  is_train = 1
  AND day = 9