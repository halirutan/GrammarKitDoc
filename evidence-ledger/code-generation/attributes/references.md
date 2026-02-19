# Section 3.1: Attributes System — References

## Source File References

| Claim | Source | Verified |
|---|---|---|
| All attributes defined as static `KnownAttribute<T>` fields | `KnownAttribute.java:29-72` | Yes |
| Global vs rule scope via `boolean global` parameter | `KnownAttribute.java:79-81` | Yes |
| `generate` attribute supersedes individual generateXXX | `attributeDescriptions/generate.html` | Yes |
| Pattern-based attributes use regex syntax | `README.md:122-129` | Yes |
| Attribute descriptions loaded from HTML resources | `KnownAttribute.java:119-127` | Yes |
| 38 attribute description HTML files exist | `resources/messages/attributeDescriptions/` | Yes |
| `ListValue` extends `LinkedList<Pair<String, String>>` | `KnownAttribute.java:133-166` | Yes |
| Single string auto-converted to ListValue | `KnownAttribute.java:108` | Yes |
| Default `parserClass` is `"generated.GeneratedParser"` | `KnownAttribute.java:44` | Yes |
| Default `extends` is `ASTWrapperPsiElement` | `KnownAttribute.java:55` | Yes |
| Default `psiImplClassSuffix` is `"Impl"` | `KnownAttribute.java:39` | Yes |
| Default `generateFirstCheck` is `2` | `KnownAttribute.java:35` | Yes |
| `extendedPin` defaults to `true` | `KnownAttribute.java:36` | Yes |
| Three naming styles: short, long, classic | `Names.java:13-63` | Yes |
| Four casing options: LOWER, UPPER, AS_IS, CAMEL | `Case.java:14-27` | Yes |
| Default Java version is 11 | `GenOptions.java:131` | Yes |

## External References

- Grammar-Kit README (Attributes section): https://github.com/JetBrains/Grammar-Kit/blob/master/README.md
- Grammar-Kit HOWTO: https://github.com/JetBrains/Grammar-Kit/blob/master/HOWTO.md
- All 38 HTML attribute descriptions at `resources/messages/attributeDescriptions/`
