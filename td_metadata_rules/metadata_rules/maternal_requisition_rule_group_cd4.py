from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register
from td_labs import cd4_panel

from ..predicates import Predicates


app_label = 'td_maternal'
pc = Predicates()


@register()
class MaternalRequisitionRuleGroupCD4(RequisitionRuleGroup):

    require_vl_prn = RequisitionRule(
        predicate=pc.func_require_cd4,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[cd4_panel])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.maternalinterimidcc'
        requisition_model = f'{app_label}.maternalrequisition'
