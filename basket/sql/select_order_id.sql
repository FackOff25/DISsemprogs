select max(order_id) as max_id
from user_orders
where user_id = '$user_id'