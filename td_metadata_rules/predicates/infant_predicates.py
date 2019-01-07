from django.apps import apps as django_apps
from edc_constants.constants import YES
from edc_metadata_rules import PredicateCollection
from edc_reference.models import Reference
from td_maternal.helper_classes import MaternalStatusHelper

from .maternal_predicates import MaternalPredicates


class InfantPredicates(PredicateCollection):

    app_label = 'td_infant'
    visit_model = f'{app_label}.infantvisit'

    def get_latest_maternal_visit_status(self, visit=None, maternal_status_helper=None):
        status = False
        try:
            maternal_visit = Reference.objects.get(
                identifier=visit.subject_identifier[:-3],
                timepoint='2000M')
        except Exception:
            pass
        else:
            mpc = MaternalPredicates()
            maternal_status_helper = maternal_status_helper or MaternalStatusHelper(
                maternal_visit)
            status = mpc.func_mother_pos(
                maternal_visit, maternal_status_helper)
        return status

    def func_show_infant_arv_proph(self, visit=None, maternal_status_helper=None):
        visit_list = ['2010', '2020', '2060', '2090',
                      '2120', '2180', '2240', '2300', '2360']

        if visit.visit_code in visit_list:
            infant_arv_proph_required = Reference.objects.filter(
                model=f'{self.app_label}.infantarvproph',
                identifier=visit.subject_identifier,
                report_datetime__lt=visit.report_datetime).order_by('-report_datetime').first()

            if not infant_arv_proph_required and visit.visit_code == '2010':
                return self.get_latest_maternal_visit_status(visit,
                                                             maternal_status_helper)
            elif infant_arv_proph_required:
                values = self.exists(
                    reference_name=f'{self.app_label}.infantarvprophmod',
                    subject_identifier=visit.subject_identifier,
                    report_datetime=infant_arv_proph_required.report_datetime,
                    field_name='dose_status')
                return values[0] != 'Permanently discontinued'
            return False

    def func_infant_heu(self, visit=None, maternal_status_helper=None, **kwargs):
        return self.get_latest_maternal_visit_status(visit,
                                                     maternal_status_helper)

    def func_infant_heu_require_pcr(self, visit=None,
                                    maternal_status_helper=None, **kwargs):

        visit_list = ['2010', '2020', '2060']
        return (visit.visit_code in visit_list
                and self.get_latest_maternal_visit_status(
                    visit, maternal_status_helper))

    def func_require_infant_elisa(self, visit=None,
                                  maternal_status_helper=None, **kwargs):
        return (visit.visit_code == '2180'
                and self.get_latest_maternal_visit_status(
                    visit, maternal_status_helper))

    def func_require_infant_dbs(self, visit=None,
                                maternal_status_helper=None, **kwargs):
        return (visit.visit_code == '2010'
                and self.get_latest_maternal_visit_status(
                    visit, maternal_status_helper))

    def func_show_infant_nvp_dispensing(self, visit=None,
                                        maternal_status_helper=None, **kwargs):
        maternal_rando_cls = django_apps.get_model(
            'td_maternal.maternalrando')
        maternal_rando = maternal_rando_cls.objects.filter(
            subject_identifier=visit.subject_identifier[:-3])
        if maternal_rando:
            return (self.get_latest_maternal_visit_status(visit, maternal_status_helper)
                    and maternal_rando[0].rx.strip('\n') == 'NVP')

    def func_show_nvp_adjustment_2010(self, visit,
                                      maternal_status_helper=None, **kwargs):
        if visit.visit_code == '2010':
            values = self.exists(
                reference_name=f'{self.app_label}.infantnvpdispensing',
                subject_identifier=visit.subject_identifier,
                report_datetime=visit.report_datetime,
                field_name='nvp_prophylaxis',
                timepoint='2000')
        return (self.get_latest_maternal_visit_status(
            visit, maternal_status_helper) and values[0] == YES)
