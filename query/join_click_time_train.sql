SELECT
  train.ip,
  app,
  device,
  channel,
  os,
  train.click_time,
  next_click,
  prev_click,
  hour,
  day,
  attributed_time,
  is_attributed
FROM
  kaggle.train AS train
LEFT JOIN (
  SELECT
    ip,
    click_time,
    next_click,
    prev_click,
    hour,
    day
  FROM
    kaggle.prev_next_click ) AS click
ON
  ( train.ip = click.ip)
  AND ( train.click_time = click.click_time)

