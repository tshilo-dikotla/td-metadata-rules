from dateutil.relativedelta import relativedelta
from django.test import TestCase
from edc_base.tests import SiteTestCaseMixin
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, NEG, POS, IND, UNK
from edc_reference import LongitudinalRefset
from edc_reference.tests import ReferenceTestHelper

from ..predicates import MaternalPredicates


class MaternalStatusHelper:

    def __init__(self, status=None, cd4=None):
        self.status = status
        self.cd4 = cd4

    @property
    def hiv_status(self):
        return self.status

    @property
    def eligible_for_cd4(self):
        return self.cd4


class TestMaternalPredicates(SiteTestCaseMixin, TestCase):

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

        report_datetime = get_utcnow()
        self.reference_helper.create_visit(
            report_datetime=report_datetime, timepoint='1000M')

        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=1),
            timepoint='1010M')
        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=3),
            timepoint='1020M')
        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=5),
            timepoint='2000M')

        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=7),
            timepoint='2010M')

        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=9),
            timepoint='2020M')

        self.reference_helper.create_visit(
            report_datetime=report_datetime + relativedelta(days=11),
            timepoint='2020M')

    def test_func_mother_pos(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertTrue(
            pc.func_mother_pos(self.maternal_visits[0],
                               maternal_status_helper))

    def test_func_mother_neg(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=NEG)

        self.assertTrue(
            pc.func_mother_neg(self.maternal_visits[1],
                               maternal_status_helper))

    def test_func_mother_pos_vl_required(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertTrue(
            pc.func_mother_pos_vl(self.maternal_visits[3],
                                  maternal_status_helper))

    def test_func_mother_pos_vl_not_required(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=NEG)

        self.assertFalse(
            pc.func_mother_pos_vl(self.maternal_visits[1],
                                  maternal_status_helper))

    def test_func_elisa_required(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=IND)

        self.assertTrue(
            pc.func_show_elisa_requisition(self.maternal_visits[0],
                                           maternal_status_helper))

    def test_func_elisa_not_required(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=NEG)

        self.assertFalse(
            pc.func_show_elisa_requisition(self.maternal_visits[0],
                                           maternal_status_helper))

    def test_func_require_cd4_required(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS, cd4=True)

        self.assertTrue(
            pc.func_require_cd4(self.maternal_visits[1],
                                maternal_status_helper))

    def test_func_require_cd4_not_required(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertFalse(
            pc.func_require_cd4(self.maternal_visits[1],
                                maternal_status_helper))

    def test_func_require_cd4_not_required_2(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=NEG)

        self.assertFalse(
            pc.func_require_cd4(self.maternal_visits[1],
                                maternal_status_helper))

    def test_func_require_cd4_not_required_3(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertFalse(
            pc.func_require_cd4(self.maternal_visits[3],
                                maternal_status_helper))

    def test_postpartum_depression_form_required(self):
        pc = MaternalPredicates()

        self.assertTrue(
            pc.func_show_postpartum_depression(self.maternal_visits[5]))

    def test_postpartum_depression_form_not_required(self):
        pc = MaternalPredicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[4].report_datetime,
            reference_name=f'{self.app_label}.maternalpostpartumdep',
            visit_code=self.maternal_visits[4].visit_code)

        self.assertFalse(
            pc.func_show_postpartum_depression(self.maternal_visits[5]))

    def test_postpartum_depression_form_not_required_2(self):
        pc = MaternalPredicates()

        self.assertFalse(
            pc.func_show_postpartum_depression(self.maternal_visits[0]))

    def test_ultrasound_form_required(self):
        pc = MaternalPredicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[0].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternal_visits[0].visit_code)
        self.assertTrue(
            pc.func_show_ultrasound_form(self.maternal_visits[0]))

    def test_ultrasound_form_required_1(self):
        pc = MaternalPredicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[1].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternal_visits[1].visit_code)
        self.assertTrue(
            pc.func_show_ultrasound_form(self.maternal_visits[1]))

    def test_ultrasound_form_not_required(self):
        pc = MaternalPredicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[0].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternal_visits[0].visit_code)

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[1].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternal_visits[1].visit_code)
        self.assertFalse(
            pc.func_show_ultrasound_form(self.maternal_visits[1]))

    def test_rapid_test_form_required(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=NEG)

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[2].report_datetime,
            reference_name=f'{self.app_label}.rapidtestresult',
            visit_code=self.maternal_visits[2].visit_code,
            result_date=self.maternal_visits[2].report_datetime.date())

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[1].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternal_visits[1].visit_code,
            edd_confirmed=(
                self.maternal_visits[2].report_datetime + relativedelta(
                    days=57)).date())

        self.assertTrue(
            pc.func_show_rapid_test_form(self.maternal_visits[3],
                                         maternal_status_helper))

    def test_rapid_test_form_required_2(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=UNK)

        self.assertTrue(
            pc.func_show_rapid_test_form(self.maternal_visits[1],
                                         maternal_status_helper))

    def test_rapid_test_form_required_3(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=UNK)

        self.assertTrue(
            pc.func_show_rapid_test_form(self.maternal_visits[2],
                                         maternal_status_helper))

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[1].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternal_visits[1].visit_code,
            edd_confirmed=(
                self.maternal_visits[2].report_datetime + relativedelta(
                    days=57)).date())

        self.assertTrue(
            pc.func_show_rapid_test_form(self.maternal_visits[3],
                                         maternal_status_helper))

    def test_rapid_test_form_not_required_2(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertFalse(
            pc.func_show_rapid_test_form(self.maternal_visits[3],
                                         maternal_status_helper))

        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[2].report_datetime,
            reference_name=f'{self.app_label}.rapidtestresult',
            visit_code=self.maternal_visits[2].visit_code,
            result_date=self.maternal_visits[2].report_datetime.date())

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[1].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternal_visits[1].visit_code,
            edd_confirmed=(
                self.maternal_visits[2].report_datetime + relativedelta(
                    days=57)).date())

        self.assertFalse(
            pc.func_show_rapid_test_form(self.maternal_visits[3],
                                         maternal_status_helper))

    def test_rapid_test_form_not_required_3(self):
        pc = MaternalPredicates()
        maternal_status_helper = MaternalStatusHelper(status=NEG)

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[2].report_datetime,
            reference_name=f'{self.app_label}.rapidtestresult',
            visit_code=self.maternal_visits[2].visit_code,
            result_date=self.maternal_visits[2].report_datetime.date())

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[1].report_datetime,
            reference_name=f'{self.app_label}.maternalultrasoundinitial',
            visit_code=self.maternal_visits[1].visit_code,
            edd_confirmed=(
                self.maternal_visits[2].report_datetime + relativedelta(
                    days=50)).date())

        self.assertFalse(
            pc.func_show_rapid_test_form(self.maternal_visits[3],
                                         maternal_status_helper))

    def test_srh_services_utilization_required(self):
        pc = MaternalPredicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[3].report_datetime,
            reference_name=f'{self.app_label}.maternalcontraception',
            visit_code=self.maternal_visits[3].visit_code,
            srh_referral=YES)

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[4].report_datetime,
            reference_name=f'{self.app_label}.maternalcontraception',
            visit_code=self.maternal_visits[4].visit_code)
        self.assertTrue(
            pc.func_show_srh_services_utilization(self.maternal_visits[4]))
        pc = MaternalPredicates()

    def test_srh_services_utilization_not_required(self):
        pc = MaternalPredicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[3].report_datetime,
            reference_name=f'{self.app_label}.maternalcontraception',
            visit_code=self.maternal_visits[3].visit_code,
            srh_referral=NO)

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[4].report_datetime,
            reference_name=f'{self.app_label}.maternalcontraception',
            visit_code=self.maternal_visits[4].visit_code)
        self.assertFalse(
            pc.func_show_srh_services_utilization(self.maternal_visits[4]))

    def test_srh_services_utilization_not_required_2(self):
        pc = MaternalPredicates()

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[3].report_datetime,
            reference_name=f'{self.app_label}.maternalcontraception',
            visit_code=self.maternal_visits[3].visit_code,
            srh_referral=NO)

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[5].report_datetime,
            reference_name=f'{self.app_label}.maternalcontraception',
            visit_code=self.maternal_visits[5].visit_code,
            srh_referral=YES)

        self.reference_helper.create_for_model(
            report_datetime=self.maternal_visits[4].report_datetime,
            reference_name=f'{self.app_label}.maternalcontraception',
            visit_code=self.maternal_visits[4].visit_code)
        self.assertFalse(
            pc.func_show_srh_services_utilization(self.maternal_visits[4]))

    @property
    def maternal_visits(self):
        return LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model=self.visit_model,
            name=self.visit_model,
            reference_model_cls=self.reference_model
        ).order_by('report_datetime')
