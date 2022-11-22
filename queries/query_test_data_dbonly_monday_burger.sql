select * from status;

select * from category;

select * from supplier;

select pr_id,pr_name,ca_name,pr_limit from product,category where pr_categoryid=ca_id;

select * from customer;

select ca_name,pr_name,po_unitprice,po_salesfactor,po_taxfactor,po_stock,po_expiredate 
from product
left join purchase_order on po_id=pr_id 
left join category on ca_id=pr_categoryid
order by ca_name,pr_name;

select sa_id,cu_firstname,cu_lastname,st_name,sa_timestamp from sales_order,customer,status
where sa_customerid=cu_id and sa_statusid=st_id;

select sa_id,pro_id,sa_timestamp,cu_firstname,cu_lastname,ca_name,pr_name,pro_quantity,st_name
from sales_order
inner join product_order on sa_id=pro_sales_orderid
inner join customer on sa_customerid=cu_id
inner join status on sa_statusid=st_id
inner join product on pro_productid=pr_id
left join category on pr_categoryid=ca_id
order by sa_id,pro_id