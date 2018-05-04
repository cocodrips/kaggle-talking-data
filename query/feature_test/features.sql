SELECT
  m.is_train,
  -- default
  m.app,
  m.click_id,
  m.ip,
  m.device,
  m.os,
  m.channel,
  m.click_time,
  --  freq
  app_count,
  os_count,
  device_count,
  channel_count,
  -- click time
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
  -- time
  EXTRACT(HOUR
  FROM
    click_time) AS hour,
  EXTRACT (DAY
  FROM
    click_time) AS day,
  CAST((COS(EXTRACT(HOUR
        FROM
          click_time) / 24 * (2*ACOS(-1))) * 100) AS INT64) AS hour_cos,
  CAST((SIN(EXTRACT(HOUR
        FROM
          click_time) / 24 * (2*ACOS(-1))) * 100) AS INT64) AS hour_sin,
  --attribute
  attributed_time,
  is_attributed
FROM
  `kaggle_views.merged` m
LEFT JOIN
  `kaggle_views.app_count` c1
ON
  c1.app = m.app
LEFT JOIN
  `kaggle_views.os_count` c2
ON
  c2.os = m.os
LEFT JOIN
  `kaggle_views.device_count` c3
ON
  c3.device = m.device
LEFT JOIN
  `kaggle_views.channel_count` c4
ON
  c4.channel = m.channel
LEFT JOIN
  `kaggle_views.clicks_ip_device_is_app` click1
ON
  (click1.click_id = m.click_id
    AND click1.is_train = m.is_train)
LEFT JOIN
  `kaggle_views.clicks_ip_device_os_app2` click2
ON
  (click2.click_id = m.click_id
    AND click2.is_train = m.is_train)
LEFT JOIN
  `kaggle_views.clicks_ip_device_os_channel` click3
ON
  (click3.click_id = m.click_id
    AND click3.is_train = m.is_train)
LEFT JOIN
  `kaggle_views.click_time_lag` timelag
ON
  (timelag.click_id = m.click_id
    AND timelag.is_train = m.is_train)