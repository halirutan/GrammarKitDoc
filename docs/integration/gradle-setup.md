# Gradle Plugin Setup

The [gradle-grammar-kit-plugin](https://github.com/JetBrains/gradle-grammar-kit-plugin) automates parser and lexer generation in your Gradle build. It provides `generateParser` and `generateLexer` tasks that invoke Grammar-Kit and JFlex without a running IDE, making it suitable for CI/CD pipelines and team builds.

!!! warning
    The Gradle plugin has two limitations compared to IDE generation: method mixins are not supported (two-pass generation is not implemented), and generic signatures and annotations may not be correct. If your grammar uses the `mixin` attribute, generate from the IDE instead. See [Gradle vs IDE Generation](gradle-vs-ide.md) for a detailed comparison.

## Plugin Installation

Apply the plugin in your `build.gradle.kts`. The plugin is published to the Gradle Plugin Portal:

```kotlin
plugins {
    id("org.jetbrains.intellij.platform") version "..."
    id("org.jetbrains.grammarkit") version "..."
}
```

Configure your IntelliJ Platform dependency as usual. Grammar-Kit's own build uses these settings as a reference:

```kotlin
dependencies {
    intellijPlatform {
        create(
            providers.gradleProperty("platformType"),
            providers.gradleProperty("platformVersion")
        )
        bundledPlugins(
            providers.gradleProperty("platformBundledPlugins")
                .map { it.split(',') }
        )
    }
}
```

Set the Java version and platform target in `gradle.properties`. Grammar-Kit requires Java 17 and targets IntelliJ 2023.3 or later:

```properties
javaVersion = 17
platformType = IU
platformVersion = 2023.3.8
platformBundledPlugins = com.intellij.java
```

## Generation Tasks

The plugin provides two tasks: `generateParser` for BNF grammars and `generateLexer` for JFlex files.

Configure `generateParser` to point at your grammar file and specify where to write the output:

```kotlin
tasks {
    generateParser {
        sourceFile.set(file("src/main/grammar/My.bnf"))
        targetRootOutputDir.set(file("src/main/gen"))
        pathToParser.set("com/example/parser/MyParser.java")
        pathToPsiRoot.set("com/example/psi")
    }
}
```

Configure `generateLexer` similarly for your JFlex file:

```kotlin
tasks {
    generateLexer {
        sourceFile.set(file("src/main/grammar/My.flex"))
        targetOutputDir.set(file("src/main/gen/com/example/lexer"))
    }
}
```

Wire these tasks into the build so they run before compilation:

```kotlin
tasks {
    compileJava {
        dependsOn(generateParser, generateLexer)
    }
}

sourceSets {
    main {
        java.srcDirs("src/main/gen")
    }
}
```

The generated sources go into `src/main/gen`, which is added as a source directory. This keeps generated code separate from hand-written code and makes it straightforward to add `gen/` to `.gitignore` if you prefer not to commit generated files.

## CI/CD Integration

Gradle-based generation produces reproducible output without an IDE. This makes it well-suited for continuous integration. A basic CI configuration runs the generation tasks as part of the standard build:

```bash
./gradlew build
```

The `generateParser` and `generateLexer` tasks participate in Gradle's up-to-date checking. If the grammar file has not changed, the tasks are skipped on subsequent runs, speeding up incremental builds.

For command-line generation without Gradle, Grammar-Kit also provides a standalone JAR:

```bash
java -jar grammar-kit.jar <output-dir> <grammars-and-dirs>
```

The standalone JAR uses `LightPsi` to create a minimal parsing environment. It has the same limitations as the Gradle plugin (no method mixins, potentially incorrect generics) but works in any environment with a JDK.

For projects that need method mixins or accurate generic signatures, consider a hybrid approach: generate from the IDE during development and commit the generated files to version control. CI then compiles the committed sources without running the generator. See [Gradle vs IDE Generation](gradle-vs-ide.md) for guidance on choosing an approach.
