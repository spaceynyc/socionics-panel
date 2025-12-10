import fitz
import re

doc = fitz.open('SCS Types.pdf')
full_text = ""
for page in doc:
    full_text += page.get_text() + "\n"

# Find type patterns
type_pattern = r'(ILE|SEI|ESE|LII|EIE|LSI|SLE|IEI|SEE|ILI|LIE|ESI|IEE|SLI|LSE|EII)\s*\([A-Z]{4,5}\)'
types_found = re.findall(type_pattern, full_text)
print("Types found:", types_found)

# Find function patterns  
func_pattern = r'(Leading|Creative|Vulnerable|PoLR|Role|Suggestive|Mobilizing|Ignoring|Demonstrative)\s+(Ne|Ni|Se|Si|Te|Ti|Fe|Fi)[+-]?'
funcs_found = re.findall(func_pattern, full_text)
print("\nFunctions found:")
for f in funcs_found:
    print(f"  {f[0]}: {f[1]}")
