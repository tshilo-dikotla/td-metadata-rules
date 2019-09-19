from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register
from edc_metadata_rules import RequisitionRuleGroup, RequisitionRule
from td_labs import karabo_wb_pbmc_pl_panel, infant_paxgene_panel, karabo_pbmc_pl_panel

from ...predicates import InfantPredicates

app_label = 'td_infant'
pc = InfantPredicates()


@register()
class KaraboTbRuleGroup(CrfRuleGroup):

    require_tb_form = CrfRule(
        predicate=pc.func_show_karabo_tb_form,
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


@register()
class KaraboRequisitionRuleGroup(RequisitionRuleGroup):

    show_infant_paxgene = RequisitionRule(
        predicate=pc.func_show_infant_paxgene_panel,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[infant_paxgene_panel])

    show_karabo_pbmc_pl = RequisitionRule(
        predicate=pc.func_show_karabo_pbmc_pl_panel,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[karabo_pbmc_pl_panel])

    show_karabo_wb_pbmc_pl_panel = RequisitionRule(
        predicate=pc.func_show_karabo_wb_pbmc_pl_panel,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[karabo_wb_pbmc_pl_panel])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.infantvisit'
        requisition_model = f'{app_label}.infantrequisition'
