SELECT
  is_train,
  click_id,
  ip,
  app,
  device,
  channel,
  os,
  click_time,
  TIMESTAMP_DIFF(next_click_time, click_time, SECOND) AS next_click,
  TIMESTAMP_DIFF(click_time, prev_click_time, SECOND) AS prev_click,
  EXTRACT(HOUR
  FROM
    click_time) AS hour,
  EXTRACT (DAY
  FROM
    click_time) AS day,
  clicks_by_ip,
  attributed_time,
  is_attributed
FROM (
  SELECT
    is_train,
    click_id,
    ip,
    app,
    device,
    os,
    channel,
    click_time,
    LEAD(click_time, 1) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC) AS next_click_time,
    LAG(click_time, 1) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC) AS prev_click_time,
    COUNT(1) OVER(PARTITION BY ip, device, os, app) AS clicks_by_ip,
    attributed_time,
    is_attributed
  FROM
    `kaggle_views.merged` )