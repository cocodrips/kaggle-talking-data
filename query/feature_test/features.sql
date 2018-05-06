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
  -- clicks
  next_1_ip_device_os_click, next_1_ip_app_device_os_click, next_1_ip_app_device_os_channel_click, prev_1_ip_channel_click, prev_1_ip_os_click,
  -- count
  count_ip_day_hour, count_ip_app, count_ip_app_os,
  -- count unique
  app_by_ip
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
LEFT JOIN `features_v2.clicks` clicks ON (clicks.click_id = m.click_id AND clicks.click_id = m.is_train)
LEFT JOIN `features_v2.count` c ON (c.click_id = m.click_id AND c.click_id = m.is_train)
LEFT JOIN `features_v2.count_app_by_ip` count_app_by_ip ON (count_app_by_ip.app = m.app)
LEFT JOIN `features_v2.count_app_by_ip_device_os` count_app_by_ip_device_os ON (count_app_by_ip_device_os.app = m.app)
LEFT JOIN `features_v2.count_channel_by_app` count_channel_by_app ON (count_channel_by_app.channel = m.channel)

LEFT JOIN `features_v2.count_channel_by_ip` count_channel_by_ip ON (count_channel_by_app.ip = m.ip)
LEFT JOIN `features_v2.count_channel_by_app` count_channel_by_app ON (count_channel_by_app.channel = m.channel)
LEFT JOIN `features_v2.count_channel_by_app` count_channel_by_app ON (count_channel_by_app.channel = m.channel)
