  -- SELECT
  --   app,
  --   COUNT(1) AS app_count
  -- FROM
  --   `kaggle_views.merged`
  -- GROUP BY
  --   app
  -- SELECT
  --   device,
  --   COUNT(1) AS device_count
  -- FROM
  --   `kaggle_views.merged`
  -- GROUP BY
  --   device
  -- ORDER BY
  --   device_count
  -- SELECT
  --   os,
  --   COUNT(1) AS os_count
  -- FROM
  --   `kaggle_views.merged`
  -- GROUP BY
  --   os
  -- ORDER BY
  --   os_count DESC
SELECT
  channel,
  COUNT(1) AS channel_count
FROM
  `kaggle_views.merged`
GROUP BY
  channel
ORDER BY
  channel_count DESC channel, channel