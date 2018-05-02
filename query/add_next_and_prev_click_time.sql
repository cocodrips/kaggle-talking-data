SELECT
  ip,
  app,
  device,
  os,
  click_time,
  LEAD(click_time, 1) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC) AS prev_click_time,
  LAG(click_time, 1) OVER(PARTITION BY ip, app, device, os ORDER BY click_time ASC) AS next_click_time
FROM
  kaggle.train
