from lsprotocol.types import CompletionItem, CompletionItemKind, InsertTextFormat


class Snippet(CompletionItem):
    def __init__(self, label: str, detail: str, insert_text: str, *args, **kwargs):
        super().__init__(
            label,
            *args,
            **kwargs,
            detail=detail,
            insert_text=insert_text,
            kind=CompletionItemKind.Snippet,
            insert_text_format=InsertTextFormat.Snippet
        )


python_snippets = (
    Snippet("pe_import", "Policy Engine variable import", "from policyengine_us.model_api import *"),
    Snippet(
        "pe_variable",
        "Policy Engine variable template",
        "\n".join(
            [
                "class ${1:variable}(Variable):",
                "\tvalue_type = ${2:float}",
                "\tentity = ${3:TaxUnit}",
                "\tdefinition_period = ${4:YEAR}",
                '\tlabel = "${5:label}"',
                "",
                "\tdef formula(${6:tax_unit}, period, parameters):",
                "\t\t${7:return 0}",
            ]
        ),
    ),
    Snippet(
        "pe_formula",
        "Policy Engine Variable formula definition",
        "def formula(${6:spm_unit}, period, parameters):\n\t${7:return 0}",
    ),
    Snippet("pe_spm", "Get Policy Engine SPM unit variable", 'spm_unit(${1:variable_name}, period)'),
    Snippet("pe_tax", "Get Policy Engine tax unit variable", 'tax_unit(${1:variable_name}, period)'),
    Snippet("pe_person", "Get Policy Engine person variable", 'person(${1:variable_name}, period)'),
    Snippet("pe_parameter", "Get Policy Engine parameter", "parameters(period).${1:gov.}${2}"),
)

pad = "  "
yaml_snippets = (
    Snippet(
        "pe_test",
        "Policy Engine test",
        "\n".join(
            [
                "- name: ${1:name}",
                pad + "period: ${2:2024}",
                pad + "input:",
                pad * 2 + "${3:input_variable}",
                pad + "output:",
                pad * 2 + "${4:output_variable}",
            ]
        ),
    ),
    Snippet(
        "pe_test_verbose",
        "Policy Engine test with multiple units",
        "\n".join(
            [
                "- name: ${1:name}",
                pad + "period: ${2:2024}",
                pad + "input:",
                pad * 2 + "people:",
                pad * 3 + "${3:head}:",
                pad * 4 + "${4:person_variable}",
                pad * 3 + "${5:spouse}:",
                pad * 4 + "${6:person_variable}",
                pad * 2 + "tax_units:",
                pad * 3 + "tax_unit:",
                pad * 4 + "${7:tax_unit_variable}",
                pad * 4 + "members: [${3}, ${5}]",
                pad * 2 + "spm_units:",
                pad * 3 + "spm_unit:",
                pad * 4 + "${8:spm_unit_variable}",
                pad * 4 + "members: [${3}, ${5}]",
                pad * 2 + "households:",
                pad * 3 + "household:",
                pad * 4 + "members: [${3}, ${5}]",
                pad * 2 + "marital_units:",
                pad * 3 + "marital_unit:",
                pad * 4 + "members: [${3}, ${5}]",
                pad + "output:",
                pad * 2 + "${9:output_variable}",
            ]
        ),
    ),
    Snippet(
        "pe_changelog",
        "Policy Engine changelog enty",
        "\n".join(
            [
                "- bump: ${1:patch}",
                pad + "changes:",
                pad * 2 + "${2:added}: ${3:description}",
            ]
        ),
    ),
    Snippet(
        "pe_basic_parameter",
        "Policy Engine value parameter",
        "\n".join(
            [
                "description: ${1:Description}",
                "values:",
                pad + "${2:2024-01-01}: ${3:0}",
                "metadata:",
                pad + "unit: ${4:currency-USD}",
                pad + "period: ${5:year}",
                pad + "label: ${6:label}",
                pad + "reference:",
                pad * 2 + "- title: ${7:refrence}",
                pad * 3 + "href: ${8:link}",
            ]
        ),
    ),
    Snippet("pe_period", "Policy Engine period", "${1:2024}-${2:01}-${3:01}"),
    Snippet(
        "pe_refrence",
        "Policy Engine refrence for a parameter",
        "\n".join(
            [
                "refrence:",
                pad + "- title: ${1:refrence}",
                pad * 2 + "href: ${2:link}",
            ]
        ),
    ),
)
