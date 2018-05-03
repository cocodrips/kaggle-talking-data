SELECT
  *
FROM (
  SELECT
    1 AS is_train,
    NULL AS click_id,
    ip,
    app,
    device,
    os,
    channel,
    click_time,
    attributed_time,
    is_attributed
  FROM
    kaggle.train)
UNION ALL
SELECT
  0 AS is_train,
  click_id,
  ip,
  app,
  device,
  os,
  channel,
  click_time,
  NULL AS attributed_time,
  NULL AS is_attributed
FROM
  kaggle.test