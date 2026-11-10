# What we found in F:\SketchUp\SketchUp\SketchUp.exe

SketchUp.exe is a program for Windows, built for x86_64 (64-bit). It looks like it was made with Qt. Its internal names were removed (stripped), so most functions will have generated names.

Evidence ev_425c8f5bcb1249bffc373068f8206dd3f36bad547ee6447fff9ccaf79c9d7775.

```json
{
  "architecture": "x86_64",
  "bits": 64,
  "dotnet_arch": null,
  "entry_point": "0x140ec4340",
  "format": "pe",
  "format_name": "PE (Windows)",
  "kind": "executable",
  "libraries": [
    "ADVAPI32.dll",
    "BugSplat64.dll",
    "CRYPT32.dll",
    "D3DCOMPILER_47.dll",
    "GDI32.dll",
    "IPHLPAPI.DLL",
    "KERNEL32.dll",
    "MSVCP140.dll",
    "MSVCP140_ATOMIC_WAIT.dll",
    "MSVCP140_CODECVT_IDS.dll",
    "OLEAUT32.dll",
    "OPENGL32.dll",
    "Qt6Core.dll",
    "Qt6Gui.dll",
    "Qt6Multimedia.dll",
    "Qt6Pdf.dll",
    "Qt6PrintSupport.dll",
    "Qt6Qml.dll",
    "Qt6Quick.dll",
    "Qt6QuickControls2.dll",
    "Qt6Svg.dll",
    "Qt6SvgWidgets.dll",
    "Qt6Widgets.dll",
    "RPCRT4.dll",
    "SETUPAPI.dll",
    "SHELL32.dll",
    "SHLWAPI.dll",
    "SketchUpCommonPreferences.dll",
    "USER32.dll",
    "USP10.dll",
    "VCRUNTIME140.dll",
    "VCRUNTIME140_1.dll"
  ],
  "next_steps": [
    {
      "tool": "core_overview_show",
      "why": "a one-page summary: sections, imports, counts"
    },
    {
      "tool": "native_functions_list",
      "why": "every function we found"
    },
    {
      "tool": "native_strings_find",
      "why": "find text the program shows or uses"
    },
    {
      "tool": "native_function_study",
      "why": "a full dossier on one function (start with main or the entry point)"
    },
    {
      "tool": "core_feature_find",
      "why": "follow a word you see in the app to the code behind it"
    },
    {
      "tool": "native_pe_resources_list",
      "why": "icons, version information and the manifest"
    }
  ],
  "operating_system": "Windows",
  "plain_english": "SketchUp.exe is a program for Windows, built for x86_64 (64-bit). It looks like it was made with Qt. Its internal names were removed (stripped), so most functions will have generated names.",
  "recommended_toolsets": [
    "core",
    "native",
    "formats"
  ],
  "stripped": true,
  "symbol_table_stripped": true,
  "toolchain_hints": [
    {
      "category": "framework",
      "evidence": "links Qt",
      "id": "qt",
      "label": "Qt",
      "strength": "strong"
    },
    {
      "category": "compiler",
      "evidence": "Rich header",
      "id": "msvc",
      "label": "Microsoft Visual C++ toolchain",
      "strength": "strong"
    }
  ]
}
```

## Ghidra

Deep mode: Ghidra has analysed F:\SketchUp\SketchUp\SketchUp.exe (19 min), so decompiling it is quick.
