# MachOListCompiledMethodSizes
Loads the given Mach-O binary, walks through all object files (OSO symbols) and generates a report with all method names and their sizes.

## How to use

1. Build your app/tool in Xcode or any other environment. Make sure to produce unstripped binary.
2. Feed your unstripped binary to this script, for example:

```
generate_method_size_report.py ~/Library/Developer/Xcode/(....)/Tool.app/Tool /path/to/output.json
```

The tool will generate a JSON file at the given output. You can then process it, convert it into CSV and use Excel/Numbers to build a table, etc. To get the most interesting stats, there are arguments:

`--at-least X` - captures methods which size exceeds the given number of bytes
`--at-most X` - captures methods which size not exceeds the given number of bytes
