#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ['python', '/main.py']
hints:
  DockerRequirement:
    dockerPull: hubmap/portal-container-h5ad-to-arrow:0.0.1
inputs:
  input_directory:
    type: Directory
    inputBinding:
        position: 1
outputs:
  csv:
    type: File
    outputBinding:
      glob: '*.csv'
#  arrow:
#    type: File
#    outputBinding:
#      glob: '*.arrow'
#  json:
#    type: File
#    outputBinding:
#      glob: '*.json'
