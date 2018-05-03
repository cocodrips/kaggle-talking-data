SELECT
  click_id,
  app,
  device,
  channel,
  os,
  next_click,
  prev_click,
  hour,
  day,
  clicks_by_ip
FROM
  `kaggle.prev_next_click`
WHERE
  is_train = 0

