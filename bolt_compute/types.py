from typing import Literal

type BoltType = Literal["default", "block", "entity"]
type OperationType = Literal["float", "integer"]

type AdditiveOperation = Literal["+", "-"]
type MultiplicativeOperation = Literal["/", "*", "//", "**", "%"]

type Operation = AdditiveOperation | MultiplicativeOperation
