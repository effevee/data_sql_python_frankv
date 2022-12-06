#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 20:47:39 2022

@author: frank
"""

from db_actions import actions

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
        # get customer id
        get_last_id = '''select max(cu_id) from customer'''
        cr.execute(get_last_id,())
        customer_id = -1
        for row in cr:
            customer_id=row[0]
            break
        cr.close() # close db cursor
        return customer_id
    

    def insert_order(self,customer_id,status_id):

        # check if connection exists
        if self.check_connect() == False:
            return False
        
        # insert sales_order
        insert_order_query = '''insert into sales_order 
        (sa_customerid,sa_statusid) values(%s,%s)'''
        cr = self._cn.cursor()
        cr.execute(insert_order_query,(customer_id,status_id))
        self._cn.commit()
        cr.close()
        
        # get last sales_order id
        get_last_sales_order_id = '''select max(sa_id) from sales_order'''
        cr.execute(get_last_sales_order_id,())
        sales_order_id = -1
        for row in cr:
            sales_order_id=row[0]
            break
        

        return True
    