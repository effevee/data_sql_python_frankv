use dbtest_join;	
select kopers.name,kopers.number,products.id,products.name,products.price from kopers
left join products on kopers.product_id = products.id;