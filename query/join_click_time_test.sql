SELECT
  test.click_id,
  app,
  device,
  channel,
  os,
  test.click_time,
  clicks_by_ip,
  next_click,
  prev_click,
  hour,
  day
FROM
  kaggle.test AS test
LEFT JOIN (
  SELECT
    ip,
    click_time,
    next_click,
    prev_click,
    clicks_by_ip,
    hour,
    day
  FROM
    kaggle.prev_next_click ) AS click
ON
  ( test.ip = click.ip)
  AND ( test.click_time = click.click_time)