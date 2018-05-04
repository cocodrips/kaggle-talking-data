SELECT
  click_id,
  is_train,
  --     COUNT(1) OVER(PARTITION BY ip, device, os, app) AS clicks_ip_device_os_app
  -- COUNT(1) OVER(PARTITION BY ip, device, os) AS clicks_ip_device_os,
  --     COUNT(1) OVER(PARTITION BY ip, device, os, app, EXTRACT(HOUR FROM click_time)) AS clicks_ip_device_os_app_hour
  COUNT(1) OVER(PARTITION BY ip, device, os, channel) AS clicks_ip_device_os_channel

FROM
  `kaggle_views.merged`

  --   COUNT(1) OVER(PARTITION BY app, channel) AS clicks_app_channel
  --     COUNT(1) OVER(PARTITION BY ip, device, os, app, channel) AS clicks_ip_device_os_app_channel,
