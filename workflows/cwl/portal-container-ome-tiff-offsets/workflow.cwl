#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
# TODO: Make main.py executable?
baseCommand: ['python', '/main.py', '--output_dir', '.', '--input_dir']
hints:
  DockerRequirement:
    dockerPull: hubmap/portal-container-ome-tiff-offsets:0.0.1
inputs:
  input_directory:
    type: Directory
    inputBinding:
        position: 6
outputs:
  tif_initial:
    type: File
    outputBinding:
      glob: 'compressed/*.ome.tif'
  tif:
    type: File
    outputBinding:
      glob: '*.ome.tif'
  xml:
    type: File
    outputBinding:
      glob: '*.ome.xml'
