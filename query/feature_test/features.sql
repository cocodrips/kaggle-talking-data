SELECT
  is_train,
  -- default
  app,
  click_id,
  ip,
  device,
  os,
  channel,
  click_time,
  --  freq
  app_count,
  os_count,
  device_count,
  channel_count,
  -- click time
  TIMESTAMP_DIFF(LEAD(click_time, 1) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC), click_time, SECOND) AS next_1_ip_app_device_os_click,
  TIMESTAMP_DIFF(LEAD(click_time, 2) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC), click_time, SECOND) AS next_2_ip_app_device_os_click,
    TIMESTAMP_DIFF(LEAD(click_time, 3) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC), click_time, SECOND) AS next_3_ip_app_device_os_click,
  TIMESTAMP_DIFF(click_time, LAG(click_time, 1) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC), SECOND) AS prev_1_ip_app_device_os_click,
  TIMESTAMP_DIFF(click_time, LAG(click_time, 2) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC), SECOND) AS prev_2_ip_app_device_os_click,
    TIMESTAMP_DIFF(click_time, LAG(click_time, 3) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC), SECOND) AS prev_3_ip_app_device_os_click,
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
  -- ip
    COUNT(1) OVER(PARTITION BY ip, device, os, app) AS clicks_by_ip,
    COUNT(1) OVER(PARTITION BY ip, device, os) AS clicks_by_ip_non_app,
    COUNT(1) OVER(PARTITION BY ip, device, os, app, EXTRACT(HOUR FROM click_time)) AS clicks_by_ip_hour,
    ROW_NUMBER() OVER(PARTITION BY ip, device, os, app ORDER BY click_time ASC) AS clicks_by_ip_prev_day,
  -- y
  attributed_time,
  is_attributed
FROM
  `kaggle_views.merged` m
  LEFT JOIN (SELECT app as app_, count(1) as app_count  from `kaggle_views.merged` group by app) m1 ON m.app = m1.app_
  LEFT JOIN (SELECT device as device_, count(1) as device_count  from `kaggle_views.merged` group by device) m2 ON m.device = m2.device_
  LEFT JOIN (SELECT os as os_, count(1) as os_count  from `kaggle_views.merged` group by os) m3 ON m.os = m3.os_
  LEFT JOIN (SELECT channel as channel_, count(1) as channel_count  from `kaggle_views.merged` group by channel) m4 ON m.channel = m4.channel_