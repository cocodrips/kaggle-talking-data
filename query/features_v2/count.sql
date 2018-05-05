SELECT
  click_id,
  is_train,
  COUNT(1) OVER(PARTITION BY ip, day, hour) AS count_ip_day_hour,
  COUNT(1) OVER(PARTITION BY ip, app) AS count_ip_app,
  COUNT(1) OVER(PARTITION BY ip, app, os) AS count_ip_app_os
FROM
  `kaggle_views.features`