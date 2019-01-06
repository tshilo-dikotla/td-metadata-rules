from django.test import TestCase
from edc_base.tests import SiteTestCaseMixin
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NEG, POS
from edc_reference import LongitudinalRefset
from edc_reference.tests import ReferenceTestHelper

from ..predicates import InfantPredicates


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


class TestInfantPredicates(SiteTestCaseMixin, TestCase):

    reference_helper_cls = ReferenceTestHelper
    maternal_visit_model = 'td_maternal.maternalvisit'
    visit_model = 'td_infant.infantvisit'
    reference_model = 'edc_reference.reference'
    app_label = 'td_infant'

    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    def tearDown(self):
        super().tearDown()

    def setUp(self):

        self.subject_identifier = '111111111-10'
        self.maternal_subject_identifier = '111111111'
        report_datetime = get_utcnow()

        self.reference_helper = self.reference_helper_cls(
            visit_model=self.maternal_visit_model,
            subject_identifier=self.maternal_subject_identifier)

        self.reference_helper.create_visit(
            report_datetime=report_datetime, timepoint='2000M')

        self.reference_helper = self.reference_helper_cls(
            visit_model=self.visit_model,
            subject_identifier=self.subject_identifier)

        self.reference_helper.create_visit(
            report_datetime=report_datetime, timepoint='2000')

        self.reference_helper.create_visit(
            report_datetime=report_datetime, timepoint='2010')

        self.reference_helper.create_visit(
            report_datetime=report_datetime, timepoint='2020')

        self.reference_helper.create_visit(
            report_datetime=report_datetime, timepoint='2060')

        self.reference_helper.create_visit(
            report_datetime=report_datetime, timepoint='2180')

    def test_func_show_infant_arv_proph_required(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertTrue(
            pc.func_show_infant_arv_proph(self.infant_visits[1],
                                          maternal_status_helper))


#     def test_func_show_infant_arv_proph_required_2(self):
#         pc = InfantPredicates()
#         maternal_status_helper = MaternalStatusHelper(status=POS)
#
#         self.reference_helper.create_for_model(
#             report_datetime=self.infant_visits[1].report_datetime,
#             reference_name=f'{self.app_label}.infantarvproph',
#             visit_code=self.infant_visits[1].visit_code)
#
#         self.reference_helper.create_for_model(
#             report_datetime=self.infant_visits[1].report_datetime,
#             reference_name=f'{self.app_label}.infantarvprophmod',
#             visit_code=self.infant_visits[1].visit_code,
#             dose_status='blah blah')
#
#         self.assertTrue(
#             pc.func_show_infant_arv_proph(self.infant_visits[2],
#                                           maternal_status_helper))

    def test_func_show_infant_arv_proph_not_required(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertFalse(
            pc.func_show_infant_arv_proph(self.infant_visits[2],
                                          maternal_status_helper))

    def test_func_infant_heu_required(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertTrue(
            pc.func_infant_heu(self.infant_visits[2],
                               maternal_status_helper))

    def test_func_infant_heu_not_required(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=NEG)

        self.assertFalse(
            pc.func_infant_heu(self.infant_visits[2],
                               maternal_status_helper))

    def test_func_infant_heu_require_pcr_required(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertTrue(
            pc.func_infant_heu_require_pcr(self.infant_visits[2],
                                           maternal_status_helper))

    def test_func_infant_heu_require_pcr_not_required(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertFalse(
            pc.func_infant_heu_require_pcr(self.infant_visits[0],
                                           maternal_status_helper))

    def test_func_infant_heu_require_pcr_not_required_2(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=NEG)

        self.assertFalse(
            pc.func_infant_heu_require_pcr(self.infant_visits[2],
                                           maternal_status_helper))

    def test_func_require_infant_elisa_required(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertTrue(
            pc.func_require_infant_elisa(self.infant_visits[4],
                                         maternal_status_helper))

    def test_func_require_infant_elisa_required_not_required(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertFalse(
            pc.func_require_infant_elisa(self.infant_visits[3],
                                         maternal_status_helper))

    def test_func_require_infant_elisa_required_not_required_2(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=NEG)

        self.assertFalse(
            pc.func_require_infant_elisa(self.infant_visits[4],
                                         maternal_status_helper))

    def test_func_require_infant_dbs_required(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertTrue(
            pc.func_require_infant_dbs(self.infant_visits[1],
                                       maternal_status_helper))

    def test_func_require_infant_dbs_not_required(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=NEG)

        self.assertFalse(
            pc.func_require_infant_dbs(self.infant_visits[1],
                                       maternal_status_helper))

    def test_func_require_infant_dbs_not_required_2(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.assertFalse(
            pc.func_require_infant_dbs(self.infant_visits[2],
                                       maternal_status_helper))

    def test_func_show_infant_nvp_dispensing_required(self):
        pass

    def test_func_show_nvp_adjustment_2010_required(self):
        pc = InfantPredicates()
        maternal_status_helper = MaternalStatusHelper(status=POS)

        self.reference_helper.create_for_model(
            report_datetime=self.infant_visits[1].report_datetime,
            reference_name=f'{self.app_label}.infantnvpdispensing',
            visit_code=self.infant_visits[0].visit_code,
            nvp_prophylaxis=YES)

        self.assertTrue(
            pc.func_show_nvp_adjustment_2010(self.infant_visits[1],
                                             maternal_status_helper))

    @property
    def infant_visits(self):
        return LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model=self.visit_model,
            name=self.visit_model,
            reference_model_cls=self.reference_model
        ).order_by('report_datetime')
