insert into supplier(su_firstname,su_lastname,su_email,su_address) values
('Frans','Wurst','frans.wurst@dbb.de','Die Bessere Burger, Koelnstrasse 444, Hamburg, Duitsland'),
('Altijd','Dorst','drankcentrale@altijddorst.be','Drankencentrale Altijd Dorst, Oudenaardsesteenweg 88, Berchem, Belgie'),
('Jan','Peeters','jan.peeters@saus.peeters.be','Sauzen Peeters, Kustlaan 23, Oostende, Belgie');

insert into product(pr_name,pr_categoryid) values
('Burger Gezond',1),
('Burger De Grote Honger',1),
('Cola',2),
('Cola Zero',2),
('Fanta',2),
('Water',2),
('Spuitwater',2),
('Jupiler',2),
('Ketchup',3),
('Mayonaise',3),
('BBQ saus',3),
('Tartaar saus',3);

insert into customer(cu_firstname,cu_lastname,cu_email,cu_address,cu_birthdate) values
('Frank','Vergote','effevee@gmail.com','Lenteakkerstraat 4, 8770 Ingelmunster', '1959-04-16 00:00:00'),
('Bernard','Geldof','beegee@gmail.com','Hertogstraat 20, 8870 Izegem', '1958-07-20 00:00:00');

insert into product_detail(pd_unitprice,pd_expiredate,pd_salesfactor,pd_taxfactor,pd_productid) values
(4.00,'2023-01-31 00:00:00',2,1.12,1),
(7.99,'2023-01-31 00:00:00',2,1.12,2),
(0.25,'2023-01-31 00:00:00',8,1.21,3),
(0.25,'2023-01-31 00:00:00',8,1.21,4),
(0.25,'2023-01-31 00:00:00',8,1.21,5),
(0.15,'2023-01-31 00:00:00',8,1.21,6),
(0.20,'2023-01-31 00:00:00',8,1.21,7),
(0.30,'2023-01-31 00:00:00',8,1.21,8),
(0.05,'2023-01-31 00:00:00',12,1.12,9),
(0.05,'2023-01-31 00:00:00',12,1.12,10),
(0.05,'2023-01-31 00:00:00',12,1.12,11),
(0.05,'2023-01-31 00:00:00',12,1.12,12);

insert into purchase_order(po_date,po_quantity,po_supplierid,po_product_detailid) values
('2022-11-16 00:00:00',400,1,1),
('2022-11-16 00:00:00',300,1,2),
('2022-11-16 00:00:00',500,2,3),
('2022-11-16 00:00:00',500,2,4),
('2022-11-16 00:00:00',500,2,5),
('2022-11-16 00:00:00',500,2,6),
('2022-11-16 00:00:00',500,2,7),
('2022-11-16 00:00:00',500,2,8),
('2022-11-16 00:00:00',400,3,9),
('2022-11-16 00:00:00',400,3,10),
('2022-11-16 00:00:00',400,3,11),
('2022-11-16 00:00:00',400,3,12);

insert into sales_order(sa_customerid,sa_statusid) values (1,1), (2,1);

insert into product_order(pro_sales_orderid,pro_productid,pro_quantity) values
(1,2,1),
(1,3,1),
(1,11,1),
(2,1,1),
(2,8,1),
(2,9,2);