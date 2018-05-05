SELECT
  click_id,
  is_train,
  ROW_NUMBER() OVER(PARTITION BY ip ORDER BY click_time ) AS cumcount_by_ip,
  ROW_NUMBER() OVER(PARTITION BY ip, device, os ORDER BY click_time ) AS cumcount_by_ip_device_os
FROM
  `kaggle_views.merged`