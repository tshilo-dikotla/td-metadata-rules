from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import YES
from edc_metadata_rules import PredicateCollection
from edc_reference import LongitudinalRefset, site_reference_configs
from edc_reference.models import Reference

from td_maternal.helper_classes import MaternalStatusHelper

from .maternal_predicates import MaternalPredicates


class InfantPredicates(PredicateCollection):

    app_label = 'td_infant'
    visit_model = f'{app_label}.infantvisit'
    karabo_tb_model = f'{app_label}.karabotuberculosishistory'
    karabo_consent_model = f'{app_label}.karabosubjectconsent'
    karabo_screening_model = f'{app_label}.karabosubjectscreening'
    registered_subject_model = 'edc_registration.registeredsubject'

    @property
    def registered_subject_model_cls(self):
        return django_apps.get_model(self.registered_subject_model)

    @property
    def karabo_tb_model_cls(self):
        return django_apps.get_model(self.karabo_tb_model)

    @property
    def karabo_consent_model_cls(self):
        return django_apps.get_model(self.karabo_consent_model)

    @property
    def karabo_screening_model_cls(self):
        return django_apps.get_model(self.karabo_screening_model)

    def get_latest_maternal_visit_status(self, visit=None, maternal_status_helper=None):
        status = False
        maternal_visit = Reference.objects.filter(
            identifier=visit.subject_identifier[:-3],
            timepoint='2000M')
        if maternal_visit:
            maternal_visit = maternal_visit[0]
            mpc = MaternalPredicates()
            maternal_status_helper = maternal_status_helper or MaternalStatusHelper(
                maternal_visit)
            status = mpc.func_mother_pos(
                maternal_visit, maternal_status_helper)
        return status

    def func_show_infant_arv_proph(self, visit=None, maternal_status_helper=None, **kwargs):
        visit_list = ['2010', '2020', '2060', '2090',
                      '2120', '2180', '2240', '2300', '2360']
        # check visit code
        if visit.visit_code in visit_list:
            infant_arv_proph_required = Reference.objects.filter(
                model=f'{self.app_label}.infantarvproph',
                identifier=visit.subject_identifier,
                report_datetime__lt=visit.report_datetime).order_by('-report_datetime').first()

            if not infant_arv_proph_required and visit.visit_code == '2010':
                return self.get_latest_maternal_visit_status(visit,
                                                             maternal_status_helper)
            elif infant_arv_proph_required:
                infant_arv_proph_cls = django_apps.get_model(
                    'td_infant.infantarvproph')
                try:
                    infant_arv_proph_model = infant_arv_proph_cls.objects.get(
                        subject_identifier=visit.subject_identifier,
                        report_datetime=infant_arv_proph_required.report_datetime)
                except infant_arv_proph_cls.DoesNotExist:
                    return False
                else:
                    arv_proph_list = infant_arv_proph_model.infantarvprophmod_set.all()
                    for arv in arv_proph_list:
                        if arv.dose_status == 'Permanently discontinued':
                            return False
                    return True

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
        maternal_rando = Reference.objects.filter(
            model='td_maternal.maternalrando',
            report_datetime__lt=visit.report_datetime,
            identifier=visit.subject_identifier[:-3]).order_by(
            '-report_datetime').last()

        if maternal_rando:
            nvp_refsets = LongitudinalRefset(
                name='td_maternal.maternalrando',
                visit_model='td_maternal.maternalvisit',
                reference_model_cls=django_apps.get_model(
                    site_reference_configs.get_reference_model('td_maternal.maternalvisit')),
                subject_identifier=visit.subject_identifier[:-3],
                report_datetime=maternal_rando.report_datetime,
            )

            value = nvp_refsets.fieldset(
                field_name='rx').all().values

            return (self.get_latest_maternal_visit_status(
                visit, maternal_status_helper)
                and value[0].strip('\n') == 'NVP')
        return False

    def func_show_nvp_adjustment_2010(self, visit,
                                      maternal_status_helper=None, **kwargs):

        if visit.visit_code == '2010':

            previous_nvp_dispensing = Reference.objects.filter(
                model=f'{self.app_label}.infantnvpdispensing',
                identifier=visit.subject_identifier,
                report_datetime__lt=visit.report_datetime).order_by(
                '-report_datetime').first()

            if previous_nvp_dispensing:
                value = self.exists(
                    reference_name=f'{self.app_label}.infantnvpdispensing',
                    subject_identifier=visit.subject_identifier,
                    report_datetime=previous_nvp_dispensing.report_datetime,
                    field_name='nvp_prophylaxis',
                    timepoint='2000')
                return (self.get_latest_maternal_visit_status(
                    visit, maternal_status_helper) and value[0] == YES)
        return False

    def show_karabo_offstudy(self, visit, **kwargs):
        if visit.visit_code == '2180':
            return True
        value = self.exists(
            reference_name=f'{self.app_label}.karabotuberculosishistory',
            subject_identifier=visit.subject_identifier,
            field_name='put_offstudy',
            timepoint=visit.visit_code)
        return visit.appointment.timepoint < 180 and value[0] == YES

    def func_show_karabo_tb_history(self, visit, **kwargs):
        relative_identifier = None
        if not self.show_karabo_offstudy(visit=visit):
            try:
                relative_identifier = self.registered_subject_model_cls.objects.get(
                    subject_identifier=visit.appointment.subject_identifier).relative_identifier
            except self.registered_subject_model_cls.DoesNotExist:
                raise ValidationError(
                    f'Registered subject for {visit.appointment.subject_identifier} '
                    'not found.')
            else:
                return self.check_for_karabo_consent(
                    relative_identifier=relative_identifier)

    def check_for_karabo_consent(self, relative_identifier=None):

        try:
            karabo_screening = self.karabo_screening_model_cls.objects.get(
                subject_identifier=relative_identifier)
        except self.karabo_screening_model_cls.DoesNotExist:
            return False
        else:
            if karabo_screening.is_eligible:
                try:
                    self.karabo_consent_model_cls.objects.get(
                        subject_identifier=relative_identifier)
                    return True
                except self.karabo_consent_model_cls.DoesNotExist:
                    raise ValidationError(
                        'Participant is eligible for Karabo sub-study, please complete '
                        'Karabo subject consent.')
            return False
