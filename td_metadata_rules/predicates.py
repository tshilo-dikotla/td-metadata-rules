from edc_constants.constants import YES, POS, NEG, IND, UNK
from edc_metadata_rules import PredicateCollection
from edc_reference.models import Reference


class MaternalStatusHelper:

    @property
    def hiv_status(self):
        return POS


class Predicates(PredicateCollection):

    app_label = 'td_maternal'
    visit_model = f'{app_label}.maternalvisit'

    def func_mother_pos(self, visit=None, **kwargs):
        """Returns true if mother is hiv positive."""
        maternal_status_helper = MaternalStatusHelper()
        return maternal_status_helper.hiv_status == POS

    def func_mother_neg(self, visit=None, **kwargs):
        """Returns true if mother is hiv neg."""
        maternal_status_helper = MaternalStatusHelper()
        return maternal_status_helper.hiv_status == NEG

    def func_show_elisa_requisition_hiv_status_ind(self, visit=None, **kwargs):
        """return True if Mother's Rapid Test Result is Inditerminate"""
        maternal_status_helper = MaternalStatusHelper()
        return maternal_status_helper.hiv_status == IND

#     def func_require_cd4(self, visit):

    def func_mother_pos_vl(self, visit=None, **kwargs):

        visit_list = ['2000M', '2010M', '2020M', '2020M', '2060M']
        return self.func_mother_pos(visit) and visit.visit_code in visit_list

#     def func_require_pbmc_vl(self, visit):
#         return self.func_mother_pos(visit)
    def func_show_postpartum_depression(self, visit=None, **kwargs):
        visit_list = ['2020M', '2060M', '2120M', '2180M', '2240M',
                      '2300M', '2360M']
        if visit.visit_code in visit_list:
            return Reference.objects.filter(
                model=f'{self.app_label}.maternalpostpartumdep',
                identifier=visit.subject_identifier).exists()

    def func_show_ultrasound_form(self, visit=None, **kwargs):
        """Return true if ultrasound form has to be filled."""
        if visit.visit_code == '1000M':
            return True
        elif visit.visit_code == '1010M':
            return not Reference.objects.filter(
                model=f'{self.app_label}.maternalultrasoundinitial',
                identifier=visit.subject_identifier,
                timepoint='1000M').exists()
        return False

    def func_show_rapid_test_form(self, visit=None, **kwargs):
        subject_identifier = visit.subject_identifier
        maternal_status_helper = MaternalStatusHelper()
        if visit.visit_code == '2000M' and maternal_status_helper.hiv_status == NEG:
            prev_rapid_test = Reference.objects.filter(
                model=f'{self.app_label}.rapidtestresult',
                report_datetime__lt=visit.report_datetime,
                identifier=subject_identifier).order_by('-report_datetime')

            maternal_ultrasound = Reference.objects.filter(
                model=f'{self.app_label}.maternalultrasoundinitial',
                report_datetime__lt=visit.report_datetime,
                identifier=subject_identifier).order_by('-report_datetime')

            if prev_rapid_test and maternal_ultrasound:
                return (maternal_ultrasound.edd_confirmed - prev_rapid_test.result_date).days < 56
            else:
                return True
        else:
            return maternal_status_helper.hiv_status in [UNK, NEG]

    def func_show_srh_services_utilization(self, visit=None, **kwargs):
        """Returns True if participant was referred to srh in the last visit."""

        visit_list = ['2010M', '2020M', '2060M', '2120M', '2180M', '2240M',
                      '2300M', '2360M']

        previous_maternal_contr = Reference.objects.filter(
            model=f'{self.app_label}.maternalcontraception',
            identifier=visit.subject_identifier).exclude(
                timepoint=visit.visit_code).order_by('-report_datetime').first()

        if visit.visit_code in visit_list:
            values = self.exists(
                reference_name=f'{self.app_label}.maternalcontraception',
                subject_identifier=visit.subject_identifier,
                report_datetime=previous_maternal_contr.report_datetime,
                field_name='srh_referral')
            return (values[0] == YES)
