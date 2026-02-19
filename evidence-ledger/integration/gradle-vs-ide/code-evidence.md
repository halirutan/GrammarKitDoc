# Section 4.2.2: Gradle vs IDE Generation — Code Evidence

## 1. IDE Generation

**Source: `src/org/intellij/grammar/actions/GenerateAction.java:51-202`**

IDE generation flow:
1. Commits all documents and saves files
2. Resolves target directory from `parserClass` attribute via `PackageIndex`
3. Runs `ParserGenerator.generate()` in a background task with progress
4. Reports results via notifications (file count, size, duration)
5. Refreshes virtual file system

Key advantages:
- **Two-pass generation**: First pass collects type information, second pass generates with full knowledge (enables method mixins)
- **Full Java resolution**: Uses `JavaHelper` to resolve types, generics, annotations
- **Real-time feedback**: Progress indicator, notification on completion
- **Live Preview integration**: Immediate testing via Ctrl-Alt-P

## 2. Gradle Plugin Limitations

**Source: `README.md:44-51`**

> Invoking the parser generator from an IDE as described above is the preferred way.
> Otherwise use [gradle-grammar-kit-plugin](https://github.com/JetBrains/gradle-grammar-kit-plugin) if the following limitations are not critical:
> * Method mixins are not supported (two-pass generation is not implemented)
> * Generic signatures and annotations may not be correct

## 3. Standalone CLI Generation

**Source: `HOWTO.md:400-424`**

```
java -jar grammar-kit.jar <output-dir> <grammars-and-dirs>
```

The `Main` class uses `LightPsi` for a minimal IntelliJ environment. Limited compared to IDE:
- No project context for type resolution
- No incremental generation
- No virtual file system integration

## 4. Feature Comparison

| Feature | IDE (Ctrl-Shift-G) | Gradle Plugin | CLI (grammar-kit.jar) |
|---|---|---|---|
| Two-pass generation | Yes | No | No |
| Method mixins | Yes | No | No |
| Generic signatures | Correct | May be incorrect | May be incorrect |
| Type annotations | Yes (ASM) | Limited | Limited |
| Live Preview | Yes | N/A | N/A |
| Target dir from source roots | Yes | Configured | Specified |
| Progress reporting | Yes | Gradle logging | Console output |
| Incremental builds | Partial (VFS refresh) | Gradle up-to-date | No |
| CI/CD compatible | No (requires IDE) | Yes | Yes |
| Reproducible | Depends on IDE state | Yes | Yes |

## 5. GenerateAction Target Directory Resolution

**Source: `GenerateAction.java:87-105`**

The IDE resolves output directories using `PackageIndex`:
```java
String parserClass = getRootAttribute(bnfFile, KnownAttribute.PARSER_CLASS);
VirtualFile target = getTargetDirectoryFor(project, file,
    StringUtil.getShortName(parserClass) + ".java",
    StringUtil.getPackageName(parserClass), true);
```

The Gradle plugin requires explicit configuration of output directories.

## 6. Fleet Support

**Source: `CHANGELOG.md:12-14`**

Grammar-Kit 2023.3 added Fleet IDE support:
- Context menu: Fleet: Generate Parser Code
- Context menu: Fleet: Generate JFlex Lexer
- Context menu: Fleet: Run JFlex Generator

**Source: `tests/org/intellij/grammar/FleetBnfGeneratorTest.java`**

Fleet generation tested separately, confirming a different code path.
