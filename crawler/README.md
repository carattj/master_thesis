# crawler.py
F-Droid does not directly provide the source code for the applications it hosts. Instead, users must navigate to the webpage of a specific application on F-Droid and click on the 'source code' link to access it. While F-Droid does offer a per-app API to access its active packages, I discovered a more convenient method to obtain the source code for each F-Droid Android application. I utilized [F-Droid Insights](https://dbeley.github.io/fdroid-insights/), an actively maintained GitHub project designed to facilitate the exploration of F-Droid apps using data from external sources. This platform displays various information for each active Android project, including the public repository for each open-source project. These details can be conveniently downloaded as a processable CSV file, which served as the primary source for creating the dataset.

## Requirements
- [Android SDK command line tools](https://developer.android.com/studio)
- [Uber APK Signer](https://github.com/patrickfav/uber-apk-signer)

## APK processing
Utilizing the CSV file as input, the script initiates the generation of the non-obfuscated dataset. The script is structured into six main sections, described below for clarity and organization.

### 1. Data cleaning
The CSV file comprises 4,329 entries, each corresponding to a specific Android project active on F-Droid. The number of application is in line with the official number of applications officially declared by F-Droid . However, prior to usage, the CSV file requires cleaning. Some entries lack repository information, while others contain duplicate repositories. Although investigating this issue falls beyond the scope of the research, it likely stems from the storage method of active Android projects on F-Droid. Notably, there are 20 entries with corrupted data and 151 duplicated rows, but these two datasets overlap. Consequently, after removing the flawed data during preprocessing, the CSV consists of 4,177 distinct Android project repositories.

### 2. Repository structure check
Upon manual inspection of numerous repositories, it became evident that they exhibit varying structures. While some repositories consist solely of an Android project, others include code for multiple platforms or exhibit different directory arrangements. Consequently, when faced with repositories that do not strictly adhere to a pure Android project structure, the repository's organization can vary greatly, dictated by the developer's discretion and not predetermined for us.
Consequently, our decision was to narrow our focus to pure Android projects, as they consistently adhere to a standardized structure. Therefore, when processing a project, our initial step involves sending a GET request to its repository URL. Subsequently, in the HTML response, we search for an <a> tag with 'gradlew' as the title. If a match is found, indicating a pure Android project repository, we proceed processing it. Conversely, if no match is found, we disregard the repository and move on to the next one.

### 3. Repository cloning
Hopefully, the Android project can then be compiled into an APK. Therefore, we proceed by cloning the repository to play with the code.

### 4. Detect and disable obfuscation
In Android development, the build.gradle and build.gradle.kts files are configuration files used to define various aspects of the build process for Android applications. Written in Groovy and Kotlin respectively, they specify build settings, dependencies, and other build-related configurations using a domain-specific language. Nowadays, Kotlin is preferred over Groovy due to its modern features and concise syntax. 
Additionally, these files play a crucial role in setting up obfuscation. By specifying rules and configurations in these files, developers can customize obfuscation, integrating tools tools such as ProGuard or R8 into the build process.

Hence, our objective is to verify the existence of either the build.gradle or the build.gradle.kts files within the cloned project repository. If neither file is found, we proceed with the next step, as obfuscation has not been implemented. Conversely, upon detecting one of these files, we examine it to identify the specific configuration parameter responsible for setting up obfuscation. It's worth noting that the parameter differs depending on whether the file is written in Kotlin or Groovy. We deactivate the parameter and overwrite the file. 

### 5. Compilation
The non-obfuscated Android project is now ready for compilation. Therefore, we run the command to compile it into an APK. However, it's important to note that this build process can be somewhat unstable, occasionally leading to compilation failures for certain applications. In such instances, we simply move to the next project, disregarding the current one. Conversely, upon a successful build, we obtain an APK that is nearly ready for use.

### 6. Save the APK
The just compiled APK is now extracted from the project repository and saved on disk, so that the remaining project repository can be deleted to save space.

## APK signing 
At this stage, executing the APK on a device will yield a ‘Missing signature failure’ as the APK compilation process did not include signing, a prerequisite for Android application execution. While various tools exist for signing APKs, one notably straightforward option is [Uber APK Signer](https://github.com/patrickfav/uber-apk-signer), available on GitHub. This tool streamlines the process by facilitating APK signing, zip alignment, and verification for multiple APKs simultaneously.
The APK can be easily run on an Android device without problems. For testing purposes, I recommend using the online emulator Appetize.