SELECT
  app,
  device,
  channel,
  os,
  next_click,
  prev_click,
  hour,
  day,
  clicks_by_ip,
  attributed_time,
  is_attributed
FROM
  `kaggle.prev_next_click`
WHERE
  is_train = 1