from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from ...predicates import InfantPredicates

app_label = 'td_infant'
pc = InfantPredicates()


@register()
class InfantNvpDispensingRuleGroup(CrfRuleGroup):
    infant_nvp_dispensing = CrfRule(
        predicate=pc.func_show_infant_nvp_dispensing,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[(f'{app_label}.infantnvpdispensing')])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.infantvisit'
