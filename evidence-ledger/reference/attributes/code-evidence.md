# Section 6.1: Attribute Reference — Code Evidence

## Complete Attribute Catalog

**Source: `src/org/intellij/grammar/KnownAttribute.java:29-72`**

### Global Attributes

| Attribute | Type | Default | HTML Doc |
|---|---|---|---|
| `classHeader` | String | `"// This is a generated file..."` | classHeader.html |
| `generate` | ListValue | `[]` | generate.html |
| `generatePsi` | Boolean | `true` | generatePsi.html |
| `generateTokens` | Boolean | `true` | generateTokens.html |
| `generateTokenAccessors` | Boolean | `false` | generateTokenAccessors.html |
| `generateFirstCheck` | Integer | `2` | generateFirstCheck.html |
| `extendedPin` | Boolean | `true` | extendedPin.html |
| `parserImports` | ListValue | `[]` | parserImports.html |
| `psiClassPrefix` | String | `""` | psiClassPrefix.html |
| `psiImplClassSuffix` | String | `"Impl"` | psiImplClassSuffix.html |
| `psiTreeUtilClass` | String | `"com.intellij.psi.util.PsiTreeUtil"` | psiTreeUtilClass.html |
| `psiPackage` | String | `"generated.psi"` | psiPackage.html |
| `psiImplPackage` | String | `"generated.psi.impl"` | psiImplPackage.html |
| `psiVisitorName` | String | `"Visitor"` | psiVisitorName.html |
| `psiImplUtilClass` | String | `null` | psiImplUtilClass.html |
| `tokenTypeClass` | String | `"...IElementType"` | tokenTypeClass.html |
| `parserClass` | String | `"generated.GeneratedParser"` | parserClass.html |
| `parserUtilClass` | String | `"...GeneratedParserUtilBase"` | parserUtilClass.html |
| `elementTypeHolderClass` | String | `"generated.GeneratedTypes"` | elementTypeHolderClass.html |
| `elementTypePrefix` | String | `""` | elementTypePrefix.html |
| `tokenTypeFactory` | String | `null` | tokenTypeFactory.html |
| `tokens` | ListValue | `[]` | tokens.html |

### Rule-Level Attributes

| Attribute | Type | Default | HTML Doc |
|---|---|---|---|
| `extends` | String | `"...ASTWrapperPsiElement"` | extends.html |
| `implements` | ListValue | `["...PsiElement"]` | implements.html |
| `elementType` | String | `null` | elementType.html |
| `elementTypeClass` | String | `"...IElementType"` | elementTypeClass.html |
| `elementTypeFactory` | String | `null` | elementTypeFactory.html |
| `fallbackStubElementType` | String | `"...IStubElementType"` | fallbackStubElementType.html |
| `pin` | Object | `-1` | pin.html |
| `mixin` | String | `null` | mixin.html |
| `recoverWhile` | String | `null` | recoverWhile.html |
| `name` | String | `null` | name.html |
| `extraRoot` | Boolean | `false` | extraRoot.html |
| `rightAssociative` | Boolean | `false` | rightAssociative.html |
| `consumeTokenMethod` | String | `"consumeToken"` | consumeTokenMethod.html |
| `stubClass` | String | `null` | stubClass.html |
| `methods` | ListValue | `[]` | methods.html |
| `hooks` | ListValue | `[]` | hooks.html |

## HTML Description Files

**Source: `resources/messages/attributeDescriptions/` — 38 files total**

Complete list:
classHeader.html, consumeTokenMethod.html, elementType.html, elementTypeClass.html, elementTypeFactory.html, elementTypeHolderClass.html, elementTypePrefix.html, extendedPin.html, extends.html, extraRoot.html, fallbackStubElementType.html, generate.html, generateFirstCheck.html, generatePsi.html, generateTokenAccessors.html, generateTokens.html, hooks.html, implements.html, methods.html, mixin.html, name.html, parserClass.html, parserImports.html, parserUtilClass.html, pin.html, psiClassPrefix.html, psiImplClassSuffix.html, psiImplPackage.html, psiImplUtilClass.html, psiPackage.html, psiTreeUtilClass.html, psiVisitorName.html, recoverWhile.html, rightAssociative.html, stubClass.html, tokens.html, tokenTypeClass.html, tokenTypeFactory.html

## `generate` Attribute Sub-Options

**Source: `attributeDescriptions/generate.html`**

| Option | Values | Default | Category |
|---|---|---|---|
| `psi` | yes, no | **yes** | PSI |
| `psi-classes-map` | yes, no | **no** | PSI |
| `psi-factory` | yes, no | **yes** | PSI |
| `visitor` | yes, no | **yes** | PSI |
| `visitor-value` | void, type name | **void** | PSI |
| `fqn` | no, yes | **no** | PSI |
| `elements` | yes, no | **yes** | Types |
| `element-case` | lower, upper, as-is | **upper** | Types |
| `tokens` | yes, no | **yes** | Types |
| `token-case` | lower, upper, as-is | **upper** | Types |
| `token-sets` | yes, no | **no** | Types |
| `exact-types` | all, no, tokens, elements | **no** | Types |
| `token-accessors` | yes, no | **no** | PSI |
| `names` | short, long, classic | **short** | Parser |
| `first-check` | positive number | **2** | Parser |
| `java` | 6, 8, 11, etc. | **11** | Generator |

## Pattern Attribute Syntax

**Source: `README.md:122-129`**

Attributes with patterns use regex matching against rule names:
```bnf
{
  extends(".*_expr")=expr
  pin(".*_list(?:_\\d+)*")=1
}
```

Pattern attributes apply to all rules whose names match the regex.
