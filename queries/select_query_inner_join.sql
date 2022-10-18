use dbtest_join;	
select kopers.name,kopers.number,products.id,products.name,products.price from kopers
inner join products on kopers.product_id = products.id;