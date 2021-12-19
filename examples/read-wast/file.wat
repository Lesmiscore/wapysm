(module
 (type $f64_=>_none (func (param f64)))
 (type $i32_=>_none (func (param i32)))
 (type $none_=>_none (func))
 (import "env" "print_console" (func $print_console (param f64)))
 (global $global$0 (mut i32) (i32.const 66560))
 (memory $0 2)
 (table $0 1 1 funcref)
 (export "memory" (memory $0))
 (export "gauss_legendre" (func $gauss_legendre))
 (export "_start" (func $_start))
 (func $gauss_legendre (param $0 i32)
  (local $1 f64)
  (local $2 f64)
  (local $3 i32)
  (local $4 f64)
  (local $5 f64)
  (local $6 f64)
  (block $label$1
   (block $label$2
    (br_if $label$2
     (i32.ge_s
      (local.get $0)
      (i32.const 1)
     )
    )
    (local.set $1
     (f64.const 1.7071067811865475)
    )
    (local.set $2
     (f64.const 1)
    )
    (br $label$1)
   )
   (local.set $3
    (i32.const 0)
   )
   (local.set $4
    (f64.const 0.25)
   )
   (local.set $5
    (f64.const 0.7071067811865475)
   )
   (local.set $2
    (f64.const 1)
   )
   (local.set $1
    (f64.const 1.7071067811865475)
   )
   (loop $label$3
    (local.set $1
     (f64.add
      (local.tee $5
       (f64.sqrt
        (f64.mul
         (local.get $5)
         (local.get $2)
        )
       )
      )
      (local.tee $6
       (f64.mul
        (local.get $1)
        (f64.const 0.5)
       )
      )
     )
    )
    (local.set $4
     (f64.sub
      (local.get $4)
      (f64.mul
       (f64.mul
        (local.tee $2
         (f64.sub
          (local.get $2)
          (local.get $6)
         )
        )
        (local.get $2)
       )
       (f64.convert_i32_s
        (i32.shl
         (i32.const 1)
         (local.get $3)
        )
       )
      )
     )
    )
    (local.set $2
     (local.get $6)
    )
    (br_if $label$3
     (i32.ne
      (local.get $0)
      (local.tee $3
       (i32.add
        (local.get $3)
        (i32.const 1)
       )
      )
     )
    )
   )
   (local.set $2
    (f64.mul
     (local.get $4)
     (f64.const 4)
    )
   )
  )
  (call $print_console
   (f64.div
    (f64.mul
     (local.get $1)
     (local.get $1)
    )
    (local.get $2)
   )
  )
 )
 (func $_start
  (call $print_console
   (f64.const 42)
  )
 )
)