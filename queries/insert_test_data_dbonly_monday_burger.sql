insert into category(ca_name) values('Food'),('Drinks'),('Sauces');

insert into supplier(su_firstname,su_lastname,su_email,su_address) values
('Frans','Wurst','frans.wurst@dbb.de','Die Bessere Burger, Koelnstrasse 444, Hamburg, Duitsland'),
('Altijd','Dorst','drankcentrale@altijddorst.be','Drankencentrale Altijd Dorst, Oudenaardsesteenweg 88, Berchem, Belgie'),
('Jan','Peeters','jan.peeters@saus.peeters.be','Sauzen Peeters, Kustlaan 23, Oostende, Belgie');

insert into product(pr_name,pr_categoryid,pr_limit) values
('Burger Gezond',1,80),
('Burger De Grote Honger',1,60),
('Cola',2,40),
('Cola Zero',2,40),
('Fanta',2,40),
('Water',2,40),
('Spuitwater',2,40),
('Jupiler',2,40),
('Ketchup',3,60),
('Mayonaise',3,60),
('BBQ saus',3,60),
('Tartaar saus',3,60);

insert into customer(cu_firstname,cu_lastname,cu_email,cu_address,cu_birthdate) values
('Jan','Met De Pet','jan.mdp@hotmail.com','Markt 2, Kruisem', '1985-01-08'),
('Ann','Koffiekan','ann.koffie@gmail.com','Karreweg 44, Kruisem', '1978-05-08');

insert into purchase_order(po_date,po_quantity,po_supplierid,po_unitprice,po_salesfactor,po_taxfactor,
po_productid,po_expiredate,po_stock) values
(now(),400,1,4.00,2,1.12,1,'2023-12-12',400),
(now(),300,1,7.99,2,1.12,2,'2023-12-12',300),
(now(),500,2,0.25,8,1.21,3,'2023-12-12',500),
(now(),500,2,0.25,8,1.21,4,'2023-12-12',500),
(now(),500,2,0.25,8,1.21,5,'2023-12-12',500),
(now(),500,2,0.15,8,1.21,6,'2023-12-12',500),
(now(),500,2,0.20,8,1.21,7,'2023-12-12',500),
(now(),500,2,0.30,8,1.21,8,'2023-12-12',500),
(now(),400,3,0.05,12,1.12,9,'2023-12-12',400),
(now(),400,3,0.05,12,1.12,10,'2023-12-12',400),
(now(),400,3,0.05,12,1.12,11,'2023-12-12',400),
(now(),400,3,0.05,12,1.12,12,'2023-12-12',400);

insert into sales_order(sa_customerid,sa_statusid) values (1,1), (2,1);

insert into product_order(pro_sales_orderid,pro_productid,pro_quantity,pro_price) values
(1,2,1,17.90),
(1,3,1,2.42),
(1,11,1,0.67),
(2,1,1,8.96),
(2,8,1,2.90),
(2,9,2,0.67);