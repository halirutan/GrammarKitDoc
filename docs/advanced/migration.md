# Migration Guide

Grammar-Kit has evolved significantly since its initial release in 2012. This page documents the changes that may require updates to your grammar, generated code, or build configuration when you upgrade.

## Version History

| Version | Year | Key Changes |
|---|---|---|
| 1.0 | 2012 | Initial release: highlighting, completion, navigation, parser generation |
| 1.1.0 | 2013 | Live Preview, `parserUtilClass` (renamed from `stubParserClass`), StubIndex support |
| 1.1.5 | 2013 | `recoverWhile` (renamed from `recoverUntil`), `#auto` recovery |
| 1.2.0 | 2014 | `generate` attribute supersedes individual `generateXXX` attributes, compact variable names |
| 1.3.0 | 2015 | "Upper" rules, `visitor-value` option |
| 1.4.0 | 2015 | `hooks` attribute, `elementTypes` for fake rules |
| 1.5.0 | 2016 | Expression parsing fixes, `psi-classes-map` option |
| 2017.1 | 2017 | Year-based versioning, merged AST/PSI trees, dash-separated rules |
| 2017.1.6 | 2018 | Java 8 lambdas (`generate=[java="8"]`), token-sets |
| 2019.1 | 2019 | `extraRoot` attribute, method mixins with generics |
| 2020.3 | 2020 | Default Java version switched to 11, `fqn` option, type annotations |
| 2022.3 | 2022 | GitHub Actions CI, MavenCentral publishing |
| 2023.3 | 2023 | Fleet support, JFlex 1.9.2 |

## Renamed Attributes

Several attributes were renamed in early versions. The old names still appear in older grammars and tutorials. If you are working with a grammar written before 2014, check for these:

| Old Name | New Name | Version Changed |
|---|---|---|
| `recoverUntil` | `recoverWhile` | 1.1.5 |
| `stubParserClass` | `parserUtilClass` | 1.1.0 |
| `methodRenames` | `methods` attribute (using `name="child"` syntax) | 1.1.6 |

Update your grammar to use the current names. The old names may still work in some versions, but they are not guaranteed to be supported going forward.

## Deprecated Attributes

Starting with version 1.2.0, the consolidated `generate` attribute supersedes several standalone attributes:

- `generateFirstCheck`: use `generate=[first-check=N]`
- `generatePsi`: use `generate=[psi="yes"]` or `generate=[psi="no"]`
- `generateTokens`: use `generate=[tokens="yes"]`
- `generateTokenAccessors`: use `generate=[token-accessors="yes"]`
- `extendedPin`: use `generate=[extended-pin="yes"]`

The standalone attributes still work but are considered deprecated. Prefer the `generate` attribute for new grammars, and consolidate existing attributes when you update a grammar.

For a full list of attributes and their current syntax, see [Attributes System](../code-generation/attributes.md).

## Java Version Changes

Grammar-Kit targets a specific Java version when generating code, controlled by `generate=[java="N"]`.

Before version 2020.3, the default was Java 6 (later 8). Starting with 2020.3, the default is Java 11. This affects the generated code in several ways:

- Lambdas appear in generated code by default (Java 8+)
- Method references are used where applicable
- `@Override` annotations are added on visitor methods
- Type annotations (via ASM-based generation) are supported

If you need to support an older Java version, set the target explicitly:

```bnf
{
  generate=[java="8"]
}
```

!!! warning
    If you upgrade Grammar-Kit and regenerate without setting an explicit Java target, the output may change from anonymous classes to lambdas. This is not a functional problem, but it produces a large diff in version control.

## Platform Compatibility

The current Grammar-Kit version requires:

- IntelliJ Platform 2023.3 or later (`pluginSinceBuild = 233`)
- Java 17 for building Grammar-Kit itself

Your generated parsers do not require Java 17. The Java version requirement applies to the Grammar-Kit plugin, not to the code it generates. The generated code's Java level is controlled by the `generate=[java="N"]` attribute.

## Notable API Changes

### Merged AST and PSI Trees (2017.1)

Version 2017.1 introduced merged AST and PSI trees, allowing `CompositePsiElement` inheritors. If your PSI implementation classes extend `CompositePsiElement` directly, this change should be transparent. If you relied on the separation between AST and PSI nodes, you may need to update code that traverses the tree.

### Java Extensions Moved (2021.1)

Java-related extensions were moved to an optional configuration file. If your plugin uses Java-related PSI extensions from Grammar-Kit, check that the optional dependency is declared in your `plugin.xml`.

### Constructor Injection Removed (2022.3.1)

Constructor injection was removed for IntelliJ 2023.1 compatibility. If your PSI classes relied on constructor injection, switch to the standard pattern of using `IElementType` constructors.

## Build System Changes

Version 2022.3 modernized the build infrastructure:

- CI moved from Travis CI to GitHub Actions
- Artifacts published to MavenCentral (in addition to the plugin marketplace)
- `gradle-changelog-plugin` integration for release management
- Dependabot integration for dependency updates

If you reference Grammar-Kit as a dependency in your build, update your repository URLs accordingly. MavenCentral coordinates are the preferred way to resolve the dependency.

## Upgrading a Grammar

When upgrading to a new Grammar-Kit version:

1. Read the changelog for all versions between your current and target version. Look for changes to defaults, renamed attributes, and behavior changes.
2. Regenerate all parsers and lexers.
3. Compare the generated output with version control. Look for unexpected changes in method signatures, import statements, or code patterns.
4. Run your parser test suite. If tests fail, check whether the failure is due to a Grammar-Kit behavior change or a pre-existing issue that the new version surfaces.
5. Update deprecated attributes to their current equivalents.

!!! tip
    The `KnownAttribute.java` file in the Grammar-Kit source is the single source of truth for all supported attributes and their defaults. If you are unsure whether an attribute is supported in your version, check that file.

For issues you encounter during migration, see [Common Issues](common-issues.md). For techniques to investigate unexpected parser behavior after an upgrade, see [Debugging Techniques](debugging.md).
