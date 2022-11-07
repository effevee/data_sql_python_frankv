select kopers.name,kopers.number,products.id,products.name,products.price from kopers
left join products on kopers.product_id = products.id
union
select kopers.name,kopers.number,products.id,products.name,products.price from kopers
right join products on kopers.product_id = products.id