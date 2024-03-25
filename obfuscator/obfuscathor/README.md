# ObfuscaThor
### Strategies
Chose and clone the identifier renaming obfuscation you want to perform among the following ones:

**Shortest**
Identifiers get replaced by the shortest possible identifiers.

**Confusion**
Identifiers get replaced by existing identifiers extracted from real projects.

**Mirror**
Identifiers get replaced by identifiers extracted from a target APK.

**Textual**
Identifiers get replaced by strings taken from a text.

### Usage
In your home directory, clone the Obfuscapk project and replace `field_rename.py`, `method_rename.py` and `class_rename.py` with the ones in `code_renaming` directory. With docker, build Obfuscapk as described in its documentation.

If you chose Shortest or Textual, just copy the dictionary in the home directory and rename it as 'dictionary.txt'. If you chose Confusion or Textual, copy the dict_confusion directory in you home directory.

You can now use Obfuscapk as described in its documentation. Identifier renaming obfuscation will be performed following the specified strategy.