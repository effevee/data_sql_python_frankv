use dbtest_join;	
select kopers.name,kopers.number,products.id,products.name,products.price from kopers
right join products on kopers.product_id = products.id;