select user_id, NULL as user_group
from external_user
where login = '$login'
  and password = '$password'