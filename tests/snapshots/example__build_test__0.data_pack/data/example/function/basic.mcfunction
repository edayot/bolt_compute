<class 'mecha.ast.AstRoot'>
  location: SourceLocation(pos=0, lineno=1, colno=1)
  end_location: SourceLocation(pos=897, lineno=30, colno=2)
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
      end_location: SourceLocation(pos=324, lineno=11, colno=85)
      identifier: 'execute:subcommand'
      arguments:
        <class 'mecha.ast.AstCommand'>
          location: SourceLocation(pos=248, lineno=11, colno=9)
          end_location: SourceLocation(pos=324, lineno=11, colno=85)
          identifier: 'execute:on:origin:subcommand'
          arguments:
            <class 'mecha.ast.AstCommand'>
              location: SourceLocation(pos=258, lineno=11, colno=19)
              end_location: SourceLocation(pos=324, lineno=11, colno=85)
              identifier: 'execute:run:subcommand'
              arguments:
                <class 'mecha.ast.AstCommand'>
                  location: SourceLocation(pos=262, lineno=11, colno=23)
                  end_location: SourceLocation(pos=324, lineno=11, colno=85)
                  identifier: 'data:modify:storage:target:targetPath:set:from:entity:source:sourcePath'
                  arguments:
                    <class 'mecha.ast.AstResourceLocation'>
                      location: SourceLocation(pos=282, lineno=11, colno=43)
                      end_location: SourceLocation(pos=296, lineno=11, colno=57)
                      is_tag: False
                      namespace: 'namespace'
                      path: 'temp'
                    <class 'mecha.ast.AstNbtPath'>
                      location: SourceLocation(pos=297, lineno=11, colno=58)
                      end_location: SourceLocation(pos=301, lineno=11, colno=62)
                      components:
                        <class 'mecha.ast.AstNbtPathKey'>
                          location: SourceLocation(pos=297, lineno=11, colno=58)
                          end_location: SourceLocation(pos=301, lineno=11, colno=62)
                          value: 'pos1'
                    <class 'mecha.ast.AstSelector'>
                      location: SourceLocation(pos=318, lineno=11, colno=79)
                      end_location: SourceLocation(pos=320, lineno=11, colno=81)
                      variable: 's'
                      arguments:
                        <empty>
                    <class 'mecha.ast.AstNbtPath'>
                      location: SourceLocation(pos=321, lineno=11, colno=82)
                      end_location: SourceLocation(pos=324, lineno=11, colno=85)
                      components:
                        <class 'mecha.ast.AstNbtPathKey'>
                          location: SourceLocation(pos=321, lineno=11, colno=82)
                          end_location: SourceLocation(pos=324, lineno=11, colno=85)
                          value: 'Pos'
    <class 'mecha.ast.AstCommand'>
      location: SourceLocation(pos=325, lineno=12, colno=1)
      end_location: SourceLocation(pos=387, lineno=12, colno=63)
      identifier: 'data:modify:storage:target:targetPath:set:from:entity:source:sourcePath'
      arguments:
        <class 'mecha.ast.AstResourceLocation'>
          location: SourceLocation(pos=345, lineno=12, colno=21)
          end_location: SourceLocation(pos=359, lineno=12, colno=35)
          is_tag: False
          namespace: 'namespace'
          path: 'temp'
        <class 'mecha.ast.AstNbtPath'>
          location: SourceLocation(pos=360, lineno=12, colno=36)
          end_location: SourceLocation(pos=364, lineno=12, colno=40)
          components:
            <class 'mecha.ast.AstNbtPathKey'>
              location: SourceLocation(pos=360, lineno=12, colno=36)
              end_location: SourceLocation(pos=364, lineno=12, colno=40)
              value: 'pos2'
        <class 'mecha.ast.AstSelector'>
          location: SourceLocation(pos=381, lineno=12, colno=57)
          end_location: SourceLocation(pos=383, lineno=12, colno=59)
          variable: 's'
          arguments:
            <empty>
        <class 'mecha.ast.AstNbtPath'>
          location: SourceLocation(pos=384, lineno=12, colno=60)
          end_location: SourceLocation(pos=387, lineno=12, colno=63)
          components:
            <class 'mecha.ast.AstNbtPathKey'>
              location: SourceLocation(pos=384, lineno=12, colno=60)
              end_location: SourceLocation(pos=387, lineno=12, colno=63)
              value: 'Pos'
    <class 'mecha.ast.AstCommand'>
      location: SourceLocation(pos=389, lineno=14, colno=1)
      end_location: SourceLocation(pos=389, lineno=14, colno=1)
      identifier: 'data:modify:storage:target:targetPath:set:compute:default:float:provider'
      arguments:
        <class 'mecha.ast.AstResourceLocation'>
          location: SourceLocation(pos=409, lineno=14, colno=21)
          end_location: SourceLocation(pos=423, lineno=14, colno=35)
          is_tag: False
          namespace: 'namespace'
          path: 'temp'
        <class 'mecha.ast.AstNbtPath'>
          location: SourceLocation(pos=424, lineno=14, colno=36)
          end_location: SourceLocation(pos=432, lineno=14, colno=44)
          components:
            <class 'mecha.ast.AstNbtPathKey'>
              location: SourceLocation(pos=424, lineno=14, colno=36)
              end_location: SourceLocation(pos=432, lineno=14, colno=44)
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
                                  location: SourceLocation(pos=488, lineno=16, colno=18)
                                  end_location: SourceLocation(pos=502, lineno=16, colno=32)
                                  is_tag: False
                                  namespace: 'namespace'
                                  path: 'temp'
                              path:
                                <class 'mecha.ast.AstNbtPath'>
                                  location: SourceLocation(pos=503, lineno=16, colno=33)
                                  end_location: SourceLocation(pos=510, lineno=16, colno=40)
                                  components:
                                    <class 'mecha.ast.AstNbtPathKey'>
                                      location: SourceLocation(pos=503, lineno=16, colno=33)
                                      end_location: SourceLocation(pos=507, lineno=16, colno=37)
                                      value: 'pos1'
                                    <class 'mecha.ast.AstNbtPathSubscript'>
                                      location: SourceLocation(pos=507, lineno=16, colno=37)
                                      end_location: SourceLocation(pos=510, lineno=16, colno=40)
                                      index:
                                        <class 'mecha.ast.AstNumber'>
                                          location: SourceLocation(pos=508, lineno=16, colno=38)
                                          end_location: SourceLocation(pos=509, lineno=16, colno=39)
                                          value: 0
                              fallback: None
                          right:
                            <class 'bolt_compute.float.AstFloatStorage'>
                              location: SourceLocation(pos=-1, lineno=0, colno=0)
                              end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                              depth: MutableDepth(value=3)
                              storage:
                                <class 'mecha.ast.AstResourceLocation'>
                                  location: SourceLocation(pos=521, lineno=16, colno=51)
                                  end_location: SourceLocation(pos=535, lineno=16, colno=65)
                                  is_tag: False
                                  namespace: 'namespace'
                                  path: 'temp'
                              path:
                                <class 'mecha.ast.AstNbtPath'>
                                  location: SourceLocation(pos=536, lineno=16, colno=66)
                                  end_location: SourceLocation(pos=543, lineno=16, colno=73)
                                  components:
                                    <class 'mecha.ast.AstNbtPathKey'>
                                      location: SourceLocation(pos=536, lineno=16, colno=66)
                                      end_location: SourceLocation(pos=540, lineno=16, colno=70)
                                      value: 'pos2'
                                    <class 'mecha.ast.AstNbtPathSubscript'>
                                      location: SourceLocation(pos=540, lineno=16, colno=70)
                                      end_location: SourceLocation(pos=543, lineno=16, colno=73)
                                      index:
                                        <class 'mecha.ast.AstNumber'>
                                          location: SourceLocation(pos=541, lineno=16, colno=71)
                                          end_location: SourceLocation(pos=542, lineno=16, colno=72)
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
                                  location: SourceLocation(pos=567, lineno=17, colno=18)
                                  end_location: SourceLocation(pos=581, lineno=17, colno=32)
                                  is_tag: False
                                  namespace: 'namespace'
                                  path: 'temp'
                              path:
                                <class 'mecha.ast.AstNbtPath'>
                                  location: SourceLocation(pos=582, lineno=17, colno=33)
                                  end_location: SourceLocation(pos=589, lineno=17, colno=40)
                                  components:
                                    <class 'mecha.ast.AstNbtPathKey'>
                                      location: SourceLocation(pos=582, lineno=17, colno=33)
                                      end_location: SourceLocation(pos=586, lineno=17, colno=37)
                                      value: 'pos1'
                                    <class 'mecha.ast.AstNbtPathSubscript'>
                                      location: SourceLocation(pos=586, lineno=17, colno=37)
                                      end_location: SourceLocation(pos=589, lineno=17, colno=40)
                                      index:
                                        <class 'mecha.ast.AstNumber'>
                                          location: SourceLocation(pos=587, lineno=17, colno=38)
                                          end_location: SourceLocation(pos=588, lineno=17, colno=39)
                                          value: 1
                              fallback: None
                          right:
                            <class 'bolt_compute.float.AstFloatStorage'>
                              location: SourceLocation(pos=-1, lineno=0, colno=0)
                              end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                              depth: MutableDepth(value=4)
                              storage:
                                <class 'mecha.ast.AstResourceLocation'>
                                  location: SourceLocation(pos=600, lineno=17, colno=51)
                                  end_location: SourceLocation(pos=614, lineno=17, colno=65)
                                  is_tag: False
                                  namespace: 'namespace'
                                  path: 'temp'
                              path:
                                <class 'mecha.ast.AstNbtPath'>
                                  location: SourceLocation(pos=615, lineno=17, colno=66)
                                  end_location: SourceLocation(pos=622, lineno=17, colno=73)
                                  components:
                                    <class 'mecha.ast.AstNbtPathKey'>
                                      location: SourceLocation(pos=615, lineno=17, colno=66)
                                      end_location: SourceLocation(pos=619, lineno=17, colno=70)
                                      value: 'pos2'
                                    <class 'mecha.ast.AstNbtPathSubscript'>
                                      location: SourceLocation(pos=619, lineno=17, colno=70)
                                      end_location: SourceLocation(pos=622, lineno=17, colno=73)
                                      index:
                                        <class 'mecha.ast.AstNumber'>
                                          location: SourceLocation(pos=620, lineno=17, colno=71)
                                          end_location: SourceLocation(pos=621, lineno=17, colno=72)
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
                              location: SourceLocation(pos=646, lineno=18, colno=18)
                              end_location: SourceLocation(pos=660, lineno=18, colno=32)
                              is_tag: False
                              namespace: 'namespace'
                              path: 'temp'
                          path:
                            <class 'mecha.ast.AstNbtPath'>
                              location: SourceLocation(pos=661, lineno=18, colno=33)
                              end_location: SourceLocation(pos=668, lineno=18, colno=40)
                              components:
                                <class 'mecha.ast.AstNbtPathKey'>
                                  location: SourceLocation(pos=661, lineno=18, colno=33)
                                  end_location: SourceLocation(pos=665, lineno=18, colno=37)
                                  value: 'pos1'
                                <class 'mecha.ast.AstNbtPathSubscript'>
                                  location: SourceLocation(pos=665, lineno=18, colno=37)
                                  end_location: SourceLocation(pos=668, lineno=18, colno=40)
                                  index:
                                    <class 'mecha.ast.AstNumber'>
                                      location: SourceLocation(pos=666, lineno=18, colno=38)
                                      end_location: SourceLocation(pos=667, lineno=18, colno=39)
                                      value: 2
                          fallback: None
                      right:
                        <class 'bolt_compute.float.AstFloatStorage'>
                          location: SourceLocation(pos=-1, lineno=0, colno=0)
                          end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                          depth: MutableDepth(value=4)
                          storage:
                            <class 'mecha.ast.AstResourceLocation'>
                              location: SourceLocation(pos=679, lineno=18, colno=51)
                              end_location: SourceLocation(pos=693, lineno=18, colno=65)
                              is_tag: False
                              namespace: 'namespace'
                              path: 'temp'
                          path:
                            <class 'mecha.ast.AstNbtPath'>
                              location: SourceLocation(pos=694, lineno=18, colno=66)
                              end_location: SourceLocation(pos=701, lineno=18, colno=73)
                              components:
                                <class 'mecha.ast.AstNbtPathKey'>
                                  location: SourceLocation(pos=694, lineno=18, colno=66)
                                  end_location: SourceLocation(pos=698, lineno=18, colno=70)
                                  value: 'pos2'
                                <class 'mecha.ast.AstNbtPathSubscript'>
                                  location: SourceLocation(pos=698, lineno=18, colno=70)
                                  end_location: SourceLocation(pos=701, lineno=18, colno=73)
                                  index:
                                    <class 'mecha.ast.AstNumber'>
                                      location: SourceLocation(pos=699, lineno=18, colno=71)
                                      end_location: SourceLocation(pos=700, lineno=18, colno=72)
                                      value: 2
                          fallback: None
                  exponent:
                    <class 'bolt_compute.float.AstFloatConstant'>
                      location: SourceLocation(pos=-1, lineno=0, colno=0)
                      end_location: SourceLocation(pos=-1, lineno=0, colno=0)
                      depth: MutableDepth(value=3)
                      value: 2.0
    <class 'mecha.ast.AstCommand'>
      location: SourceLocation(pos=729, lineno=23, colno=1)
      end_location: SourceLocation(pos=729, lineno=23, colno=1)
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
                  location: SourceLocation(pos=764, lineno=24, colno=15)
                  end_location: SourceLocation(pos=766, lineno=24, colno=17)
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
