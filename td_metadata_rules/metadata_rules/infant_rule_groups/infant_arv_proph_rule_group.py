from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from ...predicates import InfantPredicates

app_label = 'td_infant'
pc = InfantPredicates()


@register()
class InfantArvProphRuleGroup(CrfRuleGroup):
    arv_proph = CrfRule(
        predicate=pc.func_show_infant_arv_proph,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[(f'{app_label}.infantarvproph')])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.infantvisit'
