from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from ...predicates import InfantPredicates

app_label = 'td_infant'
pc = InfantPredicates()


@register()
class KaraboTbRuleGroup(CrfRuleGroup):

    require_tb_form = CrfRule(
        predicate=pc.func_show_karabo_tb_history,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[(f'{app_label}.karabotuberculosishistory')])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.infantvisit'


@register()
class KaraboOffstudyRuleGroup(CrfRuleGroup):

    show_offstudy = CrfRule(
        predicate=pc.show_karabo_offstudy,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[(f'{app_label}.karabooffstudy')])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.karabotuberculosishistory'
