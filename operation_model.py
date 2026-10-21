import re

from chemdataextractor.model import StringType, ModelType, Compound

try:
    from chemdataextractor.model.units.temperature import TemperatureModel
except ImportError:
    from chemdataextractor.model import TemperatureModel

try:
    from chemdataextractor.model.units.time import TimeModel
except ImportError:
    from chemdataextractor.model import TimeModel

try:
    from chemdataextractor.parse import I
    from chemdataextractor.parse.actions import join
except ImportError:
    from chemdataextractor.parse.elements import I
    from chemdataextractor.parse.actions import join


# Generated from the annotated operation triggers. ORDER IS SIGNIFICANT: the
# alternation is a First(), so the list runs longest-trigger-first and the most
# specific match wins.
_OPERATION_SPECIFIER_TERMS = ['used a planetary ball mill',
 'evaporated by heating',
 'allowed to react',
 'After a period',
 'crystallized hydrothermally',
 'hydrothermally synthesized',
 'hydrothermal processing',
 'ultrasonically vibrated',
 'hydrothermal treatment',
 'hydrothermally treated',
 'treated hydrothermally',
 'thermal decomposition',
 'hydrothermally treat',
 'magnetically stirred',
 'stirred continuously',
 'ultrasonic treatment',
 'continuous stirring',
 'stirring conditions',
 'continues stirring',
 'constant stirring',
 'magnetic stirring',
 'vigorous stirring',
 'ultra sonication',
 'air calcination',
 'gentle stirring',
 'air calcinated',
 'kept stirring',
 'aged further',
 'air calcined',
 'freeze dried',
 'freeze dryer',
 'heat treated',
 'pre oxidized',
 'carried out',
 'dried again',
 'oven dried',
 'air dried',
 'pre dried',
 'pre fired',
 'crystallized-hydrothermally',
 'hydrothermally-synthesized',
 'used-a-planetary-ball-mill',
 'hydrothermal-processing',
 'ultrasonically-vibrated',
 'hydrothermal-treatment',
 'hydrothermally-treated',
 'treated-hydrothermally',
 'evaporated-by-heating',
 'thermal-decomposition',
 'hydrothermally-treat',
 'magnetically-stirred',
 'stirred-continuously',
 'ultrasonic-treatment',
 'continuous-stirring',
 'stirring-conditions',
 'continues-stirring',
 'constant-stirring',
 'magnetic-stirring',
 'vigorous-stirring',
 'allowed-to-react',
 'ultra-sonication',
 'air-calcination',
 'Crystallization',
 'gentle-stirring',
 'ultrasonication',
 'After-a-period',
 'air-calcinated',
 'kept-stirring',
 'aged-further',
 'air-calcined',
 'freeze-dried',
 'freeze-dryer',
 'heat-treated',
 'pre-oxidized',
 'ultrafreezer',
 'calcinating',
 'calcination',
 'carried-out',
 'centrifuged',
 'dried-again',
 'evaporation',
 'calcinated',
 'evaporated',
 'evaporator',
 'maintained',
 'maturation',
 'oven-dried',
 'pretreated',
 'sonication',
 'ultrasonic',
 'agitation',
 'air-dried',
 'calcining',
 'degassing',
 'digesting',
 'dissolved',
 'increased',
 'pre-dried',
 'pre-fired',
 'sonicated',
 'suspended',
 'underwent',
 'agitated',
 'annealed',
 'calcined',
 'degassed',
 'digested',
 'elevated',
 'immersed',
 'maintain',
 'refluxed',
 'remained',
 'sonicate',
 'stirring',
 'exposed',
 'heating',
 'ignited',
 'leached',
 'milling',
 'reacted',
 'removed',
 'steamed',
 'stirred',
 'treated',
 'cooled',
 'drying',
 'frozen',
 'heated',
 'placed',
 'raised',
 'reflux',
 'soaked',
 'aging',
 'dried',
 'fired',
 'aged',
 'held',
 'kept',
 'left',
 'rise',
 'stir',
 'dry']

def phrase_expression(term):
    tokens = [token for token in re.split(r"\s+", term.strip()) if token]

    if not tokens:
        raise ValueError("Empty operation term.")

    expression = I(tokens[0])

    for token in tokens[1:]:
        expression = expression + I(token)

    return expression


def operation_expression(terms):
    expressions = [phrase_expression(term) for term in terms]

    if not expressions:
        raise ValueError("No operation terms provided.")

    expression = expressions[0]

    for next_expression in expressions[1:]:
        expression = expression | next_expression

    return expression


temperature_specifier_expression = operation_expression(_OPERATION_SPECIFIER_TERMS).add_action(join)
time_specifier_expression = operation_expression(_OPERATION_SPECIFIER_TERMS).add_action(join)


class OperationTemperature(TemperatureModel):
    """
    Snowball2 model for operation-related temperatures.

    Target entities:
        specifier -> annotated operation_verb_text_span
        raw_value -> temperature_value
        raw_units -> temperature_unit
    """

    specifier = StringType(
        parse_expression=temperature_specifier_expression,
        required=True,
        contextual=False,
        updatable=True,
    )

    # Never populated by this framework: no compound/material entity is built.
    # Kept because Snowball2 expands the model's nested fields and its candidate
    # generation refers to compound__* tags; removing it breaks the library.
    compound = ModelType(
        Compound,
        required=False,
        contextual=True,
    )


class OperationTime(TimeModel):
    """
    Snowball2 model for operation-related durations/times.

    Target entities:
        specifier -> annotated operation_verb_text_span
        raw_value -> time_value
        raw_units -> time_unit
    """

    specifier = StringType(
        parse_expression=time_specifier_expression,
        required=True,
        contextual=False,
        updatable=True,
    )

    # See the note on OperationTemperature.compound.
    compound = ModelType(
        Compound,
        required=False,
        contextual=True,
    )
