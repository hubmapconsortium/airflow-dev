#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ls
inputs:
  input_directory:
    type: Directory
    inputBinding:
        position: 1
stdout:
  ls.txt
outputs:
  output_file:
    type: stdout
