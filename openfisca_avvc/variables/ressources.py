from openfisca_core.periods import MONTH
from openfisca_core.variables import Variable

from openfisca_avvc.entities import Person, Household


#Liste des types de ressources déclarables par le bénéficiaire

class salaire(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    default_value = 0
    label = "Revenu d'activité salarié"

class revenu_tns(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    default_value = 0
    label = "Revenu travailleur non salarié mensuel"

class indemnite_chomage(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    default_value = 0
    label = "indeminitée chomage"

class ij_parent(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    default_value = 0
    label = "IJ de maternité, paternité, adoption"

class autre_ij_ss(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    default_value = 0
    label = "autres IJ de sécurité sociale"

class remun_esat(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    default_value = 0
    label = "rémunération garantie pour les travailleurs en esat"
    
class pension_retraite(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    default_value = 0
    label = "pension de retraire"

class autres_ressources(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH
    default_value = 0
    label = "autre ressource"


class total_ressources_personne(Variable):
    value_type = float
    entity = Person
    definition_period = MONTH

    def formula(person,period):
        return (
            + person("salaire", period)
            + person("revenu_tns", period)
            + person("indemnite_chomage", period)
            + person("ij_parent", period)
            + person("autre_ij_ss", period)
            + person("remun_esat", period)
            + person("pension_retraite", period)
            + person("autres_ressources", period)
            )

class total_ressources_foyer(Variable):
    value_type = float
    entity = Household
    definition_period = MONTH

    def formula(household, period):
        return household.members("total_ressources_personne", period)