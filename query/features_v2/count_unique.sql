-- Example
SELECT
  channel,
  COUNT(1) AS channel_by_ip
FROM (
  SELECT
    DISTINCT ip,
    channel
  FROM
    `kaggle_views.merged`
  GROUP BY
    ip,
    channel)
GROUP BY
  channel