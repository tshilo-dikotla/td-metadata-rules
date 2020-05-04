from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from ...predicates import MaternalPredicates

app_label = 'td_maternal'
pc = MaternalPredicates()


@register()
class InfantClinicianNotesRuleGroup(CrfRuleGroup):

    maternal_ultrasound = CrfRule(
        predicate=pc.func_show_cliniciannotes_form,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.infantcliniciannotes'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.infantvisit'
