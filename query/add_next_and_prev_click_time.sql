SELECT
  ip,
  app,
  device,
  channel,
  os,
  click_time,
  --   next_click_time,
  TIMESTAMP_DIFF(next_click_time, click_time, SECOND) AS next_click,
  --   prev_click_time,
  TIMESTAMP_DIFF(click_time, prev_click_time, SECOND) AS prev_click,
  --   TIMESTAMP_DIFF(click_time, prev_click_time, HOUR) AS prev_click_hour,
  EXTRACT(HOUR
  FROM
    click_time) AS hour,
  EXTRACT (DAY
  FROM
    click_time) AS day,
  clicks_by_ip
FROM (
  SELECT
    ip,
    app,
    device,
    os,
    channel,
    click_time,
    LEAD(click_time, 1) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC) AS next_click_time,
    LAG(click_time, 1) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC) AS prev_click_time,
    COUNT(1) OVER(PARTITION BY ip, device, os, app) AS clicks_by_ip
  FROM
    `kaggle_views.merged` )