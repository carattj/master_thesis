# Obfuscation
There are many ways to obfuscate an APK. Here, we are insterested in a specific type of obfuscation: identififier renaming.
The main goal of this part of the work is to obfuscate the obtained dataset of non-obfuscated APKs.

So, I identified two promising obfuscation techniques: Obfuscapk and Proguard.

## Obfuscapk
[Obfuscapk](https://github.com/Mobile-IoT-Security-Lab/Obfuscapk) is an open-source python tool for obfuscating Android apps without needing their source code. The obfuscated app retains the same functionality as the original one, but the differences under the hood sometimes make the new application very different from the original (e.g. signature-based antivirus software).
Obfuscapk offers 3 different ways to rename identifiers: FieldRename, MethodRename, and ClassRename. Clearly, these modalities can further be combined together to create even more shades of identifier renaming obfuscation.
[obfuscator.py](./obfuscapk/obfuscator.py) allows to run Obfuscapk on multiple APKs at the same time. Furthermore, we can specify the obfuscation modalities we want to use. The script will then organize the output into well-defined directories.

## R8
When you build your project with the latest Android Gradle plugins, ProGuard is no longer used to perform compile-time code optimization. Instead, the [R8](https://developer.android.com/build/shrink-code) compiler will handle the 4 compile-time tasks: code shrinking, resource shrinking, obfuscation, and optimization.
In our case, we will clearly only consider obfuscation. An interesting consideration is that R8 can be further customized by adding specific rules to the configuration file before compiling the APK.