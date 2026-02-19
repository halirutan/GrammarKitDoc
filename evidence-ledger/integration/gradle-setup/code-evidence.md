# Section 4.2.1: Gradle Setup — Code Evidence

## 1. Gradle Plugin Reference

**Source: `README.md:44-51`**

> Invoking the parser generator from an IDE as described above is the preferred way.
> Otherwise use [gradle-grammar-kit-plugin](https://github.com/JetBrains/gradle-grammar-kit-plugin) if the following limitations are not critical:
> * Method mixins are not supported (two-pass generation is not implemented)
> * Generic signatures and annotations may not be correct

## 2. Grammar-Kit's Own Build Configuration

**Source: `build.gradle.kts:1-54`**

```kotlin
plugins {
    java
    idea
    `maven-publish`
    signing
    alias(libs.plugins.intelliJPlatform)
    alias(libs.plugins.changelog)
}

dependencies {
    compileOnly(libs.annotations)
    testImplementation(libs.junit)
    intellijPlatform {
        create(providers.gradleProperty("platformType"), providers.gradleProperty("platformVersion"))
        bundledPlugins(providers.gradleProperty("platformBundledPlugins").map { it.split(',') })
        testFramework(TestFrameworkType.Platform)
        testFramework(TestFrameworkType.Plugin.Java)
    }
}

sourceSets {
    main { java.srcDirs("src", "gen"); resources.srcDirs("resources") }
    test { java.srcDirs("tests"); resources.srcDirs("testData") }
}
```

## 3. Version Properties

**Source: `gradle.properties:1-35`**

```properties
pluginGroup = org.jetbrains
pluginName = Grammar-Kit
pluginVersion = 2023.3-dev
pluginSinceBuild = 233
platformType = IU
platformVersion = 2023.3.8
platformBundledPlugins = com.intellij.diagram, com.intellij.java, com.intellij.copyright
gradleVersion = 8.14.2
javaVersion = 17
```

Key: Java 17 required, targets IntelliJ 2023.3+.

## 4. Grammar-Kit Jar for Standalone Use

**Source: `build.gradle.kts:133-145`**

```kotlin
val buildGrammarKitJar by tasks.registering(Jar::class) {
    dependsOn("assemble")
    archiveBaseName = "grammar-kit"
    destinationDirectory = file(artifactsPath)
    manifest { from("$rootDir/resources/META-INF/MANIFEST.MF") }
    from(sourceSets.main.get().output)
    from(file("$rootDir/src/org/intellij/grammar/parser/GeneratedParserUtilBase.java")) {
        into("/templates")
    }
}
```

The standalone jar includes `GeneratedParserUtilBase.java` as a template.

## 5. Maven Central Publishing

**Source: `build.gradle.kts:203-246`**

Grammar-Kit is published to Maven Central:
- Group: `org.jetbrains`
- Artifact: `Grammar-Kit`
- Includes javadoc and sources jars

## 6. Command-Line Generation

**Source: `HOWTO.md:400-424`**

```bash
java -jar grammar-kit.jar <output-dir> <grammars-and-dirs>
# or with explicit classpath:
java -cp grammar-kit.jar;<deps> org.intellij.grammar.Main <output-dir> <grammars-and-dirs>
```

The `Main` class (`src/org/intellij/grammar/Main.java`) provides the entry point for CLI generation.

## 7. Gradle Grammar-Kit Plugin

**Source: README.md reference to https://github.com/JetBrains/gradle-grammar-kit-plugin**

The separate `gradle-grammar-kit-plugin` provides:
- `generateParser` task for BNF grammar compilation
- `generateLexer` task for JFlex lexer generation
- Configurable source and output directories
- Task dependency management

Limitations vs IDE generation:
- No method mixins (no two-pass generation)
- Generic signatures and annotations may not be correct
