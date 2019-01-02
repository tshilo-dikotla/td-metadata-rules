from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register
from td_labs import pbmc_pl_panel, elisa_panel
from td_labs import viral_load_panel, pbmc_vl_panel

from ..predicates import Predicates


app_label = 'td_maternal'
pc = Predicates()


@register()
class MaternalRequisitionRuleGroup(RequisitionRuleGroup):

    require_vl_prn = RequisitionRule(
        predicate=pc.func_mother_pos_vl,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[viral_load_panel])

    require_pbmc_vl = RequisitionRule(
        predicate=pc.func_mother_pos,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[pbmc_vl_panel])

    require_pbmc_storage = RequisitionRule(
        predicate=pc.func_mother_neg,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[pbmc_pl_panel])

    require_elisa_status_ind = RequisitionRule(
        predicate=pc.func_show_elisa_requisition,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[elisa_panel])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.maternalvisit'
        requisition_model = f'{app_label}.maternalrequisition'
