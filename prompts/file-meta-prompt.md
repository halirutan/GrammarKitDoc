Your task is to use a subagent to inspect each file in `info/file-list.md` that lists all files in the Grammar-Kit subdirectory.
You will create an output file `ai-out/file-meta.md` where each line contains a file name and a highly compressed summary
that explains the file's purpose and especially if its content can be used to extract information for user documentation.
It's possible that some files can be used for extracting specific technical details, examples or concepts of GrammarKit.
If a file is not relevant for understanding how GrammarKit works from the user's perspective, do not include it in the output!

To give more context, later we will use gathered information to generate an improved version of the user documentation that
goes far beyond what's available in the original documentation.