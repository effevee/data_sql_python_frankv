#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 20:47:39 2022

@author: frank
"""

from db_actions import actions
import time

class actions_db_monday_burger(actions):
    
    def check_connect(self):
        if self._cn is not None:
            return True
        return False
    

    def insert_customer(self,fname,lname,birth,email,address):
        
        # check if connection exists
        if self.check_connect() == False:
            return -1  # no connection
        
        # check if customer exists 
        # combination of firstname, lastname, birthdate
        chk_customer_query = '''select cu_id from customer 
            where cu_firstname=%s and cu_lastname=%s and cu_birthdate=%s'''
        cr = self._cn.cursor()
        cr.execute(chk_customer_query,(fname,lname,birth))
        customer_id = -1
        for row in cr: # loop results
            customer_id=row[0]  # first column from first row
            break # there should be only one row
        if customer_id != -1: # customer already exists
            cr.close()
            return customer_id
        
        # customer does not exist, so insert into database
        insert_customer_query = '''insert into customer
        (cu_firstname,cu_lastname,cu_email,cu_address,cu_birthdate) 
        values(%s,%s,%s,%s,%s)'''
        cr.execute(insert_customer_query,(fname,lname,email,address,birth))
        self._cn.commit()
        # get last customer id
        get_last_id = '''select max(cu_id) from customer'''
        cr.execute(get_last_id,())
        customer_id = -1
        for row in cr:
            customer_id=row[0]
            break
        cr.close() # close db cursor
        return customer_id
    

    def insert_sales_order(self,customer_id,status):

        # check if connection exists
        if self.check_connect() == False:
            return False
        
        # insert sales_order
        insert_order_query = '''insert into sales_order (sa_customerid,sa_statusid) 
        values(%s,(select st_id from status where st_name = %s))'''
        cr = self._cn.cursor()
        cr.execute(insert_order_query,(customer_id,status))
        self._cn.commit()
        
        # get last sales_order id (only PAID)
        get_last_sales_order_id = '''select max(sa_id) from sales_order where
        sa_statusid = 1'''
        cr.execute(get_last_sales_order_id,())
        sales_order_id = -1
        for row in cr:
            sales_order_id=row[0]
            break
        cr.close()
        return sales_order_id
    
    
    def insert_product_order(self,products,sales_order_id):
        
        # check if connection exists
        if self.check_connect() == False:
            return False
        
        # check valid order (PAID status)
        if sales_order_id <= 0:
            return False
        
        # insert product_order
        insert_product_order_query = '''
        insert into product_order(pro_sales_orderid,pro_productid,pro_quantity,pro_price) 
        values(%s,
              (select pr_id from product where ucase(pr_name) = ucase(%s)),
              %s,
              (select %s*po_unitprice*po_salesfactor*po_taxfactor from purchase_order 
               where po_productid = (select pr_id from product where ucase(pr_name) = ucase(%s))))'''
        update_stock_query = '''
        update purchase_order set po_stock = po_stock - %s 
        where po_productid = (select pr_id from product where ucase(pr_name) = ucase(%s))
        '''
        cr = self._cn.cursor()        
        for p in products:
            cr.execute(insert_product_order_query,
                       (sales_order_id,p,products[p],products[p],p))
            self._cn.commit()
            cr.execute(update_stock_query, (products[p],p))
            self._cn.commit()            
        cr.close()

    
    def update_order_status(self,sales_order_id,status):

        # check if connection exists
        if self.check_connect() == False:
            return False

        # update status
        update_status_query = '''update sales_order set sa_statusid = 3 where sa_id = %s'''
        if status == 'DELIVERED':
            update_status_query = update_status_query.replace('3','4')
        cr = self._cn.cursor()
        cr.execute(update_status_query,(sales_order_id,))
        self._cn.commit()
        cr.close()
        
    
    def get_product_stock(self,category_id):
       
        # check if connection exists
        data = []
        if self.check_connect() == False:
            return [data]
        
        # get product stock
        get_stock_query = '''select pr_name,po_stock from purchase_order,product 
                             where pr_id = po_productid and pr_categoryid = %s'''
        
        # time stocktake
        t=time.localtime()
        now = str(t.tm_hour) + ":" + str(t.tm_min)
        cr = self._cn.cursor()
        cr.execute(get_stock_query,(category_id,))
        for row in cr:
            data.append(list(row))
            data[-1].insert(0,now) # add time of stocktake
        cr.close()
        return data
       
                                    