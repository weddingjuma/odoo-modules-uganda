# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.config import config
import xmlrpclib
import csv
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)


class util(models.Model):
    _name = 'import.product'
    _description = "Tool to import products and related data"

    action_date = fields.Date(
        'Action Date', readonly=1, index=True, copy=False)
    item_id = fields.Char("Item ID")
    model = fields.Char('Model')

    def import_prod_categ(self):
        url = self.env['ir.config_parameter'].get_param('web.base.url')
        username = config.get("app_user")
        pwd = config.get("app_pwd")
        dbname = config.get("app_db")
        sock_common = xmlrpclib.ServerProxy(url+"/xmlrpc/common")
        uid = sock_common.login(dbname, username, pwd)
        sock = xmlrpclib.ServerProxy(url+"/xmlrpc/object")
        reader = csv.reader(open(
            '/vagrant/odoo-modules-uganda/product_category.csv', 'rb'), delimiter='|', quotechar='"')
        for row in reader:
            categ = self.env['product.category'].search(
                [('name', '=', row[0].strip())])
            if categ:
                _logger.error(row[0]+" Already exist")
            else:
                product_categ = {
                    'name': row[0].strip(),
                    'parent_id': 1,  # Product category called 'All'
                    'type': 'normal'
                }
                template_id = sock.execute(
                    dbname, uid, pwd, 'product.category', 'create', product_categ)
                self.create({'model': 'product.category', 'item_id': template_id,
                             'action_date': fields.Date.context_today(self)})
        return {}

    def import_uom(self):
        url = self.env['ir.config_parameter'].get_param('web.base.url')
        username = config.get("app_user")
        pwd = config.get("app_pwd")
        dbname = config.get("app_db")
        sock_common = xmlrpclib.ServerProxy(url+"/xmlrpc/common")
        uid = sock_common.login(dbname, username, pwd)
        sock = xmlrpclib.ServerProxy(url+"/xmlrpc/object")
        reader = csv.reader(open(
            '/vagrant/odoo-modules-uganda/product_uom.csv', 'rb'), delimiter='|', quotechar='"')
        for row in reader:
            uom = self.env['product.uom'].search(
                [('name', '=', row[0].strip())])
            if uom:
                _logger.error(row[0]+" Already exist")
            else:
                product_uom = {
                    'name': row[0].strip(),
                    'category_id': 6,  # UoM category called 'Imported'
                    'uom_type': 'reference',
                    'rounding': 0.00100
                }
                template_id = sock.execute(
                    dbname, uid, pwd, 'product.uom', 'create', product_uom)
                self.create({'model': 'product.uom', 'item_id': template_id,
                             'action_date': fields.Date.context_today(self)})
        return {}

    def import_prod(self):
        url = self.env['ir.config_parameter'].get_param('web.base.url')
        username = config.get("app_user")
        pwd = config.get("app_pwd")
        dbname = config.get("app_db")
        sock_common = xmlrpclib.ServerProxy(url+"/xmlrpc/common")
        uid = sock_common.login(dbname, username, pwd)
        sock = xmlrpclib.ServerProxy(url+"/xmlrpc/object")
        reader = csv.reader(open(
            '/vagrant/odoo-modules-uganda/product_template.csv', 'rb'), delimiter=',', quotechar='"')

        for row in reader:
            uom = self.env['product.uom'].search(
                [('name', '=', row[1].strip())])
            name = self.env['product.template'].search(
                [('name', '=', row[0].split('-', 1)[1].strip())])
            prod_categ = self.env['product.category'].search(
                [('name', '=', row[6].strip())])
            if name:
                _logger.error(
                    "====="+row[0].split('-', 1)[1].strip()+" Duplicate")
            else:
                if uom:
                    product_template = {
                        'default_code': row[0].split('-', 1)[0].strip(),
                        'name': row[0].split('-', 1)[1].strip(),
                        'uom_id': uom.id,
                        'uom_po_id': uom.id,
                        'list_price': float(row[5]) if row[5] else (float(row[2]) if row[2] else 0.0),
                        'categ_id': prod_categ.id,
                        'mrp': float(row[5]) if row[5] else (float(row[2]) if row[2] else 0.0),
                        'standard_price': float(row[2]) if row[2] else (float(row[5]) if row[5] else 0.0),
                        'type': 'product'
                    }
                    template_id = sock.execute(
                        dbname, uid, pwd, 'product.template', 'create', product_template)
                    self.create({'model': 'product.template', 'item_id': template_id,
                                 'action_date': fields.Date.context_today(self)})
                    stock_warehouse_orderpoint = {
                        'name': self.env['ir.sequence'].next_by_code('stock.orderpoint') or '/',
                        'product_max_qty': (float(row[4])*3) if row[4] else 0.0,
                        'product_min_qty': float(row[4]) if row[4] else 0.0,
                        'qty_multiple': 0,
                        'lead_days': 1,
                        'lead_type': 'supplier',
                        'product_id': template_id,
                        'warehouse_id': 1,
                        'location_id': self.env['stock.picking.type'].search([('name', '=', 'Receipts')]).default_location_dest_id.id if self.env['stock.picking.type'].search([('name', '=', 'Receipts')]) else 15
                    }
                    template_id = sock.execute(
                        dbname, uid, pwd, 'stock.warehouse.orderpoint', 'create', stock_warehouse_orderpoint)
                    self.create({'model': 'stock.warehouse.orderpoint', 'item_id': template_id,
                                 'action_date': fields.Date.context_today(self)})
                else:
                    _logger.error(
                        "====="+row[0].split('-', 1)[1].strip() + " UoM not found: "+str(row[1]))
        return {}