## Your Task

Your task is to use a subagent to inspect each file in `info/file-list.md`.
This is a list of all files in the `Grammar-Kit` subdirectory.
Your goal is to create highly compressed summaries that go into the output file `info/file-meta.md`.
The summaries explain the file's purpose and especially if its content can be used to extract information for end-user facing documentation of Grammar-Kit.

For each file in `file-list.md` you will do the following steps:

## Step 1:

Check if the file is already included in the output file `file-meta.md`.
If YES, skip it and continue to the next file.

## Step 2:

Create a highly concise summary of the file's purpose and content that contains information about what user-facing documentation topics can be extracted from the file.
For instance some files can be used for extracting user-facing documentation information from implementations. Or files contain examples or concepts of Grammar-Kit.
If a file is not relevant for understanding how Grammar-Kit works from the user's perspective OR if it is a file you cannot inspect (like images or PDFs), use the summary

```
NO RELEVANT INFORMATION AVAILABLE
```

## Step 3:

Include the summary in the output file `file-meta.md` by choosing the correct section and using the required format:

```
filename.ext | summary
```
