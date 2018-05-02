SELECT
  *
FROM (
  SELECT
    ip,
    app,
    device,
    os,
    channel,
    click_time
  FROM
    kaggle.train)
UNION ALL
SELECT
  ip,
  app,
  device,
  os,
  channel,
  click_time
FROM
  kaggle.test