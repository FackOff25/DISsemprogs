select prod_name, prod_numb, prod_measure, prod_price
from product_report join product using(prod_id)
where in_month='$month' and in_year='$year';