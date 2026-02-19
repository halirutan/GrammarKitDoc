# Section 3.4: PSI Customization — References

## Source File References

| Claim | Source | Verified |
|---|---|---|
| `private` rules skip AST node creation | `README.md:131-147` | Yes |
| `extends` makes AST shallow (collapsing) | `HOWTO.md:226-251`, `attributeDescriptions/extends.html` | Yes |
| `fake` rules generate only PSI classes, no parsing code | `README.md:141-142` | Yes |
| `fake` should not be combined with `private` | `README.md:142` | Yes |
| `mixin` attribute for implementation class | `attributeDescriptions/mixin.html` | Yes |
| Method mixins not supported in Gradle | `README.md:49-51` | Yes |
| `psiImplUtilClass` for static method injection | `HOWTO.md:323-341` | Yes |
| `methods` attribute: paths, renames, mix-ins | `attributeDescriptions/methods.html` | Yes |
| Path syntax: `/expr[0]`, `/expr[last]`, multi-level | `testData/generator/PsiAccessors.bnf` | Yes |
| `stubClass` shorthand for stub support | `HOWTO.md:346-381`, `attributeDescriptions/stubClass.html` | Yes |
| `<?>` in extends replaced with stubClass | `attributeDescriptions/stubClass.html` | Yes |
| `elementTypeFactory` required for stubs | `testData/generator/Stub.bnf` (observation) | Yes |
| `elementType=""` suppresses generation | `testData/generator/PsiGen.bnf` | Yes |
| Per-rule `psiPackage`/`psiImplPackage` overrides | `testData/generator/PsiAccessors.bnf` | Yes |
| `left` modifier: takes previous sibling as parent | `README.md:131-147` | Yes |
| `inner` should only be used with `left` | `README.md:146` | Yes |
| `private left` equals `private left inner` | `README.md:147` | Yes |
| Visitor generation respects extends hierarchy | `HOWTO.md:253-301` | Yes |

## External References

- Grammar-Kit HOWTO (PSI section): https://github.com/JetBrains/Grammar-Kit/blob/master/HOWTO.md
- IntelliJ Platform SDK: [PSI](https://plugins.jetbrains.com/docs/intellij/psi.html)
- IntelliJ Platform SDK: [Stub Indexes](https://plugins.jetbrains.com/docs/intellij/stub-indexes.html)
