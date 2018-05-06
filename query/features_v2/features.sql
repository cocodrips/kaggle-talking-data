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
  m.attributed_time,
  m.is_attributed,
  m.hour,
  m.day,
  m.hour_cos,
  m.hour_sin,
  -- clicks
  clicks.next_1_ip_device_os_click,
  clicks.next_1_ip_app_device_os_click,
  clicks.next_1_ip_app_device_os_channel_click,
  clicks.prev_1_ip_channel_click,
  clicks.prev_1_ip_os_click,
  -- count
  count_by_ip.f0_ as count_by_ip,
  clicks_ip_device_os_app as count_by_device_os_app,
  clicks_ip_device_os as count_by_device_os,
  count_ip_day_hour,
  count_ip_app,
  count_ip_app_os,
  -- count unique
  app_by_ip,
  app_by_ip_device_ps,
  channel_by_app,
  channel_by_ip,
  device_by_ip,
  hour_by_ip_day,
  os_by_ip_app,
  -- cum_count
  cumcount_by_ip,
  cumcount_by_ip_device_os
FROM
  `kaggle_views.features` m
  LEFT JOIN `features_v2.clicks` clicks ON (clicks.click_id = m.click_id AND clicks.is_train = m.is_train)
  LEFT JOIN `features_v2.count` c ON (c.click_id = m.click_id AND c.is_train = m.is_train)
  LEFT JOIN `features_v2.count_by_ip` count_by_ip ON (count_by_ip.ip = m.ip)
  LEFT JOIN `features_v2.count_app_by_ip` count_app_by_ip ON (count_app_by_ip.app = m.app)
  LEFT JOIN `features_v2.count_app_by_ip_device_os` count_app_by_ip_device_os ON (count_app_by_ip_device_os.app = m.app)
  LEFT JOIN `features_v2.count_channel_by_app` count_channel_by_app ON (count_channel_by_app.channel = m.channel)
  LEFT JOIN `features_v2.count_channel_by_ip` count_channel_by_ip ON (count_channel_by_ip.channel = m.channel)
  LEFT JOIN `features_v2.count_device_by_ip` count_device_by_ip ON (count_device_by_ip.device = m.device)
  LEFT JOIN `features_v2.count_hour_by_ip_day` count_hour_by_ip_day ON (count_hour_by_ip_day.hour = m.hour)
  LEFT JOIN `features_v2.count_os_by_ip_app` count_os_by_ip_app ON (count_os_by_ip_app.os = m.os)
  LEFT JOIN `features_v2.cumcount` cumcount ON (cumcount.click_id = m.click_id AND cumcount.is_train = m.is_train)