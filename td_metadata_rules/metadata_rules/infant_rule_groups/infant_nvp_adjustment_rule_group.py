from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from ...predicates import InfantPredicates

app_label = 'td_infant'
pc = InfantPredicates()


@register()
class InfantNvpAdjustmentRuleGroup(CrfRuleGroup):
    nvp_adjustment = CrfRule(
        predicate=pc.func_show_nvp_adjustment_2010,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[(f'{app_label}.infantnvpadjustment')])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.infantvisit'
