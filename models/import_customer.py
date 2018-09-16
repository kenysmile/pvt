# -*- coding: utf-8 -*-
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime,timedelta
import pytz
import re

group_user_index = 17
min_col_number = 18

class Test_customer(models.TransientModel):
    _name = 'test.customer'
    _inherits = {'ir.attachment': 'attachment_id'}



    #
    # name = fields.Char()
    # _import_model_name = 'res.partner'
    # _import_date_format = '%d-%m-%Y'
    #
    # template_file_url = fields.Char(compute='_compute_template_file_url',
    #                                 default=lambda self:
    #                                 self.env['ir.config_parameter'].
    #                                 get_param('web.base.url') +
    #                                 '/bave_import/static/import_template/'
    #                                 'import_customer.xlsx')

    # @api.multi
    # def _compute_template_file_url(self):
    #     base_url = self.env['ir.config_parameter'].get_param('web.base.url')
    #     url = base_url + '/bave_import/static/import_template/import_customer.xlsx'
    #     for ip in self:
    #         ip.template_file_url = url

    def find_brand(self, source_string):
        ls_brand = []
        if source_string:
            ls_info = source_string.split("/")
            for ls_in in ls_info:
                brand = ls_in.split(" ")
                ls_brand.extend(brand)
        for item in ls_brand:
            result = self.env['fleet.vehicle.model.brand'].search([('name', 'ilike', item)])
            if result:
                return result[0].name
        return False

    def find_current(self, source_string):
        ls_current = []
        if source_string:
            ls_info = source_string.split("/")
            for ls_in in ls_info:
                current = ls_in.split(" ")
                ls_current.extend(current)
        for item in ls_current:
            result = self.env['fleet.vehicle.model'].search([('name', 'ilike', item)])
            if result:
                return result[0].name
        return False

    def find_phone(self, source_string):
        ls_phone = []
        if source_string:
            source_string = source_string.replace('.', '')
            source_string = source_string.replace('-', '')
            source_string = source_string.replace(' ', '')
            ls_info = source_string.split("/")
            for item in ls_info:
                phone_number = re.findall(r'((?:\d{9,13}))', item)
                if phone_number:
                    ls_phone.extend(phone_number)

        return ls_phone

    def find_name(self, source_string):
        ls_name = []
        if source_string:
            ls_info = source_string.split("/")
            for item in ls_info:
                try:
                    str(item)
                except:
                    return item
                # name = re.findall(r'^[a-zA-Z]\w*', item) or re.findall(r'^[a-zA-Z]\w*[0-9]', item)
                #name = re.findall(r'[A-Z][a-z]{1,10}[A-Z][a-z]{1,10}', item) or re.findall(r'([a-z]{1,20}[A-Z][a-z])', item)
                #name = re.findall(r'[A-Z][a-z]{1,20}[A-Z][a-z]{1,10}', item) or re.findall(r'([a-z]{1,20}[A-Z]\w*)', item)
                # name = re.search('[A-Z]+', item)
                # if name:
                #     ls_name.append(name)
                #     print(name)
                    # print(ls_name)
                    # for nam in name:
                    #     print()
        return ls_name

    # def find_license_plate(self, source_string):
    #     ls_license_plate = []
    #     if source_string:
    #         ls_info = source_string.split("/")
    #         for item in ls_info:
    #             name = re.findall(r'((?:\d{2}[A-Z][0-9]{3,8}))', item)
    #             if name:
    #                 ls_license_plate.append(name)
    #     return ls_license_plate

    def test_customer(self):
        content = self.get_value_from_excel_row()
        content = content[1:]
        lst_customer = []
        for cont in content:
            phone = self.find_phone(cont)
            lst_customer.extend(phone)

            # name = self.find_name(cont)
            # lst_customer.append(name)

            lst_find_brand = self.find_brand(cont)
            lst_customer.append(lst_find_brand)

            lst_find_current = self.find_current(cont)
            lst_customer.append(lst_find_current)

            print(lst_customer)
        return True

    @api.multi
    def get_value_from_excel_row(self):
        list_test = []
        excel_data = self.env['read.excel'].read_file(data=self.datas, sheet="Sheet1", path=False)
        if len(excel_data) < 2:
            raise UserError(_(
                'Error: Format file incorrect, you must import file have at least 2 row!'))

        if len(excel_data[0]) < min_col_number:
            raise UserError(_(
                'Error: Format file incorrect, you must import file have at least {} column!').format(
                min_col_number))
        for i in excel_data:
            list_test.append(i[2])
        return list_test




    #
    #     partner_model = self.env['res.partner']
    #     company_id = self.env.user.company_id.id
    #     if excel_data:
    #         catg_data = {}
    #         atts_create = []
    #         row_count = 1
    #         for i in excel_data[1:]:
    #             row_count += 1
    #             if not i[1]:
    #                 raise UserError(_('Customer name can not empty, Row %s - Column B') % row_count)
    #             if not i[2]:
    #                 raise UserError(_('Customer code can not empty, Row %s - Column C') % row_count)
    #             exist_code = partner_model.sudo().search([('code', '=', i[2])])
    #             if exist_code:
    #                 raise UserError(_('Customer already exists, Row %s - Column C') % row_count)
    #             if not i[15]:
    #                 raise UserError(_('Receivable Account can not empty, Row %s - Column P') % row_count)
    #
    #             if not i[16]:
    #                 raise UserError(_('Payable Account can not empty, Row %s - Column Q') % row_count)
    #
    #             x_type_1 = u'Cá nhân'
    #             x_type_2 = u'Công ty'
    #
    #             x_type = ''
    #             if i[0].encode('utf-8').strip().lower() == x_type_1.encode('utf-8').strip().lower():
    #                 x_type = 'person'
    #             elif i[0].encode('utf-8').strip().lower() == x_type_2.encode('utf-8').strip().lower():
    #                 x_type = 'company'
    #
    #             if not x_type:
    #                 raise UserError(_('Type customer does not exists, Row %s - Column A') % row_count)
    #
    #             country_id = self.env['res.country'].search([('name', '=', i[4].encode('utf-8').strip())])
    #             if i[4] and not country_id:
    #                 raise UserError(_('Không tìm thấy trường quốc gia, Hàng %s - Cột E') % row_count)
    #             state_id = self.env['res.country.state'].search([('name', '=', i[5].encode('utf-8').strip())])
    #             if i[5] and not state_id:
    #                 raise UserError(_('Không tìm thấy trường thành phố, Hàng %s - Cột F') % row_count)
    #             district_id = self.env['res.country.district'].search([('name', '=', i[6].encode('utf-8').strip())])
    #             if i[6] and not district_id:
    #                 raise UserError(_('Không tìm thấy trường Quận/Huyện, Hàng %s - Cột G') % row_count)
    #             ward_id = self.env['res.country.ward'].search([('name', '=', i[7].encode('utf-8').strip())])
    #             if i[7] and not ward_id:
    #                 raise UserError(_('Không tìm thấy trường Phường xã, Hàng %s - Cột G') % row_count)
    #
    #             receivable_id = False
    #             payable_id = False
    #
    #             if type(i[15]) is float:
    #                 x_receivable_id = self.env['account.account'].with_context(show_parent_account=True).search(
    #                     [('code', '=', str(i[15]).split('.')[0].encode('utf-8')), ('company_id', '=', company_id)])
    #                 if not x_receivable_id:
    #                     raise UserError(_('Receivable Account does not exists! Row %s - Column P') % row_count)
    #                 else:
    #                     receivable_id = x_receivable_id.id
    #
    #             if type(i[15]) is unicode:
    #                 x_receivable_id = self.env['account.account'].with_context(show_parent_account=True).search(
    #                     [('code', '=', i[15].encode('utf-8')), ('company_id', '=', company_id)])
    #                 if not x_receivable_id:
    #                     raise UserError(_('Receivable Account does not exists! Row %s - Column P') % row_count)
    #                 else:
    #                     receivable_id = x_receivable_id.id
    #
    #             if type(i[16]) is float:
    #                 x_code = str(i[16]).split('.')[0].encode('utf-8')
    #                 x_payable_id = self.env['account.account'].with_context(show_parent_account=True).search(
    #                         [('code', '=', x_code), ('company_id', '=', company_id)])
    #                 if not x_payable_id:
    #                     raise UserError(_('Payable Account does not exists! Row %s - Column Q') % row_count)
    #                 else:
    #                     payable_id = x_payable_id.id
    #
    #             if type(i[16]) is unicode:
    #                 x_payable_id = self.env['account.account'].with_context(show_parent_account=True).search(
    #                     [('code', '=', i[16].encode('utf-8')), ('company_id', '=', company_id)])
    #                 if not x_payable_id:
    #                     raise UserError(_('Payable Account does not exists! Row %s - Column Q') % row_count)
    #                 else:
    #                     payable_id = x_payable_id.id
    #
    #             group_user = False
    #             if i[group_user_index]:
    #                 group_users = self.env['btek.partner.group'].search(
    #                     ['|',('name', '=', i[group_user_index]),('code', '=', i[group_user_index])])
    #                 group_user = group_users and group_users[0].id or False
    #                 if not group_user:
    #                     raise UserError(_(
    #                         'Partner group "{}" does not exists! Row {}').format(i[group_user_index], row_count))
    #
    #             x_sex_1 = u'Nam'
    #             x_sex_2 = u'Nữ'
    #             x_sex_3 = u'Khác'
    #
    #             x_sex = ''
    #             if i[9].encode('utf-8').strip().lower() == x_sex_1.encode('utf-8').strip().lower():
    #                 x_sex = 'male'
    #             elif i[9].encode('utf-8').strip().lower() == x_sex_2.encode('utf-8').strip().lower():
    #                 x_sex = 'female'
    #             elif i[9].encode('utf-8').strip().lower() == x_sex_3.encode('utf-8').strip().lower():
    #                 x_sex = 'other'
    #
    #             title = self.env['res.partner.title'].search([('name', '=', i[11].encode('utf-8').strip())])
    #             if i[11] and not title:
    #                 raise UserError(_('Không tìm thấy trường tiêu đề, Hàng %s - Cột L') % row_count)
    #
    #             if type(i[10]) != unicode:
    #                 raise UserError(_('Định dạng nhập trường ngày không đúng, vui lòng nhập định dạng chuỗi như mẫu, Hàng %s - Cột K') % row_count)
    #             check_birth = ''
    #             if i[10]:
    #                 date_birth = str(datetime.strptime(i[10], '%d/%m/%Y'))
    #                 check_birth = str(datetime.strptime(date_birth, '%Y-%m-%d 00:00:00'))
    #
    #             atts_create.append({
    #                 'company_type': x_type,
    #                 'name': i[1],
    #                 'code': i[2],
    #                 'vat': i[8],
    #                 'street': i[3],
    #                 'district_id': district_id[0].id if district_id else False,
    #                 'country_id': country_id[0].id if country_id else False,
    #                 'state_id': state_id[0].id if state_id else False,
    #                 'ward_id': ward_id[0].id if ward_id else False,
    #                 'sex': x_sex,
    #                 'date_of_birth': check_birth,
    #                 'title': title.id,
    #                 'comment': i[12],
    #                 'property_account_receivable_id': receivable_id,
    #                 'property_account_payable_id': payable_id,
    #                 'customer': True,
    #                 'phone': i[13],
    #                 'email': i[14],
    #                 'group_user': group_user,
    #             })
    #         catg_data['atts_create'] = atts_create
    #         return catg_data
