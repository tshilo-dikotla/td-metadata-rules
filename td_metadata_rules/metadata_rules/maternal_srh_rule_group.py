from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from ..predicates import MaternalPredicates

app_label = 'td_maternal'
pc = MaternalPredicates()


@register()
class MaternalSrhServicesRuleGroup(CrfRuleGroup):
    srh_services = CrfRule(
        predicate=pc.func_show_srh_services_utilization,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[(f'{app_label}.maternalsrh')])

    class Meta:
        app_label = app_label
