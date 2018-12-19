from datetime import datetime

from arrow.arrow import Arrow
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.tests import SiteTestCaseMixin
from edc_constants.constants import YES, NO
from edc_reference import LongitudinalRefset
from edc_reference.tests import ReferenceTestHelper

from ..predicates import Predicates, MaternalStatusHelper


@tag('pr')
class TestPredicates(SiteTestCaseMixin, TestCase):

    reference_helper_cls = ReferenceTestHelper
    visit_model = 'td_maternal.maternalvisit'
    reference_model = 'edc_reference.reference'
    app_label = 'td_maternal'

    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    def tearDown(self):
        super().tearDown()

    def setUp(self):

        self.subject_identifier = '111111111'
        self.reference_helper = self.reference_helper_cls(
            visit_model=self.visit_model,
            subject_identifier=self.subject_identifier)

        report_datetime = Arrow.fromdatetime(
            datetime(2018, 12, 17)).datetime
        self.reference_helper.create_visit(
            report_datetime=report_datetime - relativedelta(days=1), timepoint='1000M')

        self.reference_helper.create_visit(
            report_datetime=report_datetime,
            timepoint='1010M')
        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=3),
            timepoint='1020M')
        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=3),
            timepoint='2000M')

        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=3),
            timepoint='2010M')

    def test_func_elisa_required(self):
        pc = Predicates()

        self.assertFalse(
            pc.func_show_elisa_requisition_hiv_status_ind(self.maternla_visits[0]))

    def test_func_mother_pos_vl_required(self):
        pc = Predicates()

        self.assertTrue(
            pc.func_mother_pos_vl(self.maternla_visits[3]))

    def test_func_mother_pos_vl_not_required(self):
        pc = Predicates()

        self.assertFalse(
            pc.func_mother_pos_vl(self.maternla_visits[1]))

    def test_ultrasound_form_1000_required(self):
        pc = Predicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternla_visits[0].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternla_visits[0].visit_code)
        self.assertTrue(
            pc.func_show_ultrasound_form(self.maternla_visits[0]))

    def test_ultrasound_form_not_1000_required(self):
        pc = Predicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternla_visits[1].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternla_visits[1].visit_code)
        self.assertTrue(
            pc.func_show_ultrasound_form(self.maternla_visits[1]))

    def test_ultrasound_form_not_1000_not_required(self):
        pc = Predicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternla_visits[0].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternla_visits[0].visit_code)

        self.reference_helper.create_for_model(
            report_datetime=self.maternla_visits[1].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternla_visits[1].visit_code)
        self.assertFalse(
            pc.func_show_ultrasound_form(self.maternla_visits[1]))

    @property
    def maternla_visits(self):
        return LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model=self.visit_model,
            name=self.visit_model,
            reference_model_cls=self.reference_model
        ).order_by('report_datetime')

    def test_srh_services_utilization_required(self):
        pc = Predicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternla_visits[3].report_datetime,
            reference_name=f'{self.app_label}.maternalcontraception',
            visit_code=self.maternla_visits[3].visit_code,
            srh_referral=YES)

        self.reference_helper.create_for_model(
            report_datetime=self.maternla_visits[4].report_datetime,
            reference_name=f'{self.app_label}.maternalcontraception',
            visit_code=self.maternla_visits[4].visit_code)
        self.assertTrue(
            pc.func_show_srh_services_utilization(self.maternla_visits[4]))

    def test_srh_services_utilization_not_required(self):
        pc = Predicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternla_visits[3].report_datetime,
            reference_name=f'{self.app_label}.maternalcontraception',
            visit_code=self.maternla_visits[3].visit_code,
            srh_referral=NO)

        self.reference_helper.create_for_model(
            report_datetime=self.maternla_visits[4].report_datetime,
            reference_name=f'{self.app_label}.maternalcontraception',
            visit_code=self.maternla_visits[4].visit_code)
        self.assertFalse(
            pc.func_show_srh_services_utilization(self.maternla_visits[4]))
