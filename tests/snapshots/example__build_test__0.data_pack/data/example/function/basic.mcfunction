<class 'mecha.ast.AstRoot'>
  location: SourceLocation(pos=0, lineno=1, colno=1)
  end_location: SourceLocation(pos=907, lineno=30, colno=2)
  commands:
    <class 'mecha.ast.AstCommand'>
      location: SourceLocation(pos=0, lineno=1, colno=1)
      end_location: SourceLocation(pos=0, lineno=1, colno=1)
      identifier: 'compute:bolt'
      arguments:
        <class 'bolt_compute.node.AstComputeRoot'>
          location: SourceLocation(pos=-1, lineno=0, colno=0)
          end_location: SourceLocation(pos=-1, lineno=0, colno=0)
          children:
            <class 'bolt_compute.float.AstFloatFromInt'>
              location: SourceLocation(pos=-1, lineno=0, colno=0)
              end_location: SourceLocation(pos=-1, lineno=0, colno=0)
              depth: MutableDepth(value=0)
              input:
                <class 'bolt_compute.integer.AstIntegerScoreResolveLater'>
                  location: SourceLocation(pos=-1, lineno=0, colno=0)
                  end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                  depth: MutableDepth(value=1)
                  args:
                    <class 'bolt_compute.node.AstNodeContainer'>
                      location: SourceLocation(pos=-1, lineno=0, colno=0)
                      end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                      value: 'context'
                    <class 'bolt_compute.node.AstNodeContainer'>
                      location: SourceLocation(pos=-1, lineno=0, colno=0)
                      end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                      value: 'this'
                    <class 'bolt_compute.node.AstNodeContainer'>
                      location: SourceLocation(pos=-1, lineno=0, colno=0)
                      end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                      value: 'average'
          argument_node: None
          bolt_type: 'default'
          operation_type: 'float'
    <class 'mecha.ast.AstCommand'>
      location: SourceLocation(pos=67, lineno=5, colno=1)
      end_location: SourceLocation(pos=67, lineno=5, colno=1)
      identifier: 'compute:default:float:provider'
      arguments:
        <class 'bolt_compute.float.AstFloatAdd'>
          location: SourceLocation(pos=-1, lineno=0, colno=0)
          end_location: SourceLocation(pos=-1, lineno=0, colno=0)
          depth: MutableDepth(value=0)
          inputs:
            <class 'bolt_compute.float.AstFloatMul'>
              location: SourceLocation(pos=-1, lineno=0, colno=0)
              end_location: SourceLocation(pos=-1, lineno=0, colno=0)
              depth: MutableDepth(value=1)
              inputs:
                <class 'bolt_compute.float.AstFloatConstant'>
                  location: SourceLocation(pos=-1, lineno=0, colno=0)
                  end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                  depth: MutableDepth(value=1)
                  value: 2.0
                <class 'bolt_compute.float.AstFloatSin'>
                  location: SourceLocation(pos=-1, lineno=0, colno=0)
                  end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                  depth: MutableDepth(value=1)
                  input:
                    <class 'bolt_compute.float.AstFloatStorage'>
                      location: SourceLocation(pos=-1, lineno=0, colno=0)
                      end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                      depth: MutableDepth(value=3)
                      storage:
                        <class 'mecha.ast.AstResourceLocation'>
                          location: SourceLocation(pos=109, lineno=6, colno=19)
                          end_location: SourceLocation(pos=123, lineno=6, colno=33)
                          is_tag: False
                          namespace: 'namespace'
                          path: 'test'
                      path:
                        <class 'mecha.ast.AstNbtPath'>
                          location: SourceLocation(pos=124, lineno=6, colno=34)
                          end_location: SourceLocation(pos=127, lineno=6, colno=37)
                          components:
                            <class 'mecha.ast.AstNbtPathKey'>
                              location: SourceLocation(pos=124, lineno=6, colno=34)
                              end_location: SourceLocation(pos=127, lineno=6, colno=37)
                              value: 'div'
                      fallback: None
            <class 'bolt_compute.float.AstFloatMax'>
              location: SourceLocation(pos=-1, lineno=0, colno=0)
              end_location: SourceLocation(pos=-1, lineno=0, colno=0)
              depth: MutableDepth(value=1)
              inputs:
                <class 'bolt_compute.float.AstFloatFromInt'>
                  location: SourceLocation(pos=-1, lineno=0, colno=0)
                  end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                  depth: MutableDepth(value=3)
                  input:
                    <class 'bolt_compute.integer.AstIntegerScore'>
                      location: SourceLocation(pos=-1, lineno=0, colno=0)
                      end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                      depth: MutableDepth(value=4)
                      target_type:
                        <class 'bolt_compute.integer.AstTargetTypeType'>
                          location: SourceLocation(pos=135, lineno=6, colno=45)
                          end_location: SourceLocation(pos=140, lineno=6, colno=50)
                          value: 'context'
                      target_target:
                        <class 'bolt_compute.integer.AstTargetType'>
                          location: SourceLocation(pos=141, lineno=6, colno=51)
                          end_location: SourceLocation(pos=145, lineno=6, colno=55)
                          value: 'this'
                      target_name: None
                      score:
                        <class 'mecha.ast.AstObjective'>
                          location: SourceLocation(pos=146, lineno=6, colno=56)
                          end_location: SourceLocation(pos=160, lineno=6, colno=70)
                          value: 'namespace.data'
                      fallback: None
                <class 'bolt_compute.float.AstFloatFromInt'>
                  location: SourceLocation(pos=-1, lineno=0, colno=0)
                  end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                  depth: MutableDepth(value=3)
                  input:
                    <class 'bolt_compute.integer.AstIntegerScore'>
                      location: SourceLocation(pos=-1, lineno=0, colno=0)
                      end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                      depth: MutableDepth(value=4)
                      target_type:
                        <class 'bolt_compute.integer.AstTargetTypeType'>
                          location: SourceLocation(pos=162, lineno=6, colno=72)
                          end_location: SourceLocation(pos=167, lineno=6, colno=77)
                          value: 'context'
                      target_target:
                        <class 'bolt_compute.integer.AstTargetType'>
                          location: SourceLocation(pos=168, lineno=6, colno=78)
                          end_location: SourceLocation(pos=172, lineno=6, colno=82)
                          value: 'this'
                      target_name: None
                      score:
                        <class 'mecha.ast.AstObjective'>
                          location: SourceLocation(pos=173, lineno=6, colno=83)
                          end_location: SourceLocation(pos=188, lineno=6, colno=98)
                          value: 'namespace.money'
                      fallback: None
    <class 'mecha.ast.AstCommand'>
      location: SourceLocation(pos=240, lineno=11, colno=1)
      end_location: SourceLocation(pos=329, lineno=11, colno=90)
      identifier: 'execute:subcommand'
      arguments:
        <class 'mecha.ast.AstCommand'>
          location: SourceLocation(pos=248, lineno=11, colno=9)
          end_location: SourceLocation(pos=329, lineno=11, colno=90)
          identifier: 'execute:on:origin:subcommand'
          arguments:
            <class 'mecha.ast.AstCommand'>
              location: SourceLocation(pos=258, lineno=11, colno=19)
              end_location: SourceLocation(pos=329, lineno=11, colno=90)
              identifier: 'execute:run:subcommand'
              arguments:
                <class 'mecha.ast.AstCommand'>
                  location: SourceLocation(pos=262, lineno=11, colno=23)
                  end_location: SourceLocation(pos=329, lineno=11, colno=90)
                  identifier: 'data:modify:storage:target:targetPath:set:from:entity:source:sourcePath'
                  arguments:
                    <class 'mecha.ast.AstResourceLocation'>
                      location: SourceLocation(pos=282, lineno=11, colno=43)
                      end_location: SourceLocation(pos=301, lineno=11, colno=62)
                      is_tag: False
                      namespace: 'grappling_hook'
                      path: 'temp'
                    <class 'mecha.ast.AstNbtPath'>
                      location: SourceLocation(pos=302, lineno=11, colno=63)
                      end_location: SourceLocation(pos=306, lineno=11, colno=67)
                      components:
                        <class 'mecha.ast.AstNbtPathKey'>
                          location: SourceLocation(pos=302, lineno=11, colno=63)
                          end_location: SourceLocation(pos=306, lineno=11, colno=67)
                          value: 'pos1'
                    <class 'mecha.ast.AstSelector'>
                      location: SourceLocation(pos=323, lineno=11, colno=84)
                      end_location: SourceLocation(pos=325, lineno=11, colno=86)
                      variable: 's'
                      arguments:
                        <empty>
                    <class 'mecha.ast.AstNbtPath'>
                      location: SourceLocation(pos=326, lineno=11, colno=87)
                      end_location: SourceLocation(pos=329, lineno=11, colno=90)
                      components:
                        <class 'mecha.ast.AstNbtPathKey'>
                          location: SourceLocation(pos=326, lineno=11, colno=87)
                          end_location: SourceLocation(pos=329, lineno=11, colno=90)
                          value: 'Pos'
    <class 'mecha.ast.AstCommand'>
      location: SourceLocation(pos=330, lineno=12, colno=1)
      end_location: SourceLocation(pos=397, lineno=12, colno=68)
      identifier: 'data:modify:storage:target:targetPath:set:from:entity:source:sourcePath'
      arguments:
        <class 'mecha.ast.AstResourceLocation'>
          location: SourceLocation(pos=350, lineno=12, colno=21)
          end_location: SourceLocation(pos=369, lineno=12, colno=40)
          is_tag: False
          namespace: 'grappling_hook'
          path: 'temp'
        <class 'mecha.ast.AstNbtPath'>
          location: SourceLocation(pos=370, lineno=12, colno=41)
          end_location: SourceLocation(pos=374, lineno=12, colno=45)
          components:
            <class 'mecha.ast.AstNbtPathKey'>
              location: SourceLocation(pos=370, lineno=12, colno=41)
              end_location: SourceLocation(pos=374, lineno=12, colno=45)
              value: 'pos2'
        <class 'mecha.ast.AstSelector'>
          location: SourceLocation(pos=391, lineno=12, colno=62)
          end_location: SourceLocation(pos=393, lineno=12, colno=64)
          variable: 's'
          arguments:
            <empty>
        <class 'mecha.ast.AstNbtPath'>
          location: SourceLocation(pos=394, lineno=12, colno=65)
          end_location: SourceLocation(pos=397, lineno=12, colno=68)
          components:
            <class 'mecha.ast.AstNbtPathKey'>
              location: SourceLocation(pos=394, lineno=12, colno=65)
              end_location: SourceLocation(pos=397, lineno=12, colno=68)
              value: 'Pos'
    <class 'mecha.ast.AstCommand'>
      location: SourceLocation(pos=399, lineno=14, colno=1)
      end_location: SourceLocation(pos=399, lineno=14, colno=1)
      identifier: 'data:modify:storage:target:targetPath:set:compute:default:float:provider'
      arguments:
        <class 'mecha.ast.AstResourceLocation'>
          location: SourceLocation(pos=419, lineno=14, colno=21)
          end_location: SourceLocation(pos=433, lineno=14, colno=35)
          is_tag: False
          namespace: 'namespace'
          path: 'temp'
        <class 'mecha.ast.AstNbtPath'>
          location: SourceLocation(pos=434, lineno=14, colno=36)
          end_location: SourceLocation(pos=442, lineno=14, colno=44)
          components:
            <class 'mecha.ast.AstNbtPathKey'>
              location: SourceLocation(pos=434, lineno=14, colno=36)
              end_location: SourceLocation(pos=442, lineno=14, colno=44)
              value: 'distance'
        <class 'bolt_compute.float.AstFloatSqrt'>
          location: SourceLocation(pos=-1, lineno=0, colno=0)
          end_location: SourceLocation(pos=-1, lineno=0, colno=0)
          depth: MutableDepth(value=0)
          input:
            <class 'bolt_compute.float.AstFloatAdd'>
              location: SourceLocation(pos=-1, lineno=0, colno=0)
              end_location: SourceLocation(pos=-1, lineno=0, colno=0)
              depth: MutableDepth(value=1)
              inputs:
                <class 'bolt_compute.float.AstFloatAdd'>
                  location: SourceLocation(pos=-1, lineno=0, colno=0)
                  end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                  depth: MutableDepth(value=2)
                  inputs:
                    <class 'bolt_compute.float.AstFloatPow'>
                      location: SourceLocation(pos=-1, lineno=0, colno=0)
                      end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                      depth: MutableDepth(value=2)
                      base:
                        <class 'bolt_compute.float.AstFloatSub'>
                          location: SourceLocation(pos=-1, lineno=0, colno=0)
                          end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                          depth: MutableDepth(value=2)
                          left:
                            <class 'bolt_compute.float.AstFloatStorage'>
                              location: SourceLocation(pos=-1, lineno=0, colno=0)
                              end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                              depth: MutableDepth(value=3)
                              storage:
                                <class 'mecha.ast.AstResourceLocation'>
                                  location: SourceLocation(pos=498, lineno=16, colno=18)
                                  end_location: SourceLocation(pos=512, lineno=16, colno=32)
                                  is_tag: False
                                  namespace: 'namespace'
                                  path: 'temp'
                              path:
                                <class 'mecha.ast.AstNbtPath'>
                                  location: SourceLocation(pos=513, lineno=16, colno=33)
                                  end_location: SourceLocation(pos=520, lineno=16, colno=40)
                                  components:
                                    <class 'mecha.ast.AstNbtPathKey'>
                                      location: SourceLocation(pos=513, lineno=16, colno=33)
                                      end_location: SourceLocation(pos=517, lineno=16, colno=37)
                                      value: 'pos1'
                                    <class 'mecha.ast.AstNbtPathSubscript'>
                                      location: SourceLocation(pos=517, lineno=16, colno=37)
                                      end_location: SourceLocation(pos=520, lineno=16, colno=40)
                                      index:
                                        <class 'mecha.ast.AstNumber'>
                                          location: SourceLocation(pos=518, lineno=16, colno=38)
                                          end_location: SourceLocation(pos=519, lineno=16, colno=39)
                                          value: 0
                              fallback: None
                          right:
                            <class 'bolt_compute.float.AstFloatStorage'>
                              location: SourceLocation(pos=-1, lineno=0, colno=0)
                              end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                              depth: MutableDepth(value=3)
                              storage:
                                <class 'mecha.ast.AstResourceLocation'>
                                  location: SourceLocation(pos=531, lineno=16, colno=51)
                                  end_location: SourceLocation(pos=545, lineno=16, colno=65)
                                  is_tag: False
                                  namespace: 'namespace'
                                  path: 'temp'
                              path:
                                <class 'mecha.ast.AstNbtPath'>
                                  location: SourceLocation(pos=546, lineno=16, colno=66)
                                  end_location: SourceLocation(pos=553, lineno=16, colno=73)
                                  components:
                                    <class 'mecha.ast.AstNbtPathKey'>
                                      location: SourceLocation(pos=546, lineno=16, colno=66)
                                      end_location: SourceLocation(pos=550, lineno=16, colno=70)
                                      value: 'pos2'
                                    <class 'mecha.ast.AstNbtPathSubscript'>
                                      location: SourceLocation(pos=550, lineno=16, colno=70)
                                      end_location: SourceLocation(pos=553, lineno=16, colno=73)
                                      index:
                                        <class 'mecha.ast.AstNumber'>
                                          location: SourceLocation(pos=551, lineno=16, colno=71)
                                          end_location: SourceLocation(pos=552, lineno=16, colno=72)
                                          value: 0
                              fallback: None
                      exponent:
                        <class 'bolt_compute.float.AstFloatConstant'>
                          location: SourceLocation(pos=-1, lineno=0, colno=0)
                          end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                          depth: MutableDepth(value=2)
                          value: 2.0
                    <class 'bolt_compute.float.AstFloatPow'>
                      location: SourceLocation(pos=-1, lineno=0, colno=0)
                      end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                      depth: MutableDepth(value=2)
                      base:
                        <class 'bolt_compute.float.AstFloatSub'>
                          location: SourceLocation(pos=-1, lineno=0, colno=0)
                          end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                          depth: MutableDepth(value=3)
                          left:
                            <class 'bolt_compute.float.AstFloatStorage'>
                              location: SourceLocation(pos=-1, lineno=0, colno=0)
                              end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                              depth: MutableDepth(value=4)
                              storage:
                                <class 'mecha.ast.AstResourceLocation'>
                                  location: SourceLocation(pos=577, lineno=17, colno=18)
                                  end_location: SourceLocation(pos=591, lineno=17, colno=32)
                                  is_tag: False
                                  namespace: 'namespace'
                                  path: 'temp'
                              path:
                                <class 'mecha.ast.AstNbtPath'>
                                  location: SourceLocation(pos=592, lineno=17, colno=33)
                                  end_location: SourceLocation(pos=599, lineno=17, colno=40)
                                  components:
                                    <class 'mecha.ast.AstNbtPathKey'>
                                      location: SourceLocation(pos=592, lineno=17, colno=33)
                                      end_location: SourceLocation(pos=596, lineno=17, colno=37)
                                      value: 'pos1'
                                    <class 'mecha.ast.AstNbtPathSubscript'>
                                      location: SourceLocation(pos=596, lineno=17, colno=37)
                                      end_location: SourceLocation(pos=599, lineno=17, colno=40)
                                      index:
                                        <class 'mecha.ast.AstNumber'>
                                          location: SourceLocation(pos=597, lineno=17, colno=38)
                                          end_location: SourceLocation(pos=598, lineno=17, colno=39)
                                          value: 1
                              fallback: None
                          right:
                            <class 'bolt_compute.float.AstFloatStorage'>
                              location: SourceLocation(pos=-1, lineno=0, colno=0)
                              end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                              depth: MutableDepth(value=4)
                              storage:
                                <class 'mecha.ast.AstResourceLocation'>
                                  location: SourceLocation(pos=610, lineno=17, colno=51)
                                  end_location: SourceLocation(pos=624, lineno=17, colno=65)
                                  is_tag: False
                                  namespace: 'namespace'
                                  path: 'temp'
                              path:
                                <class 'mecha.ast.AstNbtPath'>
                                  location: SourceLocation(pos=625, lineno=17, colno=66)
                                  end_location: SourceLocation(pos=632, lineno=17, colno=73)
                                  components:
                                    <class 'mecha.ast.AstNbtPathKey'>
                                      location: SourceLocation(pos=625, lineno=17, colno=66)
                                      end_location: SourceLocation(pos=629, lineno=17, colno=70)
                                      value: 'pos2'
                                    <class 'mecha.ast.AstNbtPathSubscript'>
                                      location: SourceLocation(pos=629, lineno=17, colno=70)
                                      end_location: SourceLocation(pos=632, lineno=17, colno=73)
                                      index:
                                        <class 'mecha.ast.AstNumber'>
                                          location: SourceLocation(pos=630, lineno=17, colno=71)
                                          end_location: SourceLocation(pos=631, lineno=17, colno=72)
                                          value: 1
                              fallback: None
                      exponent:
                        <class 'bolt_compute.float.AstFloatConstant'>
                          location: SourceLocation(pos=-1, lineno=0, colno=0)
                          end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                          depth: MutableDepth(value=3)
                          value: 2.0
                <class 'bolt_compute.float.AstFloatPow'>
                  location: SourceLocation(pos=-1, lineno=0, colno=0)
                  end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                  depth: MutableDepth(value=2)
                  base:
                    <class 'bolt_compute.float.AstFloatSub'>
                      location: SourceLocation(pos=-1, lineno=0, colno=0)
                      end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                      depth: MutableDepth(value=3)
                      left:
                        <class 'bolt_compute.float.AstFloatStorage'>
                          location: SourceLocation(pos=-1, lineno=0, colno=0)
                          end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                          depth: MutableDepth(value=4)
                          storage:
                            <class 'mecha.ast.AstResourceLocation'>
                              location: SourceLocation(pos=656, lineno=18, colno=18)
                              end_location: SourceLocation(pos=670, lineno=18, colno=32)
                              is_tag: False
                              namespace: 'namespace'
                              path: 'temp'
                          path:
                            <class 'mecha.ast.AstNbtPath'>
                              location: SourceLocation(pos=671, lineno=18, colno=33)
                              end_location: SourceLocation(pos=678, lineno=18, colno=40)
                              components:
                                <class 'mecha.ast.AstNbtPathKey'>
                                  location: SourceLocation(pos=671, lineno=18, colno=33)
                                  end_location: SourceLocation(pos=675, lineno=18, colno=37)
                                  value: 'pos1'
                                <class 'mecha.ast.AstNbtPathSubscript'>
                                  location: SourceLocation(pos=675, lineno=18, colno=37)
                                  end_location: SourceLocation(pos=678, lineno=18, colno=40)
                                  index:
                                    <class 'mecha.ast.AstNumber'>
                                      location: SourceLocation(pos=676, lineno=18, colno=38)
                                      end_location: SourceLocation(pos=677, lineno=18, colno=39)
                                      value: 2
                          fallback: None
                      right:
                        <class 'bolt_compute.float.AstFloatStorage'>
                          location: SourceLocation(pos=-1, lineno=0, colno=0)
                          end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                          depth: MutableDepth(value=4)
                          storage:
                            <class 'mecha.ast.AstResourceLocation'>
                              location: SourceLocation(pos=689, lineno=18, colno=51)
                              end_location: SourceLocation(pos=703, lineno=18, colno=65)
                              is_tag: False
                              namespace: 'namespace'
                              path: 'temp'
                          path:
                            <class 'mecha.ast.AstNbtPath'>
                              location: SourceLocation(pos=704, lineno=18, colno=66)
                              end_location: SourceLocation(pos=711, lineno=18, colno=73)
                              components:
                                <class 'mecha.ast.AstNbtPathKey'>
                                  location: SourceLocation(pos=704, lineno=18, colno=66)
                                  end_location: SourceLocation(pos=708, lineno=18, colno=70)
                                  value: 'pos2'
                                <class 'mecha.ast.AstNbtPathSubscript'>
                                  location: SourceLocation(pos=708, lineno=18, colno=70)
                                  end_location: SourceLocation(pos=711, lineno=18, colno=73)
                                  index:
                                    <class 'mecha.ast.AstNumber'>
                                      location: SourceLocation(pos=709, lineno=18, colno=71)
                                      end_location: SourceLocation(pos=710, lineno=18, colno=72)
                                      value: 2
                          fallback: None
                  exponent:
                    <class 'bolt_compute.float.AstFloatConstant'>
                      location: SourceLocation(pos=-1, lineno=0, colno=0)
                      end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                      depth: MutableDepth(value=3)
                      value: 2.0
    <class 'mecha.ast.AstCommand'>
      location: SourceLocation(pos=739, lineno=23, colno=1)
      end_location: SourceLocation(pos=739, lineno=23, colno=1)
      identifier: 'compute:bolt'
      arguments:
        <class 'bolt_compute.node.AstComputeRoot'>
          location: SourceLocation(pos=-1, lineno=0, colno=0)
          end_location: SourceLocation(pos=-1, lineno=0, colno=0)
          children:
            <class 'bolt_compute.float.AstFloatConditional'>
              location: SourceLocation(pos=-1, lineno=0, colno=0)
              end_location: SourceLocation(pos=-1, lineno=0, colno=0)
              depth: MutableDepth(value=0)
              condition:
                <class 'mecha.ast.AstNbtCompound'>
                  location: SourceLocation(pos=774, lineno=24, colno=15)
                  end_location: SourceLocation(pos=776, lineno=24, colno=17)
                  entries:
                    <empty>
              on_true:
                <class 'bolt_compute.float.AstFloatConstant'>
                  location: SourceLocation(pos=-1, lineno=0, colno=0)
                  end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                  depth: MutableDepth(value=1)
                  value: 220210.0
              on_false:
                <class 'bolt_compute.float.AstFloatConstant'>
                  location: SourceLocation(pos=-1, lineno=0, colno=0)
                  end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                  depth: MutableDepth(value=1)
                  value: 23.0
          argument_node: None
          bolt_type: 'default'
          operation_type: 'float'
